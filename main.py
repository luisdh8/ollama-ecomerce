from dotenv import load_dotenv
import os
import requests
import json
import time

# Cargar variables de entorno
load_dotenv()

# Configuración de Ollama desde .env
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODELO = os.getenv("OLLAMA_MODEL", "llama3")

def cargar(nombre_del_archivo):
    """Carga el contenido de un archivo de texto"""
    try:
        with open(nombre_del_archivo, "r", encoding="utf-8") as archivo:
            datos = archivo.read()
            return datos
    except IOError as e:
        print(f"Error al leer el archivo: {e}")
        return None

def llamar_ollama(prompt_sistema, prompt_usuario):
    """Función para enviar peticiones a la API de Ollama"""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    
    # Combinamos los prompts para enviarlos a Ollama
    prompt_completo = f"{prompt_sistema}\n\n{prompt_usuario}"
    
    payload = {
        "model": MODELO,
        "prompt": prompt_completo,
        "stream": False
    }
    
    print(f"Enviando solicitud a Ollama con el modelo {MODELO}...")
    inicio = time.time()
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            fin = time.time()
            tiempo_total = round(fin - inicio, 2)
            print(f"Respuesta recibida en {tiempo_total} segundos")
            return response.json()["response"]
        else:
            print(f"Error en la solicitud: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error al llamar a Ollama: {e}")
        print("\nAsegúrate de que Ollama esté en ejecución con: 'ollama serve'")
        print(f"Y verifica que el modelo '{MODELO}' esté descargado con: 'ollama list'")
        return None

def main():
    # Definir el prompt del sistema
    prompt_sistema = """
    Identifique el perfil de compra para cada cliente a continuación.
    
    El formato de salida debe ser:
    
    cliente - describe el perfil del cliente en 3 palabras
    """
    
    # Ruta del archivo CSV
    ruta_archivo = "datos/lista-compra-300-clientes.csv"
    
    # Cargar los datos
    prompt_usuario = cargar(ruta_archivo)
    
    if not prompt_usuario:
        print(f"No se pudo cargar el archivo: {ruta_archivo}")
        return
    
    # Verificar longitud del CSV
    print(f"Tamaño del archivo CSV: {len(prompt_usuario)} caracteres")
    
    # Llamar a Ollama y obtener respuesta
    respuesta = llamar_ollama(prompt_sistema, prompt_usuario)
    
    if respuesta:
        print("\nRESULTADO DEL ANÁLISIS:")
        print("-" * 40)
        print(respuesta)
        
        # Guardar resultado en un archivo
        with open("resultado_analisis.txt", "w", encoding="utf-8") as archivo:
            archivo.write(respuesta)
        print("\nResultado guardado en 'resultado_analisis.txt'")
    else:
        print("No se pudo obtener una respuesta de Ollama")

if __name__ == "__main__":
    main()