from flask import Flask, request, jsonify
import subprocess
import json
from scripts.asistente_ai import get_chat_completion # Script 2
from  backend_playwright.playwright_prueba import analizar_pagina_web # Script 1
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_page():
    '''
    # 1. Recibir la URL del frontend
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'JSON with "url" is required'}), 400
        url = data['url']
    except Exception as e:
        return jsonify({'error': 'Invalid JSON format'}), 400

    # 2. Ejecutar el script de análisis de accesibilidad
    try:
        hallazgos = analizar_pagina_web(url)  # Script 1
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # 3. Pasar los hallazgos al script de Azure OpenAI
    '''
    hallazgos = analizar_pagina_web()


    try:
        correcciones = get_chat_completion(hallazgos)  # Script 2
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # 4. Devolver las correcciones al frontend
    return jsonify(correcciones), 200

if __name__ == '__main__':

    app.run(debug=True)