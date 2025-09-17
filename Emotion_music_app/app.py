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
        "music/pehla_nasha.mp3",
        "music/tujhe_dekha.mp3",
	"music/badtameez_dil.mp3",
	"music/ilahi.mp3"
    ],
    'sad': [
        "music/channa_mereya.mp3",
        "music/tum_hi_ho.mp3",
	"music/dooriyan.mp3"
    ],
    'angry': [
        "music/saadda_haq.mp3",
        "music/bulleya.mp3"
    ],
    'surprise': [
        "music/ek_ladki.mp3"
    ],
    'neutral': [
        "music/ae_mere_humsafar.mp3",
	"music/kabira.mp3",
	"music/tera hone.mp3"
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
