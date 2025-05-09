import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

def generate_completion(messages, temperatura=1, max_tokens=200):
    """
    Genera una respuesta utilizando Ollama API
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"
    
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "options": {
            "temperature": temperatura,
            "num_predict": max_tokens
        },
        "stream": False  # Asegurarnos de que no sea streaming
    }
    
    response = requests.post(url, json=payload)
    print("Respuesta cruda del servidor:", response.text)  # Imprimir la respuesta cruda
    
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            print("Error al decodificar JSON:", e)
            return None
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def clasifica_productos(nombre_producto, lista_categorias):
    """
    Clasifica un producto en una de las categorías especificadas
    """
    prompt_sistema = f"""    
    Eres un categorizador de productos.
    Debes asumir las categorías presentes en la lista a continuación.
    # Lista de Categorías Válidas
    {lista_categorias.split(",")}
    # Formato de Salida
        Producto: Nombre del Producto
        Categoría: presenta la categoría del producto
    # Ejemplo de Salida
        Producto: Cepillo de dientes con carga solar
        Categoría: Electrónicos Verdes
    """
    
    messages = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": nombre_producto
        }
    ]
    
    respuesta = generate_completion(messages, temperatura=1, max_tokens=200)
    
    if respuesta and "message" in respuesta:
        return respuesta["message"]["content"]
    else:
        return "Error al clasificar el producto."

# Ejecución principal
if __name__ == "__main__":
    categorias = input("Liste las categorias separadas por una coma: ")
    
    while True:
        producto = input("Ingrese el nombre del producto a clasificar (o 'salir' para terminar): ")
        
        if producto.lower() == 'salir':
            break
            
        texto_resultado = clasifica_productos(producto, categorias)
        print(texto_resultado)
        print("-" * 50)