# rufus/relevance_checker.py

from langchain.embeddings import OpenAIEmbeddings
import numpy as np
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

class RelevanceChecker:
    def __init__(self, extracted_topics):
        self.extracted_topics = extracted_topics
        self.embeddings_model = OpenAIEmbeddings()
        # Precompute the embedding for the extracted topics
        self.topics_embedding = self.get_embedding(' '.join(self.extracted_topics))

    def is_relevant(self, content, threshold=0.4):  # Adjusted threshold
        content_embedding = self.get_embedding(content)
        similarity = self.cosine_similarity(self.topics_embedding, content_embedding)
        return similarity >= threshold

    def get_embedding(self, text):
        return self.embeddings_model.embed_query(text)

    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# rufus/relevance_checker.py

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class LLMRelevanceChecker:
    def __init__(self, instructions, model_name='gpt-3.5-turbo'):
        self.instructions = instructions
        self.llm = ChatOpenAI(model=model_name)  # Use ChatOpenAI for chat-based models
        self.prompt_template = PromptTemplate(
            input_variables=['instructions', 'content'],
            template="""
You are an AI assistant that determines whether the given web page content is relevant to the user's instructions.

Instructions:
{instructions}

Content:
{content}

Question: Based on the instructions above, is the content relevant? Answer 'Yes' or 'No', followed by a brief explanation.

Answer:
"""
        )

    def is_relevant(self, content):
        prompt = self.prompt_template.format(instructions=self.instructions, content=content[:2000])
        response = self.llm.predict(prompt)  # Use 'predict' instead of '__call__'
        if 'Yes' in response:
            return True
        else:
            return False
