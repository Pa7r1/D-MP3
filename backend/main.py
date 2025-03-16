from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp as youtube_dl
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class VideoRequest (BaseModel):
    url:str
    download_folder: str

@app.post("/download")
async def download_video (video: VideoRequest):
    try:
        if not os.path.exists(video.download_folder):
         os.makedirs(video.download_folder)

        print(video.download_folder)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'outtmpl': os.path.join(video.download_folder, '%(title)s.%(ext)s'),
            'ffmpeg_location': 'C:\\FFmpeg\\bin',
            'noplaylist':False,
            'ignoreerrors': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video.url, download = True)
            if 'entries' in info:
                filenames = []
                for entry in info['entries']:
                    if entry is not None:
                        filename = ydl.prepare_filename(entry).replace (".webm", ".mp3").replace(".m4a", ".mp3")
                        filenames.append(filename)
                        return{"message":"Descarga completa", "files": filenames}
                    else:
                        filename = ydl.prepare_filename(info).replace(".webm",".mp3").replace(".m4a",".mp3")
                        return {"message": "Descarga completa", "file":filename}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al descargar: {str(e)}")