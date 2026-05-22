import pyautogui
import pandas as pd
from utils.funcs import validar_planilha

class ExcelBot:

    # Inicializa a classe, recebendo a chave como parâmetro para garantir o carregamento da Nota Fiscal.
    def __init__(self, chave):
        self.dados = pd.read_csv(f'data/notas_fiscais/nf_{chave[:44]}.csv')
    
    # Garante que esteja na célula correta para iniciar a inserção dos dados.
    def celula_inicial(self, celula):
        pyautogui.hotkey('alt', 'tab')
        pyautogui.hotkey('ctrl', 'g')
        pyautogui.write(celula)
        pyautogui.press('enter')
    
    # Insere os dados na planilha, iteirando sobre cada linha da Nota Fiscal extraída.
    def inserir_no_excel(self, planilha_buscada):
        planilha_atual = validar_planilha(planilha_buscada)
        if planilha_atual:
            for linha in self.dados.values:
                for valor in linha:
                    pyautogui.write(str(valor))
                    pyautogui.press('tab')

                pyautogui.press('enter')