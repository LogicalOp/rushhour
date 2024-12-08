from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from utils import get_song_details

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/song/")
async def song(song_name: str, artist_name: str):
    result = get_song_details(song_name, artist_name)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    file_path = result["video_file"]
    return FileResponse(file_path, media_type='video/mp4', filename=f"{song_name} - {artist_name}.mp4")