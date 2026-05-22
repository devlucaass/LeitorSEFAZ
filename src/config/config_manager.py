import json

def load_config():
    with open('src/config/settings.json', 'r', encoding='utf-8') as file:
        return json.load(file)  