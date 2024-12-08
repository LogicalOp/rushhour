import yt_dlp
from typing import Optional
import os
import time

def find_youtube_match(song_name: str, artist_name: str, target_duration: int):
    start_time = time.time()
    query = f"{song_name} {artist_name}"
    cookies_file = 'cookies.txt'

    if not os.path.exists(cookies_file):
        print(f"Cookies file not found: {cookies_file}")
        return None

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio',
        'default_search': 'ytsearch5',  # Reduced number of search results
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

def download_audio(video_url: str, title: str, artist: str):
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
