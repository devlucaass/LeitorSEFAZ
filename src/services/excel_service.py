import os
import pyautogui
import pandas as pd
from tkinter import messagebox
from utils.funcs import validar_planilha

class ExcelBot:

    # Inicializa a classe, recebendo a chave como parâmetro para conseguir carregar os dados do CSV gerado pela coleta de dados.
    def __init__(self, chave):
        self.caminho_csv = f'data/notas_fiscais/nf_{chave[:44]}.csv'

        # Verifica se o arquivo CSV existe. Se não existir, exibe uma mensagem de erro e interrompe a execução.
        if not os.path.exists(self.caminho_csv):
            messagebox.showerror('Erro', 'Arquivo CSV não encontrado. Certifique-se de que a coleta de dados foi realizada com sucesso.')
            raise FileNotFoundError(f'Arquivo {self.caminho_csv} não encontrado.')

        self.dados = pd.read_csv(self.caminho_csv)

    # Utiliza um atalho do Excel para acessar a célula inicial informada pelo usuário, onde os dados serão inseridos. Isso servirá de norte para a inserção dos dados, que ocorrerá de forma sequencial a partir dessa célula.
    def celula_inicial(self, celula):
        pyautogui.hotkey('alt', 'tab')
        pyautogui.hotkey('ctrl', 'g')
        pyautogui.write(celula)
        pyautogui.press('enter')

    # Insere os dados na planilha, linha por linha, utilizando a tecla 'tab' para navegar entre as colunas e 'enter' para passar para a próxima linha demarcada pela célula inicial.
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