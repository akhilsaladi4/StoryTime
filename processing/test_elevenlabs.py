import requests
import pygame
import os
import time

# Replace with your actual Eleven Labs API key
API_KEY = "sk_5a819d5b34425324df843d18e16bdbf09362b1b8c9c2cd6d"

def test_elevenlabs_api(text):
    begin = time.time()
    # The endpoint for Eleven Labs Text-to-Speech API
    endpoint = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM/stream"
    
    # Example text to convert to speech
    
    

    # Set up the request headers with your API key
    headers = {
        "xi-api-key": API_KEY,  # Correct way to pass the API key
        "Content-Type": "application/json"
    }

    # Set up the request data
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    # Make the POST request to the Eleven Labs API
    response = requests.post(endpoint, headers=headers, json=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        print("API key works! Speech has been generated.")
        # Save the audio file to disk if needed
        with open("output_audio.mp3", "wb") as audio_file:
            audio_file.write(response.content)
        print("Audio saved as output_audio.mp3.")
        
        print("Time taken to generate speech:", time.time() - begin)
        # Initialize pygame mixer for audio playback
        pygame.mixer.init(frequency=22050, size=-16, channels=2)  # Specify the audio format
        pygame.mixer.music.load("output_audio.mp3")  # Load the audio file
        pygame.mixer.music.play()  # Play the audio
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():  # Check if the music is still playing
            pygame.time.Clock().tick(10)  # Sleep for 10ms and keep checking
        
    else:
        print(f"Failed to generate speech. Status code: {response.status_code}")
        print("Response:", response.json())

# Run the test function
test_elevenlabs_api("Starting up the server!")
