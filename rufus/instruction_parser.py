# rufus/instruction_parser.py

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class InstructionParser:
    def __init__(self, model_name='gpt-3.5-turbo'):
        self.llm = ChatOpenAI(model=model_name)  # Use ChatOpenAI for chat-based models
        self.prompt_template = PromptTemplate(
            input_variables=['instructions'],
            template="""
You are an AI assistant that extracts key topics and specific keywords from user instructions to guide web content extraction.

Instructions:
{instructions}

Extracted Topics and Keywords:
- Provide a concise list of topics and keywords to look for, focusing on nouns and noun phrases relevant to the instructions.
"""
        )

    def parse_instructions(self, instructions):
        prompt = self.prompt_template.format(instructions=instructions)
        response = self.llm.predict(prompt)  # Use 'predict' instead of '__call__'
        # Parse the response into a list of keywords
        extracted_info = response.strip().split('\n- ')
        extracted_info = [info.strip('- ').lower() for info in extracted_info if info.strip()]
        return extracted_info
