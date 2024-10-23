from bs4 import BeautifulSoup
import re

def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Remove scripts, styles, and unnecessary tags
    for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
        element.decompose()
    text = soup.get_text(separator=' ')
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
