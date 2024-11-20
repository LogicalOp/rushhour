from spotify import search_track, get_track_from_id, get_spotify_token
from youtube import find_youtube_match, download_audio
from liblrc import get_lyrics
from typing import Optional
import json

# Simple test flow before integration
def get_song(song_name: str, artist_name: str):
    client_id = '85ffb4098ca344518417ce90e4b5cce8'
    client_secret = '5dd0542356524a87b6827ae1d90d6704'

    token = get_spotify_token(client_id, client_secret)
    print(token)
    
    if token:
        spotify_track = search_track(song_name, artist_name, token)
        if spotify_track:
            spotify_name = spotify_track['track_name']
            spotify_artist = spotify_track['artist_name']
            spotify_duration = spotify_track['duration'] / 1000

            print(f"Spotify Track: {spotify_name} by {spotify_artist} ({spotify_duration}s)")

            youtube_match = find_youtube_match(spotify_name, spotify_artist, spotify_duration)

            if youtube_match:
                youtube_name = youtube_match['title']
                youtube_artist = youtube_match['uploader']
                youtube_duration = youtube_match['duration']

                print(f"Found match: {youtube_name} by {youtube_artist} ({youtube_duration}s)")

                download_audio(youtube_match['webpage_url'])

                lyrics = get_lyrics(spotify_name, spotify_artist)

                if lyrics:
                    print(json.dumps(lyrics, indent=4, sort_keys=True))

get_song("Still Ill", "The Smiths")