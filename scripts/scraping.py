import requests as re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_html_and_css(url):
    try:
        # Solicitar el HTML de la página
        response = re.get(url)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        
        # Obtener el contenido HTML
        html_content = response.text

        # Parsear el HTML con BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extraer todas las referencias a archivos CSS
        css_links = []
        for link in soup.find_all('link', rel='stylesheet'):
            css_url = urljoin(url, link['href'])  # Manejar rutas relativas
            css_links.append(css_url)

        # Descargar el contenido de los archivos CSS
        css_content = ""
        for css_url in css_links:
            try:
                css_response = re.get(css_url)
                css_response.raise_for_status()
                css_content += f"/* CSS file: {css_url} */\n{css_response.text}\n"
            except re.exceptions.RequestException as e:
                print(f"Error fetching CSS file {css_url}: {e}")

        return html_content, css_content

    except re.exceptions.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        return None, None

# Ejemplo de uso
if __name__ == "__main__":
    url = input("Ingresa la URL de la página web: ")
    html, css = fetch_html_and_css(url)
    
    if html:
        print("\n--- HTML Content ---\n")
        print(html[:2000])  # Muestra los primeros 1000 caracteres del HTML
        print("\n--- CSS Content ---\n")
        print(css[:2000])  # Muestra los primeros 1000 caracteres del CSS