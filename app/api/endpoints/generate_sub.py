from fastapi import APIRouter, HTTPException
from app.services.youtube import download_youtube_file
from app.services.gemini import process_subtitles_with_gemini
import os


router = APIRouter()


@router.post("/generateSab")
async def generate_subtitles(videoId: str):
    output_path = ""
    try:
        output_path = download_youtube_file(videoId)
        subtitles = process_subtitles_with_gemini(output_path)
        return {"subtitles": subtitles}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error while generating subtitles: {str(e)}")
