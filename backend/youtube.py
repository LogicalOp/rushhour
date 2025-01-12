import yt_dlp
from typing import Optional
import os
import time

async def find_youtube_match(song_name: str, artist_name: str, target_duration: int):
    """
    Find the best matching YouTube video for a given song and artist.
    This function searches YouTube for videos matching the provided song name and artist name,
    and returns the video that best matches the target duration. It uses cookies for authentication
    and age restriction purposes.
    Args:
        song_name (str): The name of the song to search for.
        artist_name (str): The name of the artist to search for.
        target_duration (int): The target duration of the video in seconds.
    Returns:
        dict: A dictionary containing information about the best matching video, or None if no match is found.
    Raises:
        FileNotFoundError: If the cookies file does not exist.
    Note:
        This function requires the `yt_dlp` library and a valid `cookies.txt` file for YouTube authentication.
    """
    start_time = time.time()
    query = f"{song_name} {artist_name}"
    cookies_file = 'cookies.txt'

    if not os.path.exists(cookies_file):
        print(f"Cookies file not found: {cookies_file}")
        return None

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio',
        'default_search': 'ytsearch5',  
        'noplaylist': True,
        'cookiefile': cookies_file,
        'age_limit': 17
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(query, download=False)['entries']
    print(f"Search time: {time.time() - start_time:.2f} seconds")

    best_match = None
    min_duration_diff = float('inf')

    for video in search_results:
        if not video:
            continue

        video_duration = video.get('duration', 0)
        channel_name = video.get('uploader', '')

        is_topic_channel = " - Topic" in channel_name

        duration_diff = abs(video_duration - target_duration)
        if duration_diff < min_duration_diff or (is_topic_channel and duration_diff <= min_duration_diff):
            best_match = video
            min_duration_diff = duration_diff

    print(f"Total time: {time.time() - start_time:.2f} seconds")
    return best_match

async def download_audio(video_url: str, title: str, artist: str):
    """
    Downloads the audio from a YouTube video and saves it as an MP3 file.
    Args:
        video_url (str): The URL of the YouTube video to download.
        title (str): The title to use for the downloaded audio file.
        artist (str): The artist name to use for the downloaded audio file.
    Returns:
        None
    Notes:
        - The function requires a cookies file named 'cookies.txt' to be present in the working directory.
        - The downloaded audio file will be saved in the 'downloads' directory with the format '{title} - {artist}.mp3'.
        - The function uses yt-dlp to download and process the audio.
        - The function sets an age limit of 17 for the content to be downloaded.
    """
    cookies_file = 'cookies.txt'
    
    # Check if the cookies file exists
    if not os.path.exists(cookies_file):
        print(f"Cookies file not found: {cookies_file}")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'downloads/{title} - {artist}.%(ext)s',
        'cookiefile': cookies_file,  
        'age_limit': 17  
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        print(f"Downloaded: {video_url}")
