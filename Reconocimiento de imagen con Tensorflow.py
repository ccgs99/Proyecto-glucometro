import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
from tkinter import Tk, filedialog

# 📌 FUNCIÓN PARA PREPROCESAR IMÁGENES
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Escala de grises
    image = cv2.resize(image, (64, 64))  # Redimensionar a 64x64
    image = image / 255.0  # Normalizar
    image = np.expand_dims(image, axis=0)  # Agregar batch dimension
    image = np.expand_dims(image, axis=-1)  # Agregar canal de color
    return image

# 📌 SELECCIONAR IMAGEN DESDE EL ORDENADOR
def select_image():
    Tk().withdraw()  # Ocultar ventana de Tkinter
    file_path = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Imágenes", "*.jpg;*.jpeg;*.png")])
    return file_path

# 📌 DEFINIR MODELO CNN PARA RECONOCER DÍGITOS
model = keras.Sequential([
    layers.Conv2D(32, (3,3), activation="relu", input_shape=(64, 64, 1)),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64, (3,3), activation="relu"),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dense(10, activation="softmax")  # 10 clases (dígitos 0-9)
])

# 📌 COMPILAR MODELO
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

model.summary()

# 📌 CONFIGURAR CARGA DE DATOS
dataset_path = r"C:\Users\cristian camilo gil\Desktop\PYTHON\dataset\train"

train_datagen = ImageDataGenerator(rescale=1./255)  # Normalizar imágenes

train_data = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(64, 64),
    color_mode="grayscale",
    batch_size=32,
    class_mode="sparse"
)

# 📌 ENTRENAR EL MODELO
model.fit(train_data, epochs=10, batch_size=32)

# 📌 SELECCIONAR IMAGEN Y HACER PREDICCIÓN
selected_image = select_image()
if selected_image:
    processed_image = preprocess_image(selected_image)
    
    prediction = model.predict(processed_image)
    predicted_class = np.argmax(prediction)  # Obtener la clase con mayor probabilidad
    
    print(f"🔢 Número detectado: {predicted_class}")
else:
    print("❌ No se seleccionó ninguna imagen.")
