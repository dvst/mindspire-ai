from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

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

    def check_headings(soup):
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        issues = []
        prev_level = 0
        for h in headings:
            curr_level = int(h.name[1])
            if curr_level > prev_level + 1:
                issues.append({
                    "description": "Nivel de encabezado omitido",
                    "code_fragment": str(h)
                })
            prev_level = curr_level
        return issues

    return check_images(soup) + check_headings(soup)

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

if __name__ == "__main__":
    url = "https://data.seattle.gov/"
    check_wcag(url)