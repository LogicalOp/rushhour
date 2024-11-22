from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import re

def parse_lrc(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    lyrics = []

    for line in lines:
        match = re.match(r'\[(\d+):(\d+\.\d+)\](.*)', line)
        if match:
            minute, second, lyric = match.groups()
            timestamp = int(minute) * 60 + float(second)
            lyrics.append((timestamp, lyric.strip()))

    return lyrics

def create_video(lrc_file, instrumental_file, output_file):
    lyrics = parse_lrc(lrc_file)

    # Load the audio file
    audio = AudioFileClip(instrumental_file)

    test_clips = []

    # Create a video clip for each line of lyrics
    for timestamp, lyric in lyrics:
        # Create an image for the lyric
        img = Image.new('RGB', (1920, 1080), color='black')
        draw = ImageDraw.Draw(img)
        
        # Use a more readable font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        except IOError:
            font = ImageFont.load_default()
        
        # Use textbbox (instead of textsize) to calculate text dimensions
        text_bbox = draw.textbbox((0, 0), lyric, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Calculate the position to center the text
        position = ((1920 - text_width) // 2, (1080 - text_height) // 2)
        
        # Draw the text on the image
        draw.text(position, lyric, font=font, fill='white')

        # Convert the image to a numpy array
        img_array = np.array(img)

        # Convert the numpy array to a video clip
        img_clip = ImageClip(img_array).set_duration(3).set_start(timestamp)
        test_clips.append(img_clip)
    
    # Concatenate all the image clips into one video
    video = concatenate_videoclips(test_clips, method="compose")

    # Set the audio to the video
    video = video.set_audio(audio)

    # Set the fps (frames per second) of the video, e.g., 24 fps
    video = video.set_fps(24)

    # Write the video to the output file
    video.write_videofile(output_file, codec='libx264')

# Example call to the function
create_video("/usr/local/home/u200298/Downloads/rushhour/backend/lrc/A Bar Song (Tipsy) - Shaboozey.lrc", "/usr/local/home/u200298/Downloads/rushhour/backend/Music/Instrumental/Eoin.wav", "/usr/local/home/u200298/Downloads/rushhour/backend/Music/output/output.mp4")
