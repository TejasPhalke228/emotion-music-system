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

# Emotion to Bollywood songs mapping
emotion_playlist = {
    'happy': [
        {"title": "pehla nasha", "url":"https://drive.google.com/uc?export=download&id=13bfaZXgsGNPPkD_pA-Rkm8FXTNO3bQeD",
        {"title": "tujhe dekha", "url":"https://drive.google.com/uc?export=download&id=1JdXgcvcfiqftvr5-CLcGGXvRx6WOKMjq"},
		{"title": "badtameez dil", "url":"https://drive.google.com/uc?export=download&id=1R6BWqjS2x22C3bziEuhhBLfhvbSw8S5B"},
		{"title": "ilahi", "url":"https://drive.google.com/uc?export=download&id=1EvDoLKpCbcwyK4ArKaHr4Z8U4M7S0X70"}
    ],
    'sad': [
        {"title": "channa mereya", "url":"https://drive.google.com/uc?export=download&id=1xQs78QDm6Keh-3c5R02gX6JJUxBxP0E6"},
        {"title": "tum hi ho", "url":"https://drive.google.com/uc?export=download&id=1VGPTp2-xN1lRUF36P3yfR5z9BbvTnS4r"},
	{"title": "dooriyan", "url":"https://drive.google.com/uc?export=download&id=1uAjVLL8pSNb5FTc9sDQpMPxH-5VE1jDn"}
    ],
    'angry': [
       {"title": "saada haq", "url":"https://drive.google.com/uc?export=download&id=1reSryO2rgIjWGdZ2PgZbno5nmmcywWpH"},
        {"title": "bulleya", "url":"https://drive.google.com/uc?export=download&id=116l9rKuM1YHYtPnqFW-vk76Ms7E7dq-R"}
    ],
    'surprise': [
        {"title": "ek ladki", "url":"https://drive.google.com/uc?export=download&id=1dIEjD7HH_FpndU9Px1oGQIiwNr_Re-4Q"}
    ],
    'neutral': [
	{"title": "kabira", "url":"https://drive.google.com/uc?export=download&id=1OBw5YVlxMsAoNKNT9DEj0dkZyOb2lLw7"},
	{"title": "tera hone", "url":"https://drive.google.com/uc?export=download&id=1C0z_LLbvoGR1qKM8a94fUZsHijR6NBTp"}
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
            emotion = result[0]['dominant_emotion'].lower()
        except:
            emotion = 'neutral'

        # Map emotions not in our simplified list to 'neutral'
        if emotion not in emotion_playlist:
            emotion = 'neutral'

        playlist = emotion_playlist.get(emotion, emotion_playlist['neutral'])

        os.remove(filepath)

    return render_template('index.html', emotion=emotion, playlist=playlist)

if __name__ == "__main__":
    app.run(debug=True)


