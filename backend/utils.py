import csv
import os
import json
import logging
from datetime import datetime, timedelta
from spotify import search_track, get_spotify_token
from youtube import find_youtube_match, download_audio
from liblrc import get_lyrics
from video import create_video
from stemming import separate_and_save
import aiofiles
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)

async def delete_old_videos(directory: str, age_minutes: int):
    now = datetime.now()
    cutoff = now - timedelta(minutes=age_minutes)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time < cutoff:
                logging.info(f"Deleting old video file: {file_path}")
                os.remove(file_path)

async def log_download(song_name: str, artist_name: str):
    async with aiofiles.open('download_counts.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        await writer.writerow([song_name, artist_name])

async def get_download_counts():
    download_counts = {}
    if not os.path.exists('download_counts.csv'):
        return download_counts

    async with aiofiles.open('download_counts.csv', mode='r') as file:
        content = await file.read()
        reader = csv.reader(content.splitlines())
        for row in reader:
            song_name, artist_name = row
            key = f"{song_name} - {artist_name}"
            if key in download_counts:
                download_counts[key] += 1
            else:
                download_counts[key] = 1

    return download_counts

async def get_song_details(song_name: str, artist_name: str):
    logging.info("Starting get_song_details")
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    if not os.path.exists('lrc'):
        os.makedirs('lrc')
    if not os.path.exists('videos'):
        os.makedirs('videos')

    # Delete old videos
    await delete_old_videos('videos', 10)

    client_id = '85ffb4098ca344518417ce90e4b5cce8'
    client_secret = '5dd0542356524a87b6827ae1d90d6704'

    logging.info("Getting Spotify token")
    token = await get_spotify_token(client_id, client_secret)
    if not token:
        logging.error("Failed to get Spotify token")
        return {"error": "Failed to get Spotify token"}

    logging.info("Searching for track on Spotify")
    spotify_track = await search_track(song_name, artist_name, token)
    if not spotify_track:
        logging.error("Spotify track not found")
        return {"error": "Spotify track not found"}

    spotify_name = spotify_track['track_name']
    spotify_artist = spotify_track['artist_name']
    spotify_duration = spotify_track['duration'] / 1000

    lrc_file = os.path.join('lrc', f"{spotify_name} - {spotify_artist}.lrc")
    audio_filename = os.path.join('downloads', f"{spotify_name} - {spotify_artist}.mp3")
    video_filename = os.path.join('videos', f"{spotify_name} - {spotify_artist}.mp4")
    instrumental_filename = f"{spotify_name} - {spotify_artist}_instrumental.wav"

    if os.path.exists(lrc_file) and os.path.exists(video_filename):
        logging.info("Files already exist, reading from cache")
        await log_download(spotify_name, spotify_artist)
        return {
            "video_file": video_filename
        }

    logging.info("Finding YouTube match")
    youtube_match = await find_youtube_match(spotify_name, spotify_artist, spotify_duration)
    if not youtube_match:
        logging.error("YouTube match not found")
        return {"error": "YouTube match not found"}

    logging.info("Downloading audio from YouTube")
    await download_audio(youtube_match['webpage_url'], spotify_name, spotify_artist)

    logging.info("Getting lyrics")
    lyrics = await get_lyrics(spotify_name, spotify_artist)
    if not lyrics:
        logging.error("Lyrics not found")
        return {"error": "Lyrics not found"}

    async with aiofiles.open(lrc_file, 'w', encoding='utf-8') as file:
        await file.write(json.dumps(lyrics, indent=4, sort_keys=True))

    logging.info("Creating video and separating audio")
    try:
        video_task = create_video(lrc_file, instrumental_filename, video_filename)
        separate_task = separate_and_save(audio_filename, f"{spotify_name} - {spotify_artist}")
        vocals_file, instrumental_file = await separate_task
        await video_task
    except Exception as e:
        logging.error(f"Error during video creation or audio separation: {e}")
        return {"error": str(e)}

    # Delete intermediate files
    logging.info("Deleting intermediate files")
    if os.path.exists(lrc_file):
        os.remove(lrc_file)
    if vocals_file and os.path.exists(vocals_file):
        os.remove(vocals_file)
    if instrumental_file and os.path.exists(instrumental_file):
        os.remove(instrumental_file)
    if os.path.exists(audio_filename):
        os.remove(audio_filename)

    logging.info("Finished get_song_details")
    await log_download(spotify_name, spotify_artist)
    return {
        "video_file": video_filename
    }