import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

from .utils import extract_text

logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self, start_url, relevance_checker, max_pages=100):
        self.start_url = start_url
        self.relevance_checker = relevance_checker
        self.max_pages = max_pages
        self.visited_urls = set()
        self.content = []

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
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        text = extract_text(html)
                        if self.relevance_checker.is_relevant(text):
                            self.content.append({'url': url, 'html': html})
                            # Only extract links if the page is relevant
                            await self._extract_links(html, url)
                        else:
                            logger.info(f'Page not relevant: {url}')
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
            # Skip non-http URLs and external domains
            if parsed_url.scheme not in ['http', 'https']:
                continue
            if urlparse(self.start_url).netloc != parsed_url.netloc:
                continue  # Skip external links
            tasks.append(self._crawl_page(full_url))
        if tasks:
            await asyncio.gather(*tasks)
