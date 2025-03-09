import requests
import pygame
import os
import time

# Replace with your actual Eleven Labs API key
API_KEY = "YOUR_APIKEY_HERE"

def test_elevenlabs_api(text):
    begin = time.time()
    # The endpoint for Eleven Labs Text-to-Speech API
    endpoint = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM/stream"
    
    
    

    # Set up the request headers with your API key
    headers = {
        "xi-api-key": API_KEY,  
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(endpoint, headers=headers, json=data)
    
    if response.status_code == 200:
        print("API key works! Speech has been generated.")
        with open("output_audio.mp3", "wb") as audio_file:
            audio_file.write(response.content)
        print("Audio saved as output_audio.mp3.")
        
        print("Time taken to generate speech:", time.time() - begin)
        pygame.mixer.init(frequency=22050, size=-16, channels=2)  
        pygame.mixer.music.load("output_audio.mp3")  
        pygame.mixer.music.play() 
        
        while pygame.mixer.music.get_busy(): 
            pygame.time.Clock().tick(10)  
        
    else:
        print(f"Failed to generate speech. Status code: {response.status_code}")
        print("Response:", response.json())

# Run the test function
test_elevenlabs_api("Starting up the server!")
