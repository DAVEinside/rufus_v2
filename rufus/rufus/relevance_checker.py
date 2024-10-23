from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

class RelevanceChecker:
    def __init__(self, instructions):
        self.instructions = instructions
        self.llm = OpenAI(temperature=0)  # Set temperature to 0 for deterministic output
        self.keywords = self.extract_keywords(instructions)
        self.prompt_template = PromptTemplate(
            input_variables=['instructions', 'content'],
            template="""
You are an AI assistant that determines whether the given web page content is relevant to the user's instructions.

Instructions:
{instructions}

Content:
{content}

Question: Is the content relevant to the instructions? Answer 'Yes' or 'No' only.

Answer:
"""
        )

    def extract_keywords(self, instructions):
        # Simple keyword extraction, todo : apply more sofiscated keyword extraction techniques
        return [word.lower() for word in instructions.split() if len(word) > 3]

    def is_relevant(self, content):
        # Pre-filter using keywords
        content_lower = content.lower()
        if not any(keyword in content_lower for keyword in self.keywords):
            logger.info('Content does not contain any keywords; skipping LLM check.')
            return False

        # Proceed with LLM check
        prompt = self.prompt_template.format(
            instructions=self.instructions, content=content[:2000]
        )
        response = self.llm(prompt).strip()
        logger.info(f'LLM Response: {response}')
        return response.lower().startswith('yes')
