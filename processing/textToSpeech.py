import os
import requests
import base64
import pygame

API_KEY = "YOUR_APIKEY_HERE" 

def text_to_speech(text, voice_id="21m00Tcm4TlvDq8ikWAM"):
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1"  
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error calling ElevenLabs TTS API:", e)
        return None
    except ValueError as e:
        print("Error parsing JSON from ElevenLabs TTS API:", e)
        return None

def save_audio(audio_base64, output_filename="output.mp3"):
    try:
        audio_data = base64.b64decode(audio_base64)
        with open(output_filename, "wb") as f:
            f.write(audio_data)
        print(f"Audio saved to {output_filename}")
    except Exception as e:
        print("Error saving audio file:", e)

def play_audio(filename="output.mp3"):
    if not os.path.exists(filename):
        print(f" Error: {filename} not found.")
        return

    print(f"Playing {filename}...")

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) 

    print(" Playback finished.")


