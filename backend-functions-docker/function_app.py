import azure.functions as func
import datetime
import json
import logging

# playwright is a Python library to automate Chromium, Firefox and WebKit with a single API.
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# openai is a Python library to interact with the OpenAI API.
import openai
import os

app = func.FunctionApp()

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:

        # get url from form-data, x-www-form-urlencoded, raw body or query params
        url = req.form.get('url') or req.params.get('url') or req.get_json().get('url') or req.form.get('url')
        language = req.form.get('language') or req.params.get('language') or req.get_json().get('language') or req.form.get('language')
    except Exception as e:
        logging.error(f"Error 27: {e}")
        return func.HttpResponse(
            "Error3: La solicitud debe contener un campo 'url'.",
            status_code=400
        )

    API_KEY = os.getenv("OPENAI_API_KEY")
    assert API_KEY, "ERROR: Azure OpenAI Key is missing"
    openai.api_key = API_KEY

    RESOURCE_ENDPOINT = os.getenv("OPENAI_API_BASE", "").strip()
    assert RESOURCE_ENDPOINT, "ERROR: Azure OpenAI Endpoint is missing"
    assert "openai.azure.com" in RESOURCE_ENDPOINT.lower(), "ERROR: Azure OpenAI Endpoint should be in the form: \n\n\t<your unique endpoint identifier>.openai.azure.com"

    openai.api_base = RESOURCE_ENDPOINT
    openai.api_type = os.getenv("OPENAI_API_TYPE")
    openai.api_version = os.getenv("OPENAI_API_VERSION")

    chat_model = os.getenv("CHAT_MODEL_NAME")


    def inject_axe_core(page):
        page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.0/axe.min.js")
        
    def check_basic_accessibility(page):
        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        def check_images(soup):
            images = soup.find_all('img')
            issues = []
            for img in images:
                if not img.get('alt'):
                    issues.append({
                        "description": "Texto alternativo faltante en la imagen",
                        "code_fragment": str(img)
                    })
                return issues

        return check_images(soup) #+ check_headings(soup)

    def run_axe_analysis(page):
        results = page.evaluate("""
            () => {
                return new Promise((resolve) => {
                    axe.run().then(results => resolve(results));
                });
            }
        """)
        return results
    
    def gather_violations(results):
        issues = []
        for violation in results.get('violations', []):
            for node in violation['nodes']:
                issues.append({
                    "description": violation['description'],
                    "code_fragment": node['html']
                })
        return issues

    def check_wcag(url):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            page.wait_for_load_state('networkidle')
            
            inject_axe_core(page)

            basic_issues = check_basic_accessibility(page)
            axe_results = run_axe_analysis(page)
            axe_issues = gather_violations(axe_results)

            issues = basic_issues + axe_issues

            report = {
                "report": {
                    "issues": issues
                }
            }

            print(json.dumps(report, indent=4))

            browser.close()

            return json.dumps(report, indent=4)
        
    def get_chat_completion_1(prompt, language, model=chat_model, temperature=0, max_tokens=200, frequency_penalty=0):
        messages = [
            {
                "role": "system",
                "content": f"""
                Solo puedes responder con un formato JSON válido. No puedes usar ningún tipo de formato de texto. 
                Eres un agente fiscalizador de accesibilidad de páginas web que cumple con todas las normas de WCAG: Web Content Accessibility Guideline 
                Devuelve un reporte en formato JSON con las siguientes reglas:
                1. Si se encuentra algún problema de accesibilidad, genera un reporte detallado con la estructura siguiente:
                {{
                "report": {{
                    "issues": [
                    {{
                        "description": "",   // Breve descripción del problema de accesibilidad encontrado.
                        "suggestion": "",    // Sugerencia específica para solucionar el problema.
                        "code_suggestion": "",  // Fragmento de código recomendado como solución.
                        "code_fragment": ""  // Fragmento del código analizado que presenta el problema.
                    }}
                    ]
                }}
                2. Aqui hay un ejemplo de un reporte de accesibilidad válido:
                {{
                "report": {{
                    "issues": [
                    {{
                        "description": "El enlace de la página de inicio no es accesible por teclado",
                        "suggestion": "Agrega un enlace de accesibilidad a la página de inicio",
                        "code_suggestion": "<a href='https://www.example.com' tabindex='0'>Inicio</a>",
                        "code_fragment": "<a href='https://www.example.com'>Inicio</a>"
                    }}
                    ]
                }}
                3. Debes recorrer cada caso de accesibilidad que te indicaré en el prompt y generar un reporte con un tipo de cada caso de accesibilidad. 
                4. Si no se detectan problemas de accesibilidad en el análisis, devuelve un JSON vacío: {{}}
                5. El idioma en el que debes realizar el reporte es: {language}
                """,
            },
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            engine=model,
            messages=messages,
            temperature=temperature, 
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty
        )
        return response.choices[0].message["content"]

    def get_chat_summary(reporte, language, model=chat_model, temperature=0, max_tokens=200, frequency_penalty=0):
        messages = [
            {
                "role": "system",
                "content": f"""
                Solo puedes responder con un formato JSON válido. No puedes usar ningún tipo de formato de texto. 
                Eres un agente fiscalizador de accesibilidad de páginas web que cumple con todas las normas de WCAG: Web Content Accessibility Guideline 
                Devuelve un reporte en formato JSON con las siguientes reglas:
                1. Debes revisar el reporte de accesibilidad que el usuario proporcionará y genera un resumen breve enfatizando al sector de población que ayudaría a mejorar la accesibilidad de la página siguiendo el siguiente formato:
                {{
                "summary": {{
                    "population": "",   // Descripción del sector de población con posibles problemas de accesibilidad.
                }}
                2. El resumen debe ser de 100 palabras como máximo.
                3. El resumen debe ser breve y conciso.
                4. El idioma en el que debes realizar esta tarea es: {language}
                """,
            },
            {"role": "user", "content": reporte}
        ]
        response = openai.ChatCompletion.create(
            engine=model,
            messages=messages,
            temperature=temperature, 
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty
        )
        return response.choices[0].message["content"]
        
    try:
        logging.info(f"Analizando la página: {url}")
        hallazgos = check_wcag(url)
        
    except Exception as e:
        logging.error(f"Error 197: {e}")
        return func.HttpResponse(
            "Error en hallazgos",
            status_code=500
        )
    
    try:
        correcciones = get_chat_completion_1(hallazgos, language, temperature=0, max_tokens=10000)
        correcciones_dict = json.loads(correcciones)

    except Exception as e:
        logging.error(f"Error en correcciones: {e}")
        return func.HttpResponse(
            "Error en correcciones",
            status_code=500
        )
    
    try:
        resumen = get_chat_summary(correcciones, language, temperature=0, max_tokens=200)
        resumen_dict = json.loads(resumen)  
    except Exception as e:
        logging.error(f"Error en resumen: {e}")
        return func.HttpResponse(
            "Error en resumen",
            status_code=500
        )
    
    try:
        if 'summary' in resumen_dict:
            correcciones_dict["summary"] = resumen_dict["summary"]
        else:
            correcciones_dict["summary"] = {}

        unified_response = correcciones_dict

        return func.HttpResponse(
            json.dumps(unified_response, indent=4),
            status_code=200
        )
    
    except Exception as e:
        logging.error(f"Error en unified_response: {e}")
        return func.HttpResponse(
            "Error en unified_response",
            status_code=500
        )


