# utils.py
import json
from langchain_core.prompts import PromptTemplate

def load_prompt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return PromptTemplate.from_template(data['template'])
