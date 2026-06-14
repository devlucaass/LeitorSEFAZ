import xlwings as xw
from tkinter import messagebox
from config.config_manager import load_config

class ExcelBot:

    def __init__(self, dados):
        self.dados = dados
        self.config = load_config()
        self.caminho_excel = self.config['caminho_excel']

    def inserir_no_excel(self, celula_inicial):

        try:
            wb = xw.Book(self.caminho_excel)
            nome_aba = self.config['nome_planilha']

            try:
                ws = wb.sheets[nome_aba]

            except Exception:
                messagebox.showerror('Erro', f'A planilha "{nome_aba}" não foi encontrada.')
                return

            matriz = [
                [
                    linha['data'],
                    linha['estabelecimento'],
                    linha['produto'],
                    linha['grandeza'],
                    linha['quantidade_comprada'],
                    linha['valor_unitario'],
                    linha['quantidade'],
                    linha['valor_total']
                ]
                for linha in self.dados
            ]

            ws.range(celula_inicial).value = matriz

            wb.save()

            messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso!')

        except Exception as erro:
            messagebox.showerror('Erro', f'Ocorreu um erro:\n{erro}')