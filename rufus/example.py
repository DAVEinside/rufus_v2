import os
from dotenv import load_dotenv
import logging
import asyncio
import sys
import io

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# For Windows systems, adjust the event loop policy
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Set stdout to handle Unicode encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from rufus import RufusClient

instructions = "We're making a chatbot for the HR in San Francisco."
client = RufusClient(instructions)
documents = client.scrape("https://www.sf.gov/")

for doc in documents:
    print(f"URL: {doc['url']}")
    print(f"Content: {doc['content']}\n")
