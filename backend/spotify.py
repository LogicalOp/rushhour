import requests
import base64
from typing import Optional

client_id = '85ffb4098ca344518417ce90e4b5cce8'
client_secret = '5dd0542356524a87b6827ae1d90d6704'

async def get_spotify_token(client_id: str, client_secret: str) -> Optional[str]:
    """
    Fetches a Spotify access token using client credentials.
    Args:
        client_id (str): The client ID provided by Spotify.
        client_secret (str): The client secret provided by Spotify.
    Returns:
        Optional[str]: The access token if the request is successful, otherwise None.
    """
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
    }
    data = {
        'grant_type': 'client_credentials'
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        print(f"Failed to get token: {response.status_code}")
        print(response.json())
        return None


token = get_spotify_token(client_id, client_secret)

async def search_track(track_name: str, artist_name: str, token: str) -> Optional[dict]:
    """
    Search for a track on Spotify by track name and artist name.
    Args:
        track_name (str): The name of the track to search for.
        artist_name (str): The name of the artist of the track.
        token (str): The OAuth token for Spotify API authentication.
    Returns:
        Optional[dict]: A dictionary containing track information if found, 
                        otherwise None. The dictionary contains the following keys:
                        - 'id': The Spotify ID of the track.
                        - 'artist_name': The name of the artist.
                        - 'track_name': The name of the track.
                        - 'album_name': The name of the album.
                        - 'duration': The duration of the track in milliseconds.
    """
    query = f'{artist_name} {track_name}'.replace(' ', '+')
    url = f'https://api.spotify.com/v1/search?q={query}&type=track'
    headers = { 'Authorization': f'Bearer {token}' }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        tracks = data.get('tracks', {}).get('items', [])
        
        if tracks:
            track = tracks[0]
            return {
                'id': track.get('id'),
                'artist_name': track.get('artists')[0].get('name'),
                'track_name': track.get('name'),
                'album_name': track.get('album').get('name'),
                'duration': track.get('duration_ms')
            }
        else:
            print("No tracks found")
            return None
    else:
        print(f"Failed to search track: {response.status_code}")
        print(response.json())
        return None

async def get_track_from_id(track_id: str, token: str) -> Optional[dict]:
    """
    Fetches track information from Spotify using the track ID.
    Args:
        track_id (str): The Spotify ID of the track.
        token (str): The OAuth token for authorization.
    Returns:
        Optional[dict]: A dictionary containing track information if the request is successful, 
                        None otherwise. The dictionary contains the following keys:
                        - 'id': The track ID.
                        - 'artist_name': The name of the artist.
                        - 'track_name': The name of the track.
                        - 'album_name': The name of the album.
                        - 'duration': The duration of the track in milliseconds.
    """
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = { 'Authorization': f'Bearer {token}' }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            'id': data.get('id'),
            'artist_name': data.get('artists')[0].get('name'),
            'track_name': data.get('name'),
            'album_name': data.get('album').get('name'),
            'duration': data.get('duration_ms')
        }
    else:
        print(f"Failed to get track: {response.status_code}")
        print(response.json())
        return None