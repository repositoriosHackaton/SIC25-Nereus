from flask import Flask, render_template, request, send_from_directory
from ultralytics import YOLO
import os
import cv2
import numpy as np  
from PIL import Image

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
UPLOAD_FOLDER = "static/uploads"
PROCESSED_FOLDER = "static/processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# MODELO IA ENTRENADO CON TUMORES CEREBRALES
model = YOLO("tumordetector.pt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/upload", methods=["POST"]) 
def upload_file():
    if "file" not in request.files:
        return "No file part", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    return {"filename": file.filename}

@app.route("/process", methods=["POST"])
def process_image():
    data = request.get_json()
    filename = data.get("filename")
    if not filename:
        return "No filename provided", 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Realizar predicción
    result_predict = model.predict(source=filepath, imgsz=(640))
    
    # Procesar imagen de salida
    plot = result_predict[0].plot()
    plot = cv2.cvtColor(plot, cv2.COLOR_BGR2RGB)
    processed_image = Image.fromarray(plot)
    
    processed_path = os.path.join(PROCESSED_FOLDER, "processed_" + filename)
    processed_image.save(processed_path)

    return {"processed_image": f"/processed/processed_{filename}"}

@app.route("/processed/<filename>")
def get_processed_image(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

# Solo un bloque para ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
