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
            "code_fragment": '<img src="image.jpg">'
        },
        {
            "description": "Contraste insuficiente entre el texto y el fondo",
            "code_fragment": '<div style="color: #eee; background-color: #fff;">Texto de ejemplo</div>'
        },
        {
            "description": "Elemento interactivo sin descripción significativa",
            "code_fragment": '<button></button>'
        }
    ]
    
    return func.HttpResponse(
        body=json.dumps(accessibility_issues),
        mimetype="application/json",
        status_code=200
    )