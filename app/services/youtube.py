from fastapi import HTTPException
from pytubefix import YouTube
from app.config import config
import logging
import os

output_path = config.get("youtube", "output_path")


def download_youtube_file(video_id: str):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            logging.warning(f"No audio stream found for video: {video_id}")
            raise HTTPException(
                status_code=404, detail="Audio stream not found")

        logging.info(f"Processing video: {video_id}")
        audio_stream.download(output_path, filename=f"{video_id}.mp3")
        logging.info(f"Audio downloaded successfully: {output_path}")
        return output_path + "/" + video_id + ".mp3"

    except Exception as e:
        logging.error(f"Error processing video {video_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
