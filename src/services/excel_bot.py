import xlwings as xw
from config.config_manager import load_config

class ExcelBot:

    def __init__(self, data):
        self.data = data
        self.config = load_config()
        self.excel_path = self.config['excel_path']

    def insert_data(self, start_cell):
        try:
            wb = self._open_workbook()
            ws = self._get_worksheet(wb)
            excel_values = self._prepare_excel_values()

            ws.range(start_cell).value = excel_values

            wb.save()
            
        except Exception as e:
            print(f"Erro ao inserir dados no Excel: {e}")

    def _open_workbook(self):
        return xw.Book(self.excel_path)

    def _get_worksheet(self, wb):
        sheet_name = self.config['sheet_name']
        return wb.sheets[sheet_name]

    def _prepare_excel_values(self):
        return [
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


