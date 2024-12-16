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

def get_chat_completion(prompt, language, model=chat_model, temperature=0, max_tokens=200, frequency_penalty=0):
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

if __name__ == "__main__":
    prompt = "Analiza la accesibilidad de esta página."
    language = "spanish"
    response = get_chat_completion(prompt, language, temperature=0, max_tokens=200)
    print(response)
