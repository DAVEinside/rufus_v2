# rufus/instruction_parser.py

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os

class InstructionParser:
    def __init__(self):
        self.llm = OpenAI()
        self.prompt_template = PromptTemplate(
            input_variables=['instructions'],
            template="""
You are an AI assistant that extracts key topics and entities from user instructions to guide web content extraction.

Instructions:
{instructions}

Extracted Information:
- List of topics or entities to look for
"""
        )

    def parse_instructions(self, instructions):
        prompt = self.prompt_template.format(instructions=instructions)
        response = self.llm(prompt)
        # Simple parsing assuming the response is a list
        extracted_info = response.strip().split('\n- ')
        extracted_info = [info.strip('- ') for info in extracted_info if info.strip()]
        return extracted_info
