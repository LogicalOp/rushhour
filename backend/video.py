from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import re
import logging
import time
import os
import subprocess

def parse_lrc(path):
    logging.info(f"Reading LRC file: {path}")
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content into individual lines
    lines = content.split("\\n")

    lyrics = []

    for line in lines:
        # Clean up the line by removing unnecessary escape characters and quotes
        line = line.replace("\\", "").replace("\"", "").strip()
        match = re.match(r'\[(\d+):(\d+\.\d+)\](.*)', line)
        if match:
            minute, second, lyric = match.groups()
            timestamp = int(minute) * 60 + float(second)
            lyrics.append((timestamp, lyric.strip()))
            logging.info(f"Parsed lyric: '{lyric}' at {timestamp}s")
        else:
            logging.warning(f"Line did not match LRC format: {line.strip()}")

    logging.info(f"Parsed {len(lyrics)} lines of lyrics")
    return lyrics

def create_image(lyric, font, max_width=1280):
    img = Image.new('RGB', (1280, 720), color='black')  # Reduced resolution
    draw = ImageDraw.Draw(img)
    
    # Split the lyric into multiple lines if it exceeds the max width
    lines = []
    words = lyric.split()
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        text_bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Calculate the total height of the text
    total_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines)
    y_offset = (720 - total_height) // 2

    # Draw each line of text
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        position = ((1280 - text_width) // 2, y_offset)
        draw.text(position, line, font=font, fill="white")
        y_offset += text_bbox[3] - text_bbox[1]

    return np.array(img)

def create_video(lrc_file, instrumental_file_path, output_file, wait_time=1):
    logging.info("Starting create_video_with_lyrics_and_instrumental")
    lyrics = parse_lrc(lrc_file)
    logging.info(f"Parsed {len(lyrics)} lines of lyrics")

    # Load the font once
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except IOError:
        font = ImageFont.load_default()

    # Create a dictionary to store images for each unique lyric
    lyric_images = {}

    # Create a list to store video segments
    video_segments = []

    # Add a blank screen from 0 until the first timestamp
    if lyrics:
        first_timestamp = lyrics[0][0]
        blank_clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=first_timestamp)
        video_segments.append(blank_clip)
        logging.info(f"Added blank screen for {first_timestamp}s")

    # Create a video clip for each line of lyrics
    for i, (timestamp, lyric) in enumerate(lyrics):
        logging.info(f"Creating video clip for lyric: {lyric} at {timestamp}s")
        
        # Check if the image for this lyric already exists
        if lyric not in lyric_images:
            lyric_images[lyric] = create_image(lyric, font)
        
        # Calculate the duration for this clip
        duration = lyrics[i + 1][0] - timestamp if i + 1 < len(lyrics) else 5
        logging.info(f"Duration for lyric '{lyric}': {duration}s")

        # Create a video segment for this lyric
        img_array = lyric_images[lyric]
        img_clip = ImageClip(img_array).set_duration(duration).set_start(timestamp)
        video_segments.append(img_clip)

    # Concatenate the video segments
    video = concatenate_videoclips(video_segments, method="compose")

    # Write the video file without audio
    temp_video_file = output_file.replace(".mp4", "_temp.mp4")
    video.write_videofile(temp_video_file, fps=24)

    logging.info("Finished render_video_without_audio")

    # Wait for the instrumental file to be available
    logging.info(f"Waiting for instrumental file: {instrumental_file_path}")
    while not os.path.exists(instrumental_file_path):
        logging.info(f"Instrumental file not found, waiting for {wait_time} seconds...")
        time.sleep(wait_time)

    # Use ffmpeg to add the audio to the video
    logging.info("Adding audio to video using ffmpeg")
    command = [
        "ffmpeg",
        "-i", temp_video_file,
        "-i", instrumental_file_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        "-y",  # Overwrite output file if it exists
        output_file
    ]
    subprocess.run(command, check=True)

    # Remove the temporary video file
    os.remove(temp_video_file)

    logging.info("Finished create_video_with_lyrics_and_instrumental")