# main.py

import sys
import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# For Windows systems, adjust the event loop policy
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configure logging
logging.basicConfig(level=logging.INFO)

from rufus.instruction_parser import InstructionParser
from rufus.web_crawler import WebCrawler
from rufus.relevance_checker import RelevanceChecker
from rufus.output_aggregator import OutputAggregator
from bs4 import BeautifulSoup

async def main():
    # User inputs
    start_url = 'https://sfgov.org'
    instructions = "We're making a chatbot for the HR in San Francisco."

    # Step 1: Parse Instructions
    parser = InstructionParser()
    extracted_info = parser.parse_instructions(instructions)
    print('Extracted Information:', extracted_info)

    # Step 2: Crawl the Web
    crawler = WebCrawler(start_url, max_pages=100)
    await crawler.crawl()

    # Step 3: Check Relevance
    checker = RelevanceChecker(instructions)
    aggregator = OutputAggregator()

    for page in crawler.content:
        url = page['url']
        html = page['html']
        text = extract_text(html)
        if checker.is_relevant(text):
            aggregator.add_content(url, text)

    # Step 4: Output Results
    aggregator.save_to_files(directory='output')
    print(f'Relevant pages saved to "output" directory.')

def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Remove scripts and styles
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    text = soup.get_text(separator=' ')
    # Collapse whitespace
    import re
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if __name__ == '__main__':
    asyncio.run(main())
