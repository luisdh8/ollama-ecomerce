import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_MODEL_ALT = "llama3:instruct"  # Modelo alternativo para casos de alta carga

def carga(nombre_archivo):
    """
    Carga el contenido de un archivo
    """
    try:
        with open(nombre_archivo, "r", encoding='utf-8') as archivo:
            return archivo.read()
    except IOError as e:
        print(f"Error al leer archivo: {e}")
        return ""

def contar_tokens(texto, modelo):
    """
    Versión mejorada para contar tokens usando el endpoint de generación
    """
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": modelo,
        "prompt": texto,
        "stream": False,
        "options": {"temperature": 0}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get("eval_count", 0) + data.get("prompt_eval_count", 0)
    except Exception as e:
        print(f"Error al contar tokens: {str(e)}")
    
    return 0

def generate_completion(messages, modelo, max_tokens=2048):
    """
    Versión mejorada que maneja streaming de respuesta
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": modelo,
        "messages": messages,
        "stream": False,  # Desactivamos streaming para simplificar
        "options": {
            "num_predict": max_tokens,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en la API: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error en generate_completion: {str(e)}")
    
    return None

def main():
    # Definir prompts
    prompt_sistema = """Identifique el perfil de compra de cada cliente
    El formato de salida debe ser:
    cliente - describa el perfil del cliente en 3 palabras"""

    prompt_usuario = carga("datos/lista-compra-300-clientes.csv")
    
    if not prompt_usuario:
        print("No se pudo cargar el archivo de datos")
        return

    # Contar tokens (versión mejorada)
    numero_tokens_entrada = contar_tokens(prompt_sistema + prompt_usuario, OLLAMA_MODEL)
    print(f"\nModelo base: {OLLAMA_MODEL}")
    print(f"Tokens de entrada estimados: {numero_tokens_entrada}")

    # Definir límites y selección de modelo
    tokens_salida = 2048
    limite_tokens_modelo = 8000  # Límite conservador para llama3
    
    modelo_seleccionado = OLLAMA_MODEL
    if numero_tokens_entrada + tokens_salida >= limite_tokens_modelo:
        modelo_seleccionado = OLLAMA_MODEL_ALT
        print(f"\nCambiando a modelo alternativo: {modelo_seleccionado}")

    # Generar respuesta
    messages = [
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": prompt_usuario}
    ]

    print("\nGenerando respuesta...")
    respuesta = generate_completion(messages, modelo_seleccionado, tokens_salida)

    # Procesar respuesta
    if respuesta and "message" in respuesta:
        print("\nResultado:")
        print(respuesta["message"]["content"])
    else:
        print("\nNo se obtuvo una respuesta válida.")

if __name__ == "__main__":
    main()