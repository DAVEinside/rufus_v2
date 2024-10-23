import json
import os

class OutputAggregator:
    def __init__(self):
        self.relevant_content = []

    def add_content(self, url, content):
        self.relevant_content.append({'url': url, 'content': content})

    def get_output(self):
        return self.relevant_content

    def save_to_files(self, directory='output'):
        os.makedirs(directory, exist_ok=True)
        for idx, item in enumerate(self.relevant_content):
            filename = f'page_{idx+1}.json'
            filepath = os.path.join(directory, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False, indent=2)
