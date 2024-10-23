import asyncio
from .instruction_parser import InstructionParser
from .web_crawler import WebCrawler
from .relevance_checker import RelevanceChecker
from .output_aggregator import OutputAggregator
from .utils import extract_text

class RufusClient:
    def __init__(self, instructions):
        self.instructions = instructions

    async def _scrape_async(self, url):
        # Step 1: Parse Instructions
        parser = InstructionParser()
        extracted_info = parser.parse_instructions(self.instructions)
        print('Extracted Information:', extracted_info)

        # Step 2: Initialize Relevance Checker and Aggregator
        checker = RelevanceChecker(self.instructions)
        aggregator = OutputAggregator()

        # Step 3: Crawl the Web
        crawler = WebCrawler(url, relevance_checker=checker, max_pages=100)
        await crawler.crawl()

        # Step 4: Collect relevant content
        for page in crawler.content:
            text = extract_text(page['html'])
            aggregator.add_content(page['url'], text)

        # Save the relevant content to the output folder
        aggregator.save_to_files(directory='output')

        return aggregator.get_output()

    def scrape(self, url):
        return asyncio.run(self._scrape_async(url))
