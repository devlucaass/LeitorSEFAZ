import xlwings as xw
from config.config_manager import load_config

class ExcelBot:

    def __init__(self, data):
        self.data = data
        self.config = load_config()
        self.excel_path = self.config['excel_path']

    def insert_data(self, start_cell):
        try:
            wb = xw.Book(self.excel_path)
            sheet_name = self.config['sheet_name']

            ws = wb.sheets[sheet_name]

            excel_values = [
                [
                    row['date'],
                    row['establishment_name'],
                    row['product'],
                    row['unit'],
                    row['purchased_quantity'],
                    row['unit_price'],
                    row['quantity'],
                    row['total_price']
                ]
                for row in self.data
            ]

            ws.range(start_cell).value = excel_values

            wb.save()
            
        except Exception as e:
            print(f"Erro ao inserir dados no Excel: {e}")