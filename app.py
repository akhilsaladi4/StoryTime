import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Flask, render_template, request, jsonify, session
from processing.backLogic import generate_initial_story, get_refined_story, split_story_into_sentences
from processing.imgprocessor import process_image
from processing.test_elevenlabs import test_elevenlabs_api
import sqlite3



app = Flask(__name__)

app.secret_key = 'i love neil ramesh'

def init_db():
    connection = sqlite3.connect('adventure_links.db')
    cursor = connection.cursor()

    with open('stories.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    #cursor.execute("DROP TABLE story")
    cursor.executescript(sql_script)
    connection.commit()
    connection.close()
    
init_db()

def initialize_story():
    with app.app_context():
        
        with sqlite3.connect('adventure_links.db') as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM story")
            story_count = cursor.fetchone()[0]
            print(story_count)
            if story_count == 0:
                print("added")
                
                full_story = generate_initial_story()
                
                first_line, *remaining_lines = full_story.split("\n", 1)
                backgroundKey = first_line.split("(")[0].replace("**Background: ", "").strip()
                updated_story = remaining_lines[0] if remaining_lines else ""
                
                cursor.execute("""
                    INSERT INTO story (story_content, background_key)
                    VALUES (?, ?)
                """, (updated_story, backgroundKey))
                
                conn.commit()
                
                print(f"Story Added - Background Key: {backgroundKey}")
            else:
                print("Story already exists, skipping insertion.")

@app.route('/read')
def reader():
    print("here")
    initialize_story()

    with sqlite3.connect('adventure_links.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT background_key FROM story ORDER BY story_id DESC LIMIT 1")
        latest_story = cursor.fetchone()
        
        if latest_story:
            latest_story = latest_story[0].replace("*","")
            sentences = split_story_into_sentences(latest_story)
            session['sentences'] = sentences
            session['current_sentence'] = 0
        else:
            latest_story = "No story available."
    
    return render_template('reading.html', story=latest_story)

@app.route('/next-sentence', methods=['GET'])
def next_sentence():
    current_sentence = session.get('current_sentence', 0)
    sentences = session.get('sentences', [])
    if current_sentence < len(sentences):
        sentence = sentences[current_sentence]
        session['current_sentence'] = current_sentence + 1
        test_elevenlabs_api(sentence)
        return jsonify({'sentence': sentence})
    else:
        return jsonify({'sentence': None})
    
@app.route('/read-sentence-aloud', methods=['POST'])
def read_sentence_aloud():
    data = request.get_json()
    sentence = data.get('sentence')
    if sentence:
        test_elevenlabs_api(sentence)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@app.route('/process-image', methods=['POST'])
def process_image_route():
    file = request.files['image']
    image_path = f'./static/images/{file.filename}'
    file.save(image_path)

    processed_data = process_image(image_path)
    if processed_data:
        with open("./static/results/emotions.txt", 'a') as f:
            f.write(f"{processed_data}\n")
        print("Data saved to file")
        return jsonify(processed_data)

    else:
        with open("./static/results/emotions.txt", 'a') as f:
            f.write(r"{'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.0, 'sad': 0.0, 'surprise': 0.0, 'neutral': 0.0}" + "\n")
        print('No faces found')
        return jsonify({'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.0, 'sad': 0.0, 'surprise': 0.0, 'neutral': 0.0})
    
@app.route('/refine-story', methods=['GET'])
def refine_story():
    refined_story = get_refined_story().replace("*","")
    
    with sqlite3.connect('adventure_links.db') as conn:
        first_line, *remaining_lines = refined_story.split("\n", 1)
        backgroundKey = first_line.split("(")[0].replace("**Background: ", "").strip()
        refined_story = remaining_lines[0] if remaining_lines else ""

        cursor = conn.cursor()
        backgroundKey = first_line.split("(")[0].replace("**Background: ", "").strip()
        cursor.execute("""
            INSERT INTO story (story_content, background_key)
            VALUES (?, ?)
        """, (refined_story, backgroundKey))  
        
        conn.commit()
    
    return jsonify({'refined_story': refined_story})

@app.route('/')
def index():
    return render_template('index.html')

app.debug = True

if __name__ == '__main__':
    if os.path.exists('stories.db'):
        os.remove('stories.db') 
    with open("./static/results/emotions.txt", 'w') as f:
        f.write(r"{'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.0, 'sad': 0.0, 'surprise': 0.0, 'neutral': 0.0}" + "\n")
    app.run(host='0.0.0.0', port=80)

