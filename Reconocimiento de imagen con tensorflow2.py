import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
from tkinter import Tk, filedialog
# 📌 VALIDAR EXISTENCIA DEL DATASET
dataset_path = r"C:\Users\cristian camilo gil\Desktop\PYTHON\dataset\train"
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"❌ La carpeta {dataset_path} no existe. Verifica la ruta.")
# 📌 PREPROCESAR IMAGEN PARA PREDICCIÓN
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (64, 64))  # Redimensionar
    image = image / 255.0  # Normalizar
    image = np.expand_dims(image, axis=0)  # Añadir batch dimension
    image = np.expand_dims(image, axis=-1)  # Añadir canal de color
    return image
# 📌 SELECCIONAR IMAGEN DESDE EL ORDENADOR
def select_image():
    Tk().withdraw()
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
    layers.Dense(10, activation="softmax")
])
# 📌 COMPILAR MODELO
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

# 📌 CONFIGURAR CARGA DE DATOS CON DATA AUGMENTATION
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.2
)
train_data = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(64, 64),
    color_mode="grayscale",
    batch_size=32,
    class_mode="sparse"
)
# 📌 ENTRENAR EL MODELO Y GUARDARLO
model.fit(train_data, epochs=10, batch_size=32)
model.save("modelo_digitos.h5")
# 📌 SELECCIONAR IMAGEN Y HACER PREDICCIÓN
selected_image = select_image()
if selected_image:
    processed_image = preprocess_image(selected_image)
    # Cargar el modelo entrenado
    model = keras.models.load_model("modelo_digitos.h5")    
    prediction = model.predict(processed_image)
    predicted_class = np.argmax(prediction)  

    print(f"🔢 Número detectado: {predicted_class}")
else:
    print("❌ No se seleccionó ninguna imagen.")
