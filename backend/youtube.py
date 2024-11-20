import yt_dlp
from typing import Optional

def find_youtube_match(song_name: str, artist_name: str, target_duration: int):
    query = f"{song_name} {artist_name}"
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio',
        'default_search': 'ytsearch10',  # Search top 10 results
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(query, download=False)['entries']

    best_match = None
    min_duration_diff = float('inf')

    for video in search_results:
        if not video:  # Skip if video data is missing
            continue

        video_duration = video.get('duration', 0)  # Duration in seconds
        channel_name = video.get('uploader', '')

        # Check if it's a 'Topic' channel
        is_topic_channel = " - Topic" in channel_name

        # Calculate the duration difference
        duration_diff = abs(video_duration - target_duration)
        if duration_diff < min_duration_diff or (is_topic_channel and duration_diff <= min_duration_diff):
            best_match = video
            min_duration_diff = duration_diff

    return best_match

def download_audio(video_url: str, title: str, artist: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': 'C:/Users/dylan/AppData/Local/Microsoft/WinGet/Links/ffmpeg.exe',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'downloads/{title} - {artist}.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        print(f"Downloaded: {video_url}")
