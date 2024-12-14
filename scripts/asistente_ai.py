import openai
import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

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

def get_chat_completion(prompt, model=chat_model, temperature=0, max_tokens=200, frequency_penalty=0):
    #messages = [{"role": "user", "content": prompt}]

    messages = [
        {
            "role": "system",
            "content": """
            Solo puedes responder con un formato JSON válido. No puedes usar ningún tipo de formato de texto. 
            Eres un agente fiscalizador de accesibilidad de páginas web que cumple con todas las normas de WCAG: Web Content Accessibility Guideline 
            Devuelve un reporte en formato JSON con las siguientes reglas:
            1. Si se encuentra algún problema de accesibilidad, genera un reporte detallado con la estructura siguiente:
            {
            "report": {
                "issues": [
                {
                    "description": "",   // Breve descripción del problema de accesibilidad encontrado.
                    "suggestion": "",    // Sugerencia específica para solucionar el problema.
                    "code_suggestion": "",  // Fragmento de código recomendado como solución.
                    "code_fragment": ""  // Fragmento del código analizado que presenta el problema.
                }
                ]
            }
            2. Aqui hay un ejemplo de un reporte de accesibilidad válido:
            {
            "report": {
                "issues": [
                {
                    "description": "El enlace de la página de inicio no es accesible por teclado",
                    "suggestion": "Agrega un enlace de accesibilidad a la página de inicio",
                    "code_suggestion": "<a href="https://www.example.com" tabindex="0">Inicio</a>",
                    "code_fragment": "<a href="https://www.example.com">Inicio</a>"
                }
                ]
            }
            """,
        },
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        engine=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty,
        #top_p = 1.0    #Es mejor usar o bien temperature o bien top_p
    )
    return response.choices[0].message["content"]

if __name__ == "__main__":
    messages =  f"""
    Cuéntame un chiste
    """
    response = get_chat_completion(messages, temperature = 0, max_tokens=200)
    print(response)


'''

        prompt = f"""
            {json.dumps(web_content)}

            Eres un agente fiscalizador de accesibilidad de páginas web que cumple con todas las normas de WCAG (Web Content Accessibility Guidelines). 
            Analiza el HTML y CSS descritos y devuelve un reporte en formato JSON con las siguientes reglas:

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
            }}

            2. Si no se detectan problemas de accesibilidad en el análisis, devuelve un JSON vacío: {{}}.

            Asegúrate de que el JSON generado sea válido y procesable, y enfoca las recomendaciones en cumplir con los criterios de éxito de nivel A y AA de WCAG.
            """
'''