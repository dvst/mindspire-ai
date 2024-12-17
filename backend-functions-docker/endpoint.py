from flask import Flask, request, jsonify
import subprocess
import json
from scripts.asistente_ai import get_chat_completion # Script 2
from  backend_playwright.playwright_wcag import check_wcag # Script 1
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_page():
    
    # 1. Recibir la URL del frontend
    try:
        data = request.get_json()
        if not data or 'url' not in data or 'language' not in data:
            return jsonify({'first_error': 'JSON with "url" and "language" is required'}), 400
        url = data['url']
        language = data['language']
    except Exception as e:
        return jsonify({'second_error': 'Invalid JSON format'}), 400

    # Verificar si la URL pertenece a una página gubernamental
    if not ('.gov' in url or '.gob' in url):
        return jsonify({'error': 'URL does not belong to a governmental website'}), 400

    # 2. Ejecutar el script de análisis de accesibilidad
    try:
        hallazgos = check_wcag(url)  # Script 1
    except Exception as e:
        return jsonify({'third_error': str(e)}), 500

    # 3. Pasar los hallazgos al script de Azure OpenAI
    
    #hallazgos = check_wcag()


    try:
        correcciones = get_chat_completion(hallazgos, language, temperature = 0, max_tokens=2000)  # Script 2
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # 4. Devolver las correcciones al frontend
    return jsonify(correcciones), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
