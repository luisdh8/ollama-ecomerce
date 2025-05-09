import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
print(f"Usando URL: {OLLAMA_BASE_URL}")
print(f"Usando modelo: {OLLAMA_MODEL}")

def generate_completion(messages):
    """
    Genera una respuesta utilizando Ollama API
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"
    
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }
    
    print(f"Enviando solicitud a: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"Código de estado: {response.status_code}")
        
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e}")
                print(f"Respuesta recibida: {response.text[:200]}...")
                return {"message": {"content": "Error al procesar la respuesta de Ollama."}}
        else:
            print(f"Error: {response.status_code}")
            print(f"Respuesta: {response.text[:200]}...")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None

# Definir los mensajes
messages = [
    {
        "role": "system",
        "content": "Eres un asistente de un e-commerce de productos sustentable, cuando te pidan productos devuelve solo el nombre sin considerar la descripción"
    },
    {
        "role": "user",
        "content": "Liste 3 productos sustentables"
    }
]

# Obtener la respuesta
print("Generando respuesta...")
response = generate_completion(messages)

# Imprimir el contenido de la respuesta
if response:
    print("\nRespuesta completa recibida:")
    print(json.dumps(response, indent=2, ensure_ascii=False)[:500])
    
    if isinstance(response, dict) and "message" in response:
        print("\nContenido de la respuesta:")
        print(response["message"]["content"])
    elif isinstance(response, dict) and "response" in response:
        # Formato alternativo de respuesta de Ollama
        print("\nContenido de la respuesta:")
        print(response["response"])
    else:
        print("\nNo se pudo extraer el contenido de la respuesta con el formato esperado.")
        print("Estructura de la respuesta:")
        print(type(response))
        if isinstance(response, dict):
            print("Claves disponibles:", list(response.keys()))
else:
    print("No se obtuvo una respuesta válida.")