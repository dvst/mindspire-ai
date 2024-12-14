# create a playwright script to check the wcag compliance of a website received by a url

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://data.seattle.gov"
# use axe-core to check the wcag compliance of the website
def inject_axe_core(page):
    # Inject axe-core from CDN
    page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.0/axe.min.js")

def check_basic_accessibility(page):
    # Use BeautifulSoup to analyze page content
    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Basic accessibility checks
    def check_images():
        images = soup.find_all('img')
        issues = []
        for img in images:
            if not img.get('alt'):
                issues.append(f"Image missing alt text: {img}")
        return issues
    
    def check_headings():
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        issues = []
        prev_level = 0
        for h in headings:
            curr_level = int(h.name[1])
            if curr_level > prev_level + 1:
                issues.append(f"Heading level skipped: {h}")
            prev_level = curr_level
        return issues
    
    page.evaluate("window.accessibilityIssues = {}")
    page.evaluate(f"window.accessibilityIssues.images = {check_images()}")
    page.evaluate(f"window.accessibilityIssues.headings = {check_headings()}")

def run_axe_analysis(page):
    # Run axe analysis and get results
    results = page.evaluate("""
        () => {
            return new Promise((resolve) => {
                axe.run().then(results => resolve(results));
            });
        }
    """)
    return results

def print_violations(results):
    violations = results.get('violations', [])
    if not violations:
        print("No accessibility violations found!")
        return
        
    print(f"\nFound {len(violations)} accessibility violations:")
    for violation in violations:
        print(f"\nRule violated: {violation['id']}")
        print(f"Impact: {violation['impact']}")
        print(f"Description: {violation['description']}")
        print(f"Help: {violation['help']}")
        print("Affected elements:")
        for node in violation['nodes']:
            print(f"- {node['html']}")

def check_wcag(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(10000)

        # Inject axe-core and run analysis
        inject_axe_core(page)
        check_basic_accessibility(page)
        results = run_axe_analysis(page)
        print_violations(results)

        browser.close()

if __name__ == "__main__":
    check_wcag(url)
