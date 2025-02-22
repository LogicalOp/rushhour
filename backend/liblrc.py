import requests
from typing import Optional
import os

root_url = 'https://lrclib.net/api/'

async def get_lyrics(track_name: str, artist_name: str, album_name: Optional[str] = None, duration: Optional[int] = None) -> Optional[str]:
    """
    Fetches lyrics for a given track and saves them to a file if they do not already exist.
    Args:
        track_name (str): The name of the track.
        artist_name (str): The name of the artist.
        album_name (Optional[str], optional): The name of the album. Defaults to None.
        duration (Optional[int], optional): The duration of the track in seconds. Defaults to None.
    Returns:
        Optional[str]: The lyrics of the track if successfully fetched, otherwise None.
    """

    if not os.path.exists('lrc'):
        os.makedirs('lrc')

    filename = os.path.join('lrc', f"{track_name} - {artist_name}.lrc")

    if os.path.exists(filename):
        print(f"File {filename} already exists")
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    
    track_name_encoded = track_name.replace(' ', '+')
    artist_name_encoded = artist_name.replace(' ', '+')
    url = f'{root_url}get?artist_name={artist_name_encoded}&track_name={track_name_encoded}'
    
    if album_name:
        album_name_encoded = album_name.replace(' ', '+')
        url += f'&album_name={album_name_encoded}'
    if duration:
        url += f'&duration={duration}'
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        filtered_data = {
            "id": data.get('id'),
            "artist_name": data.get('artistName'),
            "track_name": data.get('trackName'),
            "album_name": data.get('albumName'),
            "duration": data.get('duration'),
            "lrc": data.get('syncedLyrics')
        }

        formatted_lyrics = filtered_data['lrc'].replace('\\n', '\n')
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(formatted_lyrics)
        print(f"Lyrics saved to {filename}")
        
        return formatted_lyrics
    else:
        print(f"Failed to get lyrics: {response.status_code}")
        return None