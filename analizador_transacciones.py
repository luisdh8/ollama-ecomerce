import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:instruct")  # Modelo recomendado para JSON

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
        print(f"Error al guardar archivo: {e}")

def extraer_json(respuesta):
    """Intenta extraer un JSON de la respuesta, incluso si viene con texto alrededor"""
    try:
        # Primero intentamos parsear directamente
        return json.loads(respuesta)
    except json.JSONDecodeError:
        # Si falla, buscamos el JSON dentro del texto
        try:
            start = respuesta.find('{')
            end = respuesta.rfind('}') + 1
            if start != -1 and end != -1:
                return json.loads(respuesta[start:end])
        except Exception as e:
            print(f"Error extrayendo JSON: {e}")
    return None

def llamada_ollama(messages, temperature=0.7, formato_json=False):
    """Función mejorada para llamadas a la API de Ollama"""
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature}
        }
        
        if formato_json:
            payload["format"] = "json"  # Intenta forzar respuesta en JSON
            
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            respuesta = response.json()["message"]["content"]
            
            if formato_json:
                json_data = extraer_json(respuesta)
                if json_data:
                    return json_data
                else:
                    print("No se pudo extraer JSON válido de la respuesta:")
                    print(respuesta)
            return respuesta
            
        print(f"Error en la API: {response.status_code}")
        print(response.text)
        return None
        
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

def analizador_transacciones(lista_transacciones):
    print("1. Analizando transacciones en busca de posibles fraudes")
    
    prompt_sistema = """Eres un analista financiero experto en detección de fraudes. 
    Analiza estas transacciones y marca como 'Posible Fraude' aquellas que presenten:
    - Valores atípicamente altos
    - Localizaciones inconsistentes
    - Patrones temporales sospechosos
    
    Devuelve SOLO un JSON válido con este formato exacto, sin ningún otro texto alrededor:
    {
        "transacciones": [
            {
                "ID Transacción": "id",
                "Tipo de Transacción": "Crédito/Débito",
                "Establecimiento": "nombre",
                "Horario": "aaaa-mm-dd hh:mm:ss",
                "Producto": "nombre producto",
                "Ciudad - Estado": "Ciudad - Departamento (País)",
                "Valor (USD)": valor,
                "Estado": "Aprobado/Posible Fraude"
            }
        ]
    }
    """
    
    prompt_usuario = f"Transacciones a analizar (formato CSV):\n{lista_transacciones}"
    
    messages = [
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": prompt_usuario}
    ]
    
    # Forzamos formato JSON en la llamada
    respuesta = llamada_ollama(messages, temperature=0, formato_json=True)
    
    if respuesta:
        print("Análisis completado exitosamente")
        return respuesta
    else:
        print("No se pudo obtener un análisis válido")
        return None

def main():
    print("=== Sistema de Detección de Fraudes con Ollama ===")
    
    # Cargar transacciones
    transacciones = carga("datos/transacciones.csv")
    if not transacciones:
        print("No se pudieron cargar las transacciones")
        return
    
    # Analizar transacciones
    resultado = analizador_transacciones(transacciones)
    
    if resultado:
        print("\nResultado del análisis:")
        print(json.dumps(resultado, indent=2))
    else:
        print("\nNo se pudo completar el análisis")

if __name__ == "__main__":
    main()