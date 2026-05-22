import os
import pyautogui
import pandas as pd
from tkinter import messagebox
from utils.funcs import validar_planilha

class ExcelBot:

    def __init__(self, chave):
        self.caminho_csv = f'data/notas_fiscais/nf_{chave[:44]}.csv'

        if not os.path.exists(self.caminho_csv):
            messagebox.showerror('Erro', 'Arquivo CSV não encontrado. Certifique-se de que a coleta de dados foi realizada com sucesso.')
            raise FileNotFoundError(f'Arquivo {self.caminho_csv} não encontrado.')

        self.dados = pd.read_csv(self.caminho_csv)

    def celula_inicial(self, celula):
        pyautogui.hotkey('alt', 'tab')
        pyautogui.hotkey('ctrl', 'g')
        pyautogui.write(celula)
        pyautogui.press('enter')

    def inserir_no_excel(self, planilha_buscada):
        try:
            planilha_atual = validar_planilha(planilha_buscada)

            if not planilha_atual:
                return

            for dados_linha in self.dados.values:
                for valor in dados_linha:
                    pyautogui.write(str(valor))
                    pyautogui.press('tab')

                pyautogui.press('enter')

        except Exception:
            messagebox.showerror('Erro', 'Ocorreu um erro ao inserir os dados no Excel.')