
# Rufus

**Rufus** is an intelligent web crawler designed to extract and synthesize relevant web content based on user-defined instructions. It helps engineers quickly build structured documents from websites, which can be seamlessly integrated into Retrieval-Augmented Generation (RAG) pipelines.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Components Overview](#components-overview)
  - [RufusClient](#rufusclient)
  - [InstructionParser](#instructionparser)
  - [RelevanceChecker](#relevancechecker)
  - [WebCrawler](#webcrawler)
  - [OutputAggregator](#outputaggregator)
  - [Utils](#utils)
- [Configuration](#configuration)
- [Advanced Usage](#advanced-usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Intelligent Crawling**: Crawls websites based on user-defined instructions and extracts only relevant content.
- **Instruction Parsing**: Uses an LLM to parse user instructions and extract key topics.
- **Relevance Checking**: Determines the relevance of web pages using a combination of keyword matching and LLM-based analysis.
- **Structured Output**: Aggregates the relevant content into structured documents for easy integration into RAG systems.
- **Customizable**: Components can be customized or extended to fit specific use cases.

## Installation

You can install Rufus via `pip`:

```bash
pip install Rufus
```

## Quick Start

Here's how to use Rufus in your project:

```python
from rufus import RufusClient

instructions = "Find information about product features and customer FAQs."
client = RufusClient(instructions)
documents = client.scrape("https://example.com")

for doc in documents:
    print(f"URL: {doc['url']}")
    print(f"Content: {doc['content']}
")
```

## Components Overview

### RufusClient

The main interface for users. It orchestrates the entire process:

- **Initialization**: Accepts user instructions.
- **Scrape Method**: Takes a starting URL and returns relevant documents.

**Usage**:

```python
client = RufusClient(instructions)
documents = client.scrape("https://example.com")
```

### InstructionParser

Parses user instructions to extract key topics or entities that guide the crawling and relevance checking processes.

- **Method**: `parse_instructions(instructions)`
- **Output**: List of extracted topics/entities.

**Usage**:

```python
parser = InstructionParser()
extracted_info = parser.parse_instructions(instructions)
```

### RelevanceChecker

Determines whether a web page's content is relevant to the user's instructions.

- **Initialization**: Accepts instructions to extract keywords.
- **Method**: `is_relevant(content)`
- **Process**:
  - Pre-filters content using keyword matching.
  - Uses an LLM to make a final relevance decision.

**Usage**:

```python
checker = RelevanceChecker(instructions)
is_relevant = checker.is_relevant(content)
```

### WebCrawler

Performs the web crawling, guided by the relevance checker to focus on relevant pages.

- **Initialization**:
  - `start_url`: The URL to start crawling from.
  - `relevance_checker`: An instance of `RelevanceChecker`.
  - `max_pages`: Maximum number of pages to crawl.
- **Method**: `crawl()`
- **Attributes**:
  - `content`: List of dictionaries containing 'url' and 'html' of relevant pages.

**Usage**:

```python
crawler = WebCrawler(start_url, relevance_checker=checker, max_pages=100)
await crawler.crawl()
```

### OutputAggregator

Collects and stores the relevant content extracted by the crawler.

- **Methods**:
  - `add_content(url, content)`: Adds a page to the aggregator.
  - `get_output()`: Returns the aggregated content.
  - `save_to_files(directory)`: Saves the content to JSON files.

**Usage**:

```python
aggregator = OutputAggregator()
aggregator.add_content(url, content)
documents = aggregator.get_output()
aggregator.save_to_files(directory='output')
```

### Utils

Contains utility functions used across the application.

- **Function**: `extract_text(html_content)`
  - Extracts and cleans text from HTML content.

**Usage**:

```python
from rufus.utils import extract_text
text = extract_text(html_content)
```

## Configuration

### Environment Variables

Rufus relies on OpenAI's LLMs via the `langchain` library. You need to set up your OpenAI API key:

1. Install `python-dotenv` if you haven't:

   ```bash
   pip install python-dotenv
   ```

2. Create a `.env` file in your project directory:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Adjusting LLM Parameters

You can adjust the LLM's temperature or other parameters in the `RelevanceChecker` and `InstructionParser` classes by modifying the `OpenAI` instance initialization.

```python
self.llm = OpenAI(temperature=0)  # For deterministic responses
```

## Advanced Usage

### Custom Relevance Checking

You can extend or modify the `RelevanceChecker` to use embeddings or other methods for determining relevance.

### Extending the Crawler

You can subclass `WebCrawler` to override methods like `_crawl_page` or `_extract_links` to customize crawling behavior.

### Handling Large Websites

For large websites, consider adjusting `max_pages` or implementing additional logic to prioritize certain sections.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## Running the Example

Create a Python script `example.py`:

```python
from rufus import RufusClient

instructions = "Find information about product features and customer FAQs."
client = RufusClient(instructions)
documents = client.scrape("https://example.com")

for doc in documents:
    print(f"URL: {doc['url']}")
    print(f"Content: {doc['content']}
")
```

Run the script:

```bash
python example.py
```
