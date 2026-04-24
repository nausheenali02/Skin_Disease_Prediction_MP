import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = FastAPI(title="Skin Disease Classifier API")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Mount the static folder to serve CSS and JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Load the trained model
MODEL_PATH = 'Super_DenseNet_82.keras'
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")

CLASS_NAMES = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((256, 256))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# 3. Routes to serve your HTML files
@app.get("/")
async def serve_index():
    return FileResponse('static/index.html')

@app.get("/upload.html")
async def serve_upload():
    return FileResponse('static/upload.html')

# 4. The Prediction API
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        image_bytes = await file.read()
        processed_image = preprocess_image(image_bytes)
        predictions = model.predict(processed_image)
        
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))

        return {
            "filename": file.filename,
            "prediction": CLASS_NAMES[predicted_class_idx],
            "confidence": round(confidence * 100, 2),
            "probabilities": {
                CLASS_NAMES[i]: round(float(predictions[0][i]) * 100, 2)
                for i in range(len(CLASS_NAMES))
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# 5. The block that allows 'python3 app.py' to work
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
