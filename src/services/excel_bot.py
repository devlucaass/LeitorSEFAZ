import os

import xlwings as xw
from openpyxl import Workbook, load_workbook

from config.config_manager import ConfigManager
from utils.file_dialog import save_file


class ExcelBot:
    def __init__(self, data):
        self.data = data

    def insert_data(self, excel_cell):
        wb = self._open_workbook()
        ws = self._get_worksheet(wb)
        excel_values = self._prepare_excel_values()

        ws.range(excel_cell).value = excel_values

        wb.save()

    @staticmethod
    def create_spreadsheet_template():
        excel_path = save_file()

        if not excel_path:
            return

        if os.path.exists(excel_path):
            wb = load_workbook(excel_path)
            ws = wb.active

        else:
            wb = Workbook()
            ws = wb.active
            ws.title = ConfigManager.load_config()['sheet_name']


        ExcelBot._create_columns(ws)
        wb.save(excel_path)


    @staticmethod
    def _create_columns(ws):
        columns = [
            "DATA",
            "ESTABELECIMENTO",
            "PRODUTO",
            "GRANDEZA",
            "QUANTIDADE P/ PRODUTO",
            "VALOR UNITÁRIO",
            "QUANTIDADE",
            "TOTAL",
        ]

        for column, value in enumerate(columns, start=1):
            ws.cell(row=1, column=column, value=value)

    def _open_workbook(self):
        return xw.Book(ConfigManager.load_config()['excel_path'])

    def _get_worksheet(self, wb):
        return wb.sheets[ConfigManager.load_config()['sheet_name']]

    def _prepare_excel_values(self):
        return [
            [
                row["date"],
                row["establishment_name"],
                row["product"],
                row["unit"],
                row["purchased_quantity"],
                row["unit_price"],
                row["quantity"],
                row["total_price"],
            ]
            for row in self.data
        ]



