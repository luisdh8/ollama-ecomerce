import os
import requests
from dotenv import load_dotenv
try:
    from transformers import AutoTokenizer
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_MODEL_ALT = "llama3:instruct"

# Modelos públicos alternativos que no requieren autenticación
PUBLIC_MODELS = {
    "llama3": "hf-internal-testing/llama-tokenizer",
    "llama3:instruct": "hf-internal-testing/llama-tokenizer",
    "mistral": "mistralai/Mistral-7B-v0.1",
    "llama2": "meta-llama/Llama-2-7b-hf"
}

def contar_tokens_api(texto, modelo):
    """Cuenta tokens usando la API de Ollama"""
    endpoints = ["/api/generate", "/api/chat"]  # Probamos ambos endpoints
    
    for endpoint in endpoints:
        url = f"{OLLAMA_BASE_URL}{endpoint}"
        payload = {
            "model": modelo,
            "prompt": texto,
            "stream": False,
            "options": {"temperature": 0}
        } if endpoint == "/api/generate" else {
            "model": modelo,
            "messages": [{"role": "user", "content": texto}],
            "stream": False,
            "options": {"temperature": 0}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("eval_count", 0) + data.get("prompt_eval_count", 0)
        except Exception:
            continue
    
    return 0

def contar_tokens_local(texto, modelo):
    """Cuenta tokens localmente usando modelos públicos"""
    if not HF_AVAILABLE:
        return 0
    
    model_name = PUBLIC_MODELS.get(modelo, "hf-internal-testing/llama-tokenizer")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return len(tokenizer.encode(texto))
    except Exception as e:
        print(f"\nError en tokenizador local ({model_name}): {str(e)}")
        return 0

def contar_tokens(texto, modelo):
    """Función principal que combina ambos métodos"""
    # Intento con API primero
    count = contar_tokens_api(texto, modelo)
    if count > 0:
        return count
    
    # Fallback a tokenizador local
    return contar_tokens_local(texto, modelo)

def mostrar_resultados(modelo, texto, num_tokens):
    """Muestra resultados formateados"""
    print(f"\nModelo: {modelo}")
    print(f"Número de tokens: {num_tokens}")
    print(f"Método: {'API' if num_tokens > 0 else 'Local (fallback)'}")
    print("-" * 50)

if __name__ == "__main__":
    texto_prompt = """Eres un categorizador de productos.
Debes asumir las categorías presentes en la lista a continuación.
# Lista de Categorías Válidas
1. Cat 1
2. Cat 2
3. Cat 3
# Formato de Salida
Producto: Nombre del Producto
Categoría: presenta la categoría del producto
# Ejemplo de Salida
Producto: Cepillo de dientes con carga solar
Categoría: Electrónicos Verdes"""

    print("\n=== Contador de Tokens para Ollama ===")
    print("Texto a analizar:")
    print(texto_prompt[:200] + "...\n")

    # Contar tokens para ambos modelos
    modelos = [OLLAMA_MODEL, OLLAMA_MODEL_ALT]
    
    for modelo in modelos:
        num_tokens = contar_tokens(texto_prompt, modelo)
        mostrar_resultados(modelo, texto_prompt, num_tokens)

    if not HF_AVAILABLE:
        print("\nNOTA: Para conteo local de tokens, instala transformers:")
        print("pip install transformers")