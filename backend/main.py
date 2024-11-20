from fastapi import FastAPI
from typing import Optional
from liblrc import get_lyrics
from utils import get_song

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/lrclib/")
async def lyrics(track_name: str, artist_name: str, album_name: Optional[str] = None, duration: Optional[int] = None):
    result = get_lyrics(track_name, artist_name, album_name, duration)
    if result:
        return result
    else:
        return {"error": "Lyrics not found"}
    
@app.get("/song/")
async def song(song_name: str, artist_name: str):
    result = get_song(song_name, artist_name)
    if result:
        return result
    else:
        return {"error": "Song not found"}

    

