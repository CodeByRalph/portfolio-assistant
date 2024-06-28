from dotenv import load_dotenv
import os
import json
from pinecone import Pinecone, ServerlessSpec
import openai
from pprint import pprint

load_dotenv()

# API Authorization
openai.api_key = os.getenv('OPENAI_API_KEY')
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

# Connecting to Pinecone Index
index = pc.Index('portfolio-assistant')

# Opening Data file
with open('Data/json/combined_cleaned.json', 'r') as file:
    data = [ json.loads(line) for line in file ]

def extract_text(data):
    text_items = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                text_items.extend(extract_text(value))
            else:
                text_items.append(str(value))
    elif isinstance(data, list):
        for item in data:
            text_items.extend(extract_text(item))
    return text_items

text_data = extract_text(data)
text_data = [text for text in text_data if text.strip()] # Removes empty strings if any


def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model='text-embedding-ada-002'	
    )

    return response.data[0].embedding

get_embedding('Hello World')