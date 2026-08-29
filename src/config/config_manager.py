import json
from pathlib import Path

from config.constants import BROWSER_NAME_KEY, EXCEL_PATH_KEY, SHEET_NAME_KEY


class ConfigManager:
    SETTINGS_PATH = Path(__file__).parent / "settings.json"

    @classmethod
    def load_config(cls) -> dict:
        try:
            with cls.SETTINGS_PATH.open("r", encoding="utf-8") as file:
                config = json.load(file)

            if isinstance(config, dict):
                return config

            return {}

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @classmethod
    def save_config(cls, excel_path: str, sheet_name: str, browser_name: str) -> bool:
        config = {
            EXCEL_PATH_KEY: excel_path,
            SHEET_NAME_KEY: sheet_name,
            BROWSER_NAME_KEY: browser_name.lower()
        }

        try:
            with cls.SETTINGS_PATH.open("w", encoding="utf-8") as file:
                json.dump(config, file, indent=4, ensure_ascii=False)

            return True

        except OSError:
            return False
