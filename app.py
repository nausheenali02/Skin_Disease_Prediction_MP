import os
import io
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.preprocessing import image

# Initialize Flask with the static folder path
app = Flask(__name__, static_folder='static')

# --- CONFIGURATION ---
# Ensure this file is in the same directory as app.py
MODEL_PATH = 'Master_OOD_Model.keras' 
IMG_SIZE = (224, 224)

# Labels match your 8-class training (7 HAM10000 classes + 1 NOT_MEDICAL)
CLASS_LABELS = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'not_medical', 'nv', 'vasc']

# Load model once at startup - Utilizing your M1 GPU (Metal)
print("🚀 Loading Model...")
model = tf.keras.models.load_model(MODEL_PATH)

# --- FRONTEND ROUTES ---

@app.route('/')
def index():
    """Serves the landing page (index.html)."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload.html')
def upload_page():
    """Serves the upload page (upload.html)."""
    return send_from_directory(app.static_folder, 'upload.html')

# --- API ROUTES ---

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    try:
        # 1. Read file bytes and wrap in BytesIO 
        # This fixes the FileStorage path error on macOS/M1
        img_bytes = file.read()
        img = image.load_img(io.BytesIO(img_bytes), target_size=IMG_SIZE)
        
        # 2. Preprocess the image
        img_array = image.img_to_array(img)
        # Rescale matching your training logic: rescale=1./255
        img_array = np.expand_dims(img_array, axis=0) / 255.0 
        
        # 3. Run Prediction
        predictions = model.predict(img_array)
        class_idx = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        
        # 4. Return JSON formatted for your upload.js
        return jsonify({
            'prediction': CLASS_LABELS[class_idx],
            'confidence': round(confidence * 100, 2),
            'probabilities': {CLASS_LABELS[i]: float(predictions[0][i]) for i in range(len(CLASS_LABELS))}
        })

    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
