from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import get_song_details, get_download_counts
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/song/")
async def song(song_name: str, artist_name: str):
    result = await get_song_details(song_name, artist_name)  
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    file_path = result["video_file"]
    file_name = os.path.basename(file_path)
    return FileResponse(file_path, media_type='video/mp4', filename=file_name)

@app.get("/chart/")
async def chart():
    download_counts = await get_download_counts()  
    return download_counts