from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import re
import logging
import time
import os
import subprocess

async def parse_lrc(path):
    """
    Parses an LRC file and extracts the lyrics with their corresponding timestamps.
    Args:
        path (str): The file path to the LRC file.
    Returns:
        list of tuple: A list of tuples where each tuple contains a timestamp (float) and a lyric (str).
    Raises:
        FileNotFoundError: If the file at the specified path does not exist.
        UnicodeDecodeError: If the file cannot be decoded using 'utf-8' encoding.
    Example:
        >>> lyrics = await parse_lrc('/path/to/file.lrc')
        >>> print(lyrics)
        [(12.34, 'Some lyric'), (56.78, 'Another lyric')]
    """
    logging.info(f"Reading LRC file: {path}")
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = content.encode('utf-8').decode('unicode_escape')

    lines = content.split("\n")

    lyrics = []

    for line in lines:
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

async def create_image(lyric, font):
    """
    Create an image with a gradient background and centered text.
    Args:
        lyric (str): The text to be displayed on the image.
        font (PIL.ImageFont.FreeTypeFont): The font to be used for the text.
    Returns:
        np.ndarray: The generated image as a NumPy array.
    """

    width, height = 1280, 720
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)


    colors = [
        (35, 21, 87),  # #231557
        (68, 16, 122),  # #44107A
        (255, 19, 97),  # #FF1361
        (255, 248, 0)   # #FFF800
    ]


    for y in range(height):
        ratio = y / height
        if ratio < 0.29:
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * (ratio / 0.29))
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * (ratio / 0.29))
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * (ratio / 0.29))
        elif ratio < 0.67:
            r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * ((ratio - 0.29) / 0.38))
            g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * ((ratio - 0.29) / 0.38))
            b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * ((ratio - 0.29) / 0.38))
        else:
            r = int(colors[2][0] + (colors[3][0] - colors[2][0]) * ((ratio - 0.67) / 0.33))
            g = int(colors[2][1] + (colors[3][1] - colors[2][1]) * ((ratio - 0.67) / 0.33))
            b = int(colors[2][2] + (colors[3][2] - colors[2][2]) * ((ratio - 0.67) / 0.33))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    lines = []
    words = lyric.split()
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        text_bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        if text_width <= width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    total_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines)
    y_offset = (720 - total_height) // 2

    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        position = ((1280 - text_width) // 2, y_offset)
        draw.text(position, line, font=font, fill="white")
        y_offset += text_bbox[3] - text_bbox[1]

    return np.array(img)

async def create_video(lrc_file, instrumental_file_path, output_file, wait_time=1):
    """
    Creates a video with lyrics displayed in sync with an instrumental audio track.
    Args:
        lrc_file (str): Path to the .lrc file containing the lyrics and timestamps.
        instrumental_file_path (str): Path to the instrumental audio file.
        output_file (str): Path where the final video file will be saved.
        wait_time (int, optional): Time in seconds to wait before checking for the instrumental file if it doesn't exist. Defaults to 1.
    Returns:
        None
    Raises:
        subprocess.CalledProcessError: If the ffmpeg command fails.
        IOError: If the font file cannot be loaded.
    """
    logging.info("Starting create_video_with_lyrics_and_instrumental")
    lyrics = await parse_lrc(lrc_file)  
    logging.info(f"Parsed {len(lyrics)} lines of lyrics")

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except IOError:
        font = ImageFont.load_default()

    lyric_images = {}

    video_segments = []

    if lyrics:
        first_timestamp = lyrics[0][0]
        blank_clip = ImageClip(await create_image("",font)).set_duration(first_timestamp)
        video_segments.append(blank_clip)
        logging.info(f"Added blank screen for {first_timestamp}s")

    for i, (timestamp, lyric) in enumerate(lyrics):
        logging.info(f"Creating video clip for lyric: {lyric} at {timestamp}s")
        
        if lyric not in lyric_images:
            lyric_images[lyric] = await create_image(lyric, font)
        
        duration = lyrics[i + 1][0] - timestamp if i + 1 < len(lyrics) else 5
        logging.info(f"Duration for lyric '{lyric}': {duration}s")

        img_array = lyric_images[lyric]
        img_clip = ImageClip(img_array).set_duration(duration).set_start(timestamp)
        video_segments.append(img_clip)

    video = concatenate_videoclips(video_segments, method="compose")

    temp_video_file = output_file.replace(".mp4", "_temp.mp4")
    video.write_videofile(temp_video_file, fps=24)

    logging.info("Finished render_video_without_audio")

    logging.info(f"Waiting for instrumental file: {instrumental_file_path}")
    while not os.path.exists(instrumental_file_path):
        logging.info(f"Instrumental file not found, waiting for {wait_time} seconds...")
        time.sleep(wait_time)

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
        "-y",  
        output_file
    ]
    subprocess.run(command, check=True)

    os.remove(temp_video_file)

    logging.info("Finished create_video_with_lyrics_and_instrumental")