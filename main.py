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
logger = logging.getLogger(__name__)

from rufus.instruction_parser import InstructionParser
from rufus.web_crawler import WebCrawler
from rufus.relevance_checker import RelevanceChecker, LLMRelevanceChecker
from rufus.output_aggregator import OutputAggregator
from bs4 import BeautifulSoup

async def main():
    # User inputs
    start_url = 'https://www.sf.gov/'
    instructions = "We're making a chatbot for jobs in San Francisco."

    # Step 1: Parse Instructions
    parser = InstructionParser()
    extracted_info = parser.parse_instructions(instructions)
    print('Extracted Topics and Keywords:', extracted_info)

    # Step 2: Crawl the Web with Focused Crawling
    crawler = WebCrawler(start_url, extracted_topics=extracted_info, max_pages=100)
    await crawler.crawl()

    # Step 3: Check Relevance with Embeddings and LLM
    embedding_checker = RelevanceChecker(extracted_topics=extracted_info)
    llm_checker = LLMRelevanceChecker(instructions)
    aggregator = OutputAggregator()

    for page in crawler.content:
        url = page['url']
        html = page['html']
        text = extract_text(html)
        summarized_text = summarize_content(text)
        if embedding_checker.is_relevant(summarized_text):
            if llm_checker.is_relevant(summarized_text):
                aggregator.add_content(url, text)
            else:
                logger.info(f'LLM determined irrelevance for {url}')
        else:
            logger.info(f'Embedding similarity too low for {url}')

    # Step 4: Output Results
    aggregator.save_to_files(directory='output')
    print(f'Relevant pages saved to \"output\" directory.')

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

def summarize_content(content):
    # For now, we will limit the content to the first 2000 characters
    # Optionally, implement a better summarization method
    return content[:2000]

if __name__ == '__main__':
    asyncio.run(main())
