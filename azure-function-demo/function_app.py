import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
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