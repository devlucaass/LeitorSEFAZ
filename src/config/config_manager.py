import json
from pathlib import Path


class ConfigManager:

    SETTINGS_PATH = Path(__file__).parent / 'settings.json'

    @staticmethod
    def load_config():
        try:
            with open(ConfigManager.SETTINGS_PATH, 'r', encoding='utf-8') as file:
                return json.load(file)
            
        except Exception as e:
            print(f"Erro ao carregar o arquivo de configuração: {e}.")
            return {}
        
    @staticmethod
    def save_config(excel_path, sheet_name):
        config = {
            'excel_path': excel_path,
            'sheet_name': sheet_name,
        }
        
        with open(ConfigManager.SETTINGS_PATH, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4, ensure_ascii=False)
