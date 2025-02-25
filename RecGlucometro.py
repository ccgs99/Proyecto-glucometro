import cv2
import numpy as np
import pytesseract
import pandas as pd
import os
import requests
from datetime import datetime

# Ruta de Tesseract (cambiar según tu instalación)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows

# 📌 1. Función para Preprocesar Imagen
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convierte a escala de grises
    img = cv2.GaussianBlur(img, (5, 5), 0)  # Suaviza la imagen
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Binarización
    return img

# 📌 2. Función para Extraer Texto con OCR
def extract_glucose_value(image_path):
    processed_img = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_img, config='--psm 6')  # OCR en modo texto suelto
    return text.strip()  # Limpia espacios en blanco

# 📌 3. Función para Guardar Resultados en CSV
def save_to_csv(patient_id, glucose_value):
    filename = r"C:\Users\cristian camilo gil\Desktop\PYTHON\prueba2\glucose_readings.csv"
    data = {
        "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Paciente": [patient_id],
        "Glucosa (mg/dL)": [glucose_value]
    }
    df = pd.DataFrame(data)
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)  # Agrega nueva fila
    else:
        df.to_csv(filename, index=False)  # Crea archivo

# 📌 4. Función para Subir Datos a la Nube (Ejemplo con API de Tidepool)
def upload_to_tidepool(patient_id, glucose_value):
    url = "https://api.tidepool.org/data"
    headers = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}
    payload = {
        "patient_id": patient_id,
        "glucose": glucose_value,
        "timestamp": datetime.now().isoformat()
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("✅ Datos subidos a Tidepool correctamente")
    else:
        print("❌ Error al subir los datos:", response.text)

# 📌 5. Programa Principal
if __name__ == "__main__":
    image_path = r"C:\Users\cristian camilo gil\Desktop\PYTHON\prueba2\glucometer_screen.jpg"  # Ruta de la imagen
    patient_id = "Paciente_001"

    if not os.path.exists(image_path):
        print(f"❌ La imagen {image_path} no existe. Captura una nueva.")
    else:
        glucose_value = extract_glucose_value(image_path)
        if glucose_value:
            print(f"📊 Valor de glucosa detectado: {glucose_value} mg/dL")
            save_to_csv(patient_id, glucose_value)  # Guarda en CSV
            upload_to_tidepool(patient_id, glucose_value)  # Opcional: subir a la nube
        else:
            print("⚠️ No se pudo detectar un valor de glucosa en la imagen.")
