import google.generativeai as genai
from fastapi import HTTPException
from app.config import config
from pytube import YouTube
import logging
import json
import os

genai.configure(api_key=config.get("gemini", "api_key"))
prompt = config.get("gemini", "prompt")


def process_subtitles_with_gemini(file_path: str):

    try:
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config
        )
        logging.debug("Gemini model initialized")

        files = [
            upload_to_gemini(file_path, mime_type="audio/mpeg"),
        ]
        logging.info("File uploaded to Gemini")

        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        files[0],
                    ],
                },])
        print(prompt)
        response = chat_session.send_message(prompt)
        print(response.text)
        # subtitles = json.loads(response.text)
        # logging.info("Subtitles processed successfully")

        try:
            subtitles = json.loads(response.text)
            print(subtitles)
            return subtitles
        except json.JSONDecodeError:
            json_content = response.text.strip('`').strip()
            json_content = json_content.replace('json\n', '', 1)

            # Parse the JSON content
            parsed_json = json.loads(json_content)
            print(parsed_json)
            return parsed_json
    except genai.ModelServiceError as e:
        logging.error(f"Gemini API error: {e}")
        raise
    except Exception as e:
        logging.exception(f"Unexpected error occurred: {e}")
        raise


def upload_to_gemini(path, mime_type=None):
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        logging.info(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error uploading file: {e}")
