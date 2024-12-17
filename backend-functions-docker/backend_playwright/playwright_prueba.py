import json
def analizar_pagina_web():
    issues = [
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

    report = {
        "report": {
            "issues": issues
        }
    }
    
    return json.dumps(report, indent=4)

# Llamar a la función y mostrar el JSON generado
if __name__ == "__main__":
    print(analizar_pagina_web())