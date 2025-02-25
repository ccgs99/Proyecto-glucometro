#carga de imagenes desde archivos
import tkinter as tk
from tkinter import filedialog

def seleccionar_imagen():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    archivo = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")]
    )
    return archivo

imagen_path = seleccionar_imagen()
print("Imagen seleccionada:", imagen_path)

from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def procesar_imagen(imagen_path):
    img = Image.open(imagen_path)
    img = img.convert("L")  # Escala de grises
    img = ImageEnhance.Contrast(img).enhance(2)  # Aumentar contraste
    img = img.filter(ImageFilter.SHARPEN)  # Aumentar nitidez
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)  # Duplicar tamaño para mejorar OCR

    texto = pytesseract.image_to_string(img, config="--psm 6 digits")  # Detectar solo números
    numeros = re.findall(r'\d+', texto)  # Extraer solo los números
    return numeros[0] if numeros else "Error"

valor_glucosa = procesar_imagen(imagen_path)
print("Valor detectado:", valor_glucosa)

#--------------------------------- LOGIN TIDEPOOL
import requests

TIDEPOOL_LOGIN_URL = "https://api.tidepool.org/auth/login"

def iniciar_sesion_tidepool(email, password):
    headers = {"Content-Type": "application/json"}
    datos = {"username": email, "password": password}

    response = requests.post(TIDEPOOL_LOGIN_URL, json=datos, headers=headers)
    
    if response.status_code == 200:
        token = response.headers.get("x-tidepool-session-token")
        print("Autenticación exitosa!")
        return token
    else:
        print("Error al iniciar sesión:", response.text)
        return None

# Solicitar credenciales al usuario
email = input("Ingrese su email de Tidepool: ")
password = input("Ingrese su contraseña de Tidepool: ")
TIDEPOOL_AUTH_TOKEN = iniciar_sesion_tidepool(email, password)

#--------------------CARGA DE DATOS TIDEPOOL
TIDEPOOL_API_URL = "https://api.tidepool.org/data"

def enviar_a_tidepool(valor_glucosa, url_imagen, token):
    datos = {
        "type": "cbg",
        "value": float(valor_glucosa),
        "units": "mg/dL",
        "image_url": url_imagen
    }

    headers = {
        "Content-Type": "application/json",
        "x-tidepool-session-token": token
    }

    response = requests.post(TIDEPOOL_API_URL, json=datos, headers=headers)

    if response.status_code == 200:
        print("Datos enviados a Tidepool con éxito!")
    else:
        print("Error al enviar:", response.text)

if TIDEPOOL_AUTH_TOKEN:
    enviar_a_tidepool(valor_glucosa, "URL_DE_LA_IMAGEN", TIDEPOOL_AUTH_TOKEN)
