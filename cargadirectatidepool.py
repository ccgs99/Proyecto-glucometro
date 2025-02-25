import requests
import json

# 1. Credenciales de usuario
TIDEPOOL_USERNAME = "cgil86@uan.edu.co"
TIDEPOOL_PASSWORD = "1056805669"
API_URL = "https://api.tidepool.org"

# 2. Autenticación en la API de Tidepool
def get_auth_token():
    headers = {
        "Content-Type": "application/json",
        "x-tidepool-session-token": "",
    }
    payload = json.dumps({
        "username": TIDEPOOL_USERNAME,
        "password": TIDEPOOL_PASSWORD
    })

    response = requests.post(f"{API_URL}/auth/login", headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.headers["x-tidepool-session-token"]
    else:
        raise Exception("Error de autenticación en Tidepool")

# 3. Subir datos de glucosa
def upload_glucose_data(value, timestamp):
    token = get_auth_token()
    
    headers = {
        "Content-Type": "application/json",
        "x-tidepool-session-token": token
    }
    
    data = {
        "type": "cbg",  # Continuous Blood Glucose
        "value": value,  # Nivel de glucosa en mg/dL
        "units": "mg/dL",
        "time": timestamp,  # Formato ISO 8601: "2025-01-29T14:00:00Z"
        "deviceId": "manual-upload-python"
    }
    
    response = requests.post(f"{API_URL}/data", headers=headers, json=[data])
    
    if response.status_code == 200:
        print("✅ Datos subidos correctamente a Tidepool.")
    else:
        print(f"❌ Error al subir los datos: {response.text}")