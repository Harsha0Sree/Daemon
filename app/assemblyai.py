import os
import re
import time

import requests
from dotenv import load_dotenv

base_url = "https://api.assemblyai.com"
load_dotenv()
API_KEY = os.environ.get("ASSEMBLY_API_KEY")

headers = {"authorization": API_KEY}


def upload_audio(audio_file):

    a = audio_file.read()
    response = requests.post(base_url + "/v2/upload", headers=headers, data=a)
    audio_url = response.json()["upload_url"]
    return audio_url


def start_transcript(audio_url):
    data = {
        "audio_url": audio_url,
        "language_detection": True,
        "speech_models": ["universal-3-pro", "universal-2"],
    }

    url = base_url + "/v2/transcript"
    response = requests.post(url, json=data, headers=headers)

    transcript_id = response.json()["id"]
    return transcript_id


def get_transcript(transcript_id):
    polling_endpoint = base_url + "/v2/transcript/" + transcript_id

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()
        transcript_text = transcription_result["text"]

        if transcription_result["status"] == "completed":
            return transcript_text

        elif transcription_result["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)


def extract_workout(transcript_text):
    match = re.search(r"(\d+)\s+(\w+)", transcript_text)
    if match:
        return int(match.group(1)), match.group(2)
    else:
        return None


def process_voice_data(audio):
    audio_url = upload_audio(audio.file)

    transcript_id = start_transcript(audio_url)

    transcript_text = get_transcript(transcript_id)

    reps, exercise = extract_workout(transcript_text)

    return reps,exercise
