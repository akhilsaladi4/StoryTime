import os
import requests
import re
import json



API_KEY = "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"  # <-- REPLACE THIS WITH YOUR ACTUAL API KEY

ENDPOINT = "https://api.openai.com/v1/chat/completions"

def get_test_emotion_data():
    return [
        {"happy": 0.24, "surprise": 0.15},
        {"sad": 0.30, "angry": 0.12},
        {"fear": 0.18, "happy": 0.20},
        {"disgust": 0.25, "happy": 0.10},
        {"angry": 0.22, "sad": 0.14}
    ]

def read_emotion_data(file_path="./static/results/emotions.txt"):
    try:
        with open(file_path, 'r') as f:
            emotion_data = [json.loads(line.strip()) for line in f]

        return [
            {k: v for k, v in entry.items() if k != "neutral" and v > 0.1}
            for entry in emotion_data if isinstance(entry, dict)
        ] or get_test_emotion_data()

    except Exception:
        return get_test_emotion_data()

def generate_initial_story():

    # Define backgrounds in a properly formatted way
    backgrounds = {
        "Autumn": "Autumn.png",
        "Empty Field": "emptyField.png",
        "Fairy Land": "FairyLand.png",
        "Family": "Family.png",
        "Farms": "Farms.png",
        "Jungle": "jungle.png",
        "Mountain": "Mountain.png",
        "Park": "Park.png",
        "Rainbow": "Rainbow.png",
        "Winter Wonderland": "SnowMan.png",
        "Space": "Space.png",
        "Swamp": "Swamp.png"
    }

    # Convert dictionary to formatted text
    background_options = "\n".join([f"- {key}: {value}" for key, value in backgrounds.items()])

    prompt = (
        "Create a 2 sentence engaging story about a magical adventure with a moral. "
        "MAKE SURE YOU DO NOT USE ANY SPECIAL CHARACTERS OR BOLDED WORDS ANYWHERE IN YOUR RESPONSE ex. *   . Make sure you are talking to someone around six years old during your story.\n\n"
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a creative AI generating engaging stories based on different backgrounds."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        story = response.json()['choices'][0]['message']['content']
        return story.replace("*", "") 
    except Exception:
        return "An error occurred while generating the story."


def split_story_into_sentences(story):
    """Splits a story into sentences."""
    return re.split(r'(?<=[.!?])\s+', story)

def match_sentences_to_emotions(sentences, emotion_data):
    """Matches detected emotions to corresponding story sentences."""
    return [
        {"sentence": sentences[i], "emotions": emotion_data[min(i, len(emotion_data)-1)]}
        for i in range(len(sentences))
    ]

def refine_story_based_on_emotions(matched_sentences):
    """Refines a story based on detected emotions."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    backgrounds = {
        "Autumn": "Autumn.png",
        "Empty Field": "emptyField.png",
        "Fairy Land": "FairyLand.png",
        "Family": "Family.png",
        "Farms": "Farms.png",
        "Jungle": "jungle.png",
        "Mountain": "Mountain.png",
        "Park": "Park.png",
        "Rainbow": "Rainbow.png",
        "Winter Wonderland": "SnowMan.png",
        "Space": "Space.png",
        "Swamp": "Swamp.png"
    }
    
    background_options = "\n".join([f"- {key}: {value}" for key, value in backgrounds.items()])
    
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You refine stories based on emotions."},
            {"role": "user", "content": (
                "Here is a story with detected emotions per sentence:\n\n" +
                "\n".join(f"Sentence: \"{entry['sentence']}\"\nEmotions: {entry['emotions']}\n"
                            for entry in matched_sentences) +
                f"\nMAKE SURE YOU DO NOT USE ANY SPECIAL CHARACTERS OR BOLDED WORDS ANYWHERE IN YOUR RESPONSE ex. *, #. First, give us a report about emotions from the user and what topics elicited them. Be honest and include positive as well as negative feelings. Ex. The user seemed to like _____ but despised ____. Then, write 'xxxxxx' then write a similar story to make it more engaging and emotionally resonant based on the the user's likes and dislikes. Use simple language, language that would be easily understood by a 6-7 year old. Don't make the story over 2 small paragraphs"
            )}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    try:
        response = requests.post(ENDPOINT, headers=headers, json=data)
        response.raise_for_status()

        full_response = response.json()['choices'][0]['message']['content']
        
        emotion_report, refined_story = full_response.split("xxxxxx", 1)
        
        print(emotion_report)
        
        return refined_story
    except Exception:
        return "An error occurred while refining the story."

def get_refined_story():
    initial_story = generate_initial_story()
    emotion_data = read_emotion_data()
    sentences = split_story_into_sentences(initial_story)
    matched_sentences = match_sentences_to_emotions(sentences, emotion_data)
    return refine_story_based_on_emotions(matched_sentences)

