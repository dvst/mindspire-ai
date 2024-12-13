# mindspire-ai

## Setup Instructions

### 1. Create a virtual environment for Python 3.11

python3.11 -m venv venv_py311
source venv_py311/bin/activate
pip install -r ../requirements.txt

playwright install chromium

# run the scripts

python scripts/scraping.py

python backend-playwright/playwright-wcag.py

# give me a summary of the project 
