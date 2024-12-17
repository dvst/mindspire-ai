from flask import Flask, request, jsonify
import subprocess
import json
from scripts.asistente_ai import get_chat_completion, get_chat_completion_1, get_chat_summary # Script 2
from  backend_playwright.playwright_wcag import check_wcag # Script 1
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_page():
    # 1. Recibir la URL del frontend
    try:
        data = request.get_json()
        print(data)
        if not data or 'url' not in data or 'language' not in data:
            return jsonify({'first_error': 'JSON with "url" and "language" is required'}), 400
        url = data['url']
        language = data['language']
    except Exception as e:
        return jsonify({'second_error': 'Invalid JSON format'}), 400

    # Verificar si la URL pertenece a una página gubernamental
    if not ('.gov' in url or '.gob' in url):
        return jsonify({'fifth_error_url': 'URL does not belong to a governmental website'}), 400


    # 2. Ejecutar el script de análisis de accesibilidad
    try:
        hallazgos = check_wcag(url)  # Script 1
    except Exception as e:
        return jsonify({'third_error': str(e)}), 500

    # 3. Pasar los hallazgos al script de Azure OpenAI

    try:
        correcciones = get_chat_completion_1(hallazgos, language, temperature=0, max_tokens=10000)
        print("Correcciones response:", correcciones)  # Debug: Check the raw response
        correcciones_dict = json.loads(correcciones)
    except json.JSONDecodeError as e:
        return jsonify({'error_parse_correcciones': f'Failed to parse correcciones JSON: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'fourth_error_reporte': str(e)}), 500

    try:
        resumen = get_chat_summary(correcciones, language, temperature=0, max_tokens=200)
        print("Resumen response:", resumen)  # Debug: Check the raw response
        resumen_dict = json.loads(resumen)
    except json.JSONDecodeError as e:
        return jsonify({'error_parse_resumen': f'Failed to parse resumen JSON: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error_summary': str(e)}), 500

    try:
        if 'summary' in resumen_dict:
            correcciones_dict['summary'] = resumen_dict['summary']
        else:
            correcciones_dict['summary'] = {}

        unified_response = correcciones_dict
    except Exception as e:
        return jsonify({'error_unificado': str(e)}), 500

    #######################
    correcciones_dict_f = json.loads(correcciones)
    # 4. Devolver las correcciones al frontend
    #return jsonify(correcciones_dict_f), 200
    return jsonify(unified_response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
