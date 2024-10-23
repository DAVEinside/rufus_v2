# rufus/web_crawler.py

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self, start_url, extracted_topics, max_pages=100):
        self.start_url = start_url
        self.extracted_topics = extracted_topics  # New parameter
        self.max_pages = max_pages
        self.visited_urls = set()
        self.content = []
        self.semaphore = asyncio.Semaphore(10)  # Limit concurrency

    async def crawl(self):
        await self._crawl_page(self.start_url)
    
    async def _crawl_page(self, url):
        if len(self.visited_urls) >= self.max_pages:
            return
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        logger.info(f'Crawling: {url}')

        try:
            async with self.semaphore:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            html = await response.text()
                            self.content.append({'url': url, 'html': html})
                            await self._extract_links(html, url)
                        else:
                            logger.warning(f'Failed to retrieve {url}: Status {response.status}')
        except Exception as e:
            logger.error(f'Error retrieving {url}: {e}')

    async def _extract_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        tasks = []
        for link_tag in soup.find_all('a', href=True):
            href = link_tag['href']
            href = href.strip()
            if href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                continue
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)
            # Skip non-http URLs
            if parsed_url.scheme not in ['http', 'https']:
                continue
            # Estimate link relevance
            link_text = link_tag.get_text(separator=' ').lower()
            if self.is_relevant_link(link_text, full_url):
                tasks.append(self._crawl_page(full_url))
        if tasks:
            await asyncio.gather(*tasks)

    def is_relevant_link(self, link_text, url):
        # Check if any extracted topic is in the link text or URL
        for topic in self.extracted_topics:
            if topic in link_text or topic in url.lower():
                return True
        return False
