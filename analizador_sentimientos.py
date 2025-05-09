import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:instruct")  # Mejor para análisis

def carga(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except IOError as e:
        print(f"Error al leer archivo: {e}")
        return None

def guardar(nombre_archivo, contenido):
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
    except IOError as e:
        print(f"Error al guardar el archivo: {e}")

def procesar_respuesta_stream(response):
    full_response = ""
    try:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                json_data = json.loads(decoded_line)
                if 'message' in json_data and 'content' in json_data['message']:
                    full_response += json_data['message']['content']
        return full_response
    except Exception as e:
        print(f"Error procesando streaming: {e}")
        return None

def analizador_sentimientos(producto):
    prompt_sistema = """Eres un analizador experto de sentimientos en reseñas de productos. 
    Analiza las reseñas y proporciona:
    1. Un resumen conciso (50 palabras máximo)
    2. Sentimiento general [Positivo/Negativo/Neutro]
    3. 3 puntos fuertes
    4. 3 áreas de mejora
    
    Formato de salida:
    Nombre del Producto: [nombre]
    Resumen: [texto]
    Sentimiento: [Positivo/Negativo/Neutro]
    Puntos fuertes:
    - [punto 1]
    - [punto 2]
    - [punto 3]
    Áreas de mejora:
    - [área 1]
    - [área 2]
    - [área 3]"""

    datos_producto = carga(f"datos/{producto}.txt")
    if not datos_producto:
        print(f"No se encontraron datos para {producto}")
        return

    print(f"Analizando: {producto}...")

    messages = [
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": datos_producto}
    ]

    try:
        # Primero intentamos sin streaming
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False,  # Forzamos modo no-streaming primero
                "options": {"temperature": 0.5}
            },
            timeout=120
        )

        if response.status_code == 200:
            respuesta_json = response.json()
            texto_respuesta = respuesta_json["message"]["content"]
        else:
            # Fallback a streaming si el modo directo falla
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": OLLAMA_MODEL,
                    "messages": messages,
                    "stream": True,
                    "options": {"temperature": 0.5}
                },
                timeout=120,
                stream=True
            )
            texto_respuesta = procesar_respuesta_stream(response)

        if texto_respuesta:
            guardar(f"datos/analisis_{producto}.txt", texto_respuesta)
            print(f"✅ Análisis completado para {producto}")
            print("-" * 50)
            print(texto_respuesta[:500] + "...")  # Muestra parte del resultado
            print("-" * 50)
        else:
            print(f"❌ No se obtuvo respuesta válida para {producto}")

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con Ollama: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    productos = [
        "evaluaciones_camisetas_algodon",
        "evaluaciones_jeans_reciclados",
        "evaluaciones_maquillaje"
    ]

    print("=== Análisis de Sentimientos de Productos ===")
    for producto in productos:
        analizador_sentimientos(producto)