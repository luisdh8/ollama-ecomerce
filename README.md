# Ollama E-commerce Analytics

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python framework leveraging Ollama API for advanced e-commerce analytics including product classification, sentiment analysis, and fraud detection - optimized for sustainable e-commerce businesses.

## Overview

The Ollama E-commerce Analytics System processes various e-commerce data points to:
- Classify sustainable products
- Analyze customer sentiment from reviews
- Detect fraudulent transactions
- Optimize model selection based on computational needs

## Features

### Core Modules
- **Product Classification**: AI-powered categorization into custom categories
- **Review Analysis**: Sentiment extraction and key insights from customer feedback
- **Transaction Analysis**: Fraud pattern detection in financial data
- **Model Management**: Dynamic model selection based on workload

### Advanced Capabilities
- Batch processing for large datasets
- Customizable analysis parameters
- JSON-formatted outputs for integration
- Local model support via Ollama

## System Architecture

```mermaid
graph TD
    A[Data Sources] --> B[Core System]
    B --> C[Analysis Modules]
    C --> D[Ollama API]
    D --> E[Results]
    
    A -->|Product Reviews| C
    A -->|Transaction Data| C
    A -->|Product Listings| C
    
    subgraph Analysis Modules
    C --> F[Review Analysis]
    C --> G[Transaction Analysis]
    C --> H[Product Classification]
    end
```

## Prerequisites

- Python 3.8+
- Ollama installed locally ([installation guide](https://ollama.ai/))
- Required models (automatically pulled on first run):
  - `llama3:instruct`
  - `mistral`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/luisdh8/ollama-ecomerce.git
cd ollama-ecomerce
```

2. Set up environment:
```bash
cp .env.example .env
```
3. Edit the `.env` file with your preferences:
```ini
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:instruct
```

## Usage

### Core Functionality

```python
from analytics.review_analyzer import analyze_sentiment

results = analyze_sentiment("datos/reviews_producto.txt")
print(results)
```

### Product Classification
```bash
python clasificador.py
```
Interactive mode:
1. Enter categories (comma-separated)
2. Input product names
3. Get instant classification

### Transaction Analysis
```bash
python analizador_transacciones.py datos/transacciones.csv
```

### Review Analysis
```bash
python analizador_sentimientos.py
```

## Module Documentation

### `clasificador.py`
- `clasifica_productos(nombre_producto, categorias)`: Classifies products
- Interactive mode with category suggestions

### `analizador_transacciones.py`
- `analizar_transacciones(archivo_csv)`: Processes transaction files
- Outputs JSON with fraud flags

### `analizador_sentimientos.py`
- `analizar_sentimiento(texto_review)`: Performs sentiment analysis
- Identifies strengths/weaknesses

## Data Structure

```
.
├── contador_tokens.py
├── seleccion_modelo.py
├── analizador_sentimientos.py
├── clasificador.py
├── analizador_transacciones.py
├── main.py
├── datos/
│   ├── lista-compra-300-clientes.csv
│   ├── evaluaciones_camisetas_algodon.txt
│   ├── evaluaciones_jeans_reciclados.txt
│   ├── evaluaciones_maquillaje.txt
│   ├── analisis_evaluaciones_camisetas_algodon.txt
│   ├── analisis_evaluaciones_jeans_reciclados.txt
│   └── analisis_evaluaciones_maquillaje.txt
```

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Ollama team for the powerful local AI platform
- Open-source community for sustainable commerce tools
- Early adopters for valuable feedback
```
