from pathlib import Path
from re import fullmatch


class Validators:
    @staticmethod
    def validate_access_key(access_key):
        access_key = str(access_key).strip()

        if fullmatch(r"\d{44}", access_key):
            return access_key

        return False

    @staticmethod
    def validate_excel_cell(excel_cell):
        excel_cell = str(excel_cell).strip()

        if fullmatch(r"[A-Za-z]{1,3}[0-9]+", excel_cell):
            return excel_cell.upper()

        return False

    @staticmethod
    def validate_excel_path(excel_path):
        if not excel_path:
            return False

        file = Path(excel_path)

        return file.exists() and file.suffix.lower() in {".xlsx", ".xlsm"}

    @staticmethod
    def validate_sheet_name(sheet_name):
        return bool(sheet_name.strip())
