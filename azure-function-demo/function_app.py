import azure.functions as func
import logging
import json
import re
from urllib.parse import urlparse

def is_valid_gov_domain(url):
    """Validate if URL is a valid government domain."""
    try:
        # List of government TLDs (including non-US countries)
        gov_tlds = {
            'gov',      # United States
            'gob',      # Spain, Argentina, Mexico
            'gouv',     # France
            'gov.uk',   # United Kingdom
            'gc.ca',    # Canada
            'gov.au',   # Australia
            'gob.mx',   # Mexico
            'gov.br',   # Brazil
            'gov.it',   # Italy
            'gov.in',   # India
            'gov.de',   # Germany
            'gov.jp'    # Japan
        }

        # Parse the URL
        parsed_url = urlparse(url)
        
        # Ensure scheme is present
        if not parsed_url.scheme:
            return False
            
        # Get domain and check if it ends with any government TLD
        domain = parsed_url.netloc.lower()
        return any(domain.endswith('.' + tld) for tld in gov_tlds)

    except Exception:
        return False

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get URL from POST request
    try:
        req_body = req.get_json()
        url_submitted = req_body.get('url')
        if not url_submitted:
            return func.HttpResponse(
                "Please pass a URL in the request body",
                status_code=400
            )
        
        # Validate if it's a government domain
        if not is_valid_gov_domain(url_submitted):
            return func.HttpResponse(
                "Invalid URL. Please provide a valid government domain URL",
                status_code=400
            )

    except ValueError:
        return func.HttpResponse(
            "Please pass a valid JSON in the request body",
            status_code=400
        )

    accessibility_issues = [
        {
            "description": "Texto alternativo faltante en la imagen",
            "code_fragment": '<img src="image.jpg">',
            "suggestion": "Agrega un enlace de accesibilidad a la página de inicio",
            "code_suggestion": "<a href=\"https://www.example.com\" tabindex=\"0\">Inicio</a>",
        },
        {
            "description": "Contraste insuficiente entre el texto y el fondo",
            "code_fragment": '<div style="color: #eee; background-color: #fff;">Texto de ejemplo</div>',
            "suggestion": "Agrega un enlace de accesibilidad a la página de inicio",
            "code_suggestion": "<a href=\"https://www.example.com\" tabindex=\"0\">Inicio</a>",
        },
        {
            "description": "Elemento interactivo sin descripción significativa",
            "code_fragment": '<button></button>',
            "suggestion": "Agrega un enlace de accesibilidad a la página de inicio",
            "code_suggestion": "<a href=\"https://www.example.com\" tabindex=\"0\">Inicio</a>",
        }
    ]
    
    return func.HttpResponse(
        body=json.dumps(accessibility_issues),
        mimetype="application/json",
        status_code=200
    )