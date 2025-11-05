from flask import Flask, render_template, request
from deepface import DeepFace
import os
import uuid
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Emotion to Bollywood songs mapping (Google Drive preview links)
emotion_playlist = {
    'happy': [
        {"title": "Abhi Kuch Dino Se", "url": "https://drive.google.com/file/d/1BVBdwyH8ztemQ4WaN6eoBdCQUhBrA-9Y/preview"},
        {"title": "Mere Bina", "url": "https://drive.google.com/file/d/18QKHZQdqG3_8Pk7BF0YpzC4YeDbTGNph/preview"},
        {"title": "Samjho Na X Wishes", "url": "https://drive.google.com/file/d/1pJdCDN_3zV_ReBHyTPjek1lUybOrilNk/preview"},
        {"title": "Zara Sa", "url": "https://drive.google.com/file/d/1rdQ9qUbbUIHQanz2VTTUm0vde1CuLLbS/preview"},
        {"title": "Tum Mile", "url": "https://drive.google.com/file/d/1eaPI01FmEeQci220yEjHmXJ4_ohAkuj5/preview"},
        {"title": "Tum Se Hi", "url": "https://drive.google.com/file/d/1sk5LmsEETAsO2QL_7zB8FIPXG88yM0Cg/preview"},
        {"title": "Dil Chahta Hai", "url": "https://drive.google.com/file/d/17YMKhbAAr1a0v7lU04eXqZUVLb90JBR_/preview"}
    ],
    'sad': [
        {"title": "Channa Mereya", "url": "https://drive.google.com/file/d/1xQs78QDm6Keh-3c5R02gX6JJUxBxP0E6/preview"},
        {"title": "Tujhe Bhula Diya", "url": "https://drive.google.com/file/d/10RfOc-v_2OtG2cTS_vJygdKmMzHkLYCb/preview"},
        {"title": "Dooriyan", "url": "https://drive.google.com/file/d/1uAjVLL8pSNb5FTc9sDQpMPxH-5VE1jDn/preview"},
        {"title": "Agar Tum Sath Ho", "url": "https://drive.google.com/file/d/1my7fFYlcImmG3oVetUt3tB5oKKTmVzKm/preview"},
        {"title": "Raabta", "url": "https://drive.google.com/file/d/19DgwVL9ekNDNU_UvZFhd9wc-QwirDsJm/preview"},
        {"title": "Tu Hi Meri Shab Hai", "url": "https://drive.google.com/file/d/1oMJ9t8_DSkNG5VMDx451SXoc4AKDhUcH/preview"}
    ],
    'angry': [
        {"title": "Saada Haq", "url": "https://drive.google.com/file/d/1reSryO2rgIjWGdZ2PgZbno5nmmcywWpH/preview"},
        {"title": "Bulleya", "url": "https://drive.google.com/file/d/116l9rKuM1YHYtPnqFW-vk76Ms7E7dq-R/preview"},
        {"title": "Sher Aaya Sher", "url": "https://drive.google.com/file/d/1lx-3R6NydgNDZSGVYUCI3K6gDTA7XnFs/preview"}
    ],
    'neutral': [
        {"title": "Kabira", "url": "https://drive.google.com/file/d/1OBw5YVlxMsAoNKNT9DEj0dkZyOb2lLw7/preview"},
        {"title": "Tera Hone", "url": "https://drive.google.com/file/d/1C0z_LLbvoGR1qKM8a94fUZsHijR6NBTp/preview"},
        {"title": "Akhiyaan Gulaab", "url": "https://drive.google.com/file/d/1B1gt1OiVe0PSuO1HHqP_SsTSDN4dJUPZ/preview"},
        {"title": "Zara Zara", "url": "https://drive.google.com/file/d/1N-alcljFfJ7oveTmMRKG5PqewawIZffv/preview"},
        {"title": "Saibo", "url": "https://drive.google.com/file/d/17jegkO64D7AM7BffpNyuI4WwWZN_NjG0/preview"},
        {"title": "Khuda Jaane", "url": "https://drive.google.com/file/d/1wjzQTRSfaUsWJzFbLhWuoLSkLgyYp24n/preview"}
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    emotion = None
    playlist = []
    
    if request.method == 'POST':
        img_data = request.form['image']
        img_str = img_data.split(",")[1]
        img_bytes = base64.b64decode(img_str)
        
        filename = str(uuid.uuid4()) + ".jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        image = Image.open(BytesIO(img_bytes))
        image.save(filepath)

        try:
            result = DeepFace.analyze(img_path=filepath, actions=['emotion'], enforce_detection=False)
            detected_emotion = result[0]['dominant_emotion'].lower()
        except Exception as e:
            print("Error analyzing emotion:", e)
            detected_emotion = 'neutral'

        # Simplify emotion categories
        emotion_map = {
            'happy': 'happy',
            'sad': 'sad',
            'angry': 'angry',
            'disgust': 'angry',
            'fear': 'sad',
            'surprise': 'happy',
            'neutral': 'neutral'
        }

        emotion = emotion_map.get(detected_emotion, 'neutral')
        playlist = emotion_playlist.get(emotion, emotion_playlist['neutral'])

        os.remove(filepath)

    return render_template('index.html', emotion=emotion, playlist=playlist)


if __name__ == "__main__":
    app.run(debug=True)

