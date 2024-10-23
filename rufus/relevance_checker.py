# rufus/relevance_checker.py

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

class RelevanceChecker:
    def __init__(self, instructions):
        self.instructions = instructions
        self.llm = OpenAI()
        self.prompt_template = PromptTemplate(
            input_variables=['instructions', 'content'],
            template="""
You are an AI assistant that determines whether the given web page content is relevant to the user's instructions.

Instructions:
{instructions}

Content:
{content}

Question: Is the content relevant to the instructions? Answer 'Yes' or 'No', followed by a brief explanation.

Answer:
"""
        )

    def is_relevant(self, content):
        prompt = self.prompt_template.format(instructions=self.instructions, content=content[:2000])
        response = self.llm(prompt)
        if 'Yes' in response:
            return True
        else:
            return False
