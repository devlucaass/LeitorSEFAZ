from tkinter import filedialog

from openpyxl import Workbook


def buscar_arquivo():
    caminho = filedialog.askopenfilename(
        title='Selecione uma planilha',
        filetypes=[('Arquivos Excel', '*.xlsx')]
    )

    if not caminho:
        return None

    return caminho

def salvar_arquivo():
    caminho = filedialog.asksaveasfilename(
        initialfile='modelo_planilha.xlsx',
        defaultextension='.xlsx',
        filetypes=[('Arquivos Excel', '*.xlsx *.xlsm'), ('Todos os arquivos', '*.*')],
        title='Salvar modelo da planilha'
    )

    if not caminho:
        return
    
    return caminho

def gerar_modelo_planilha():
    wb = Workbook()

    ws = wb.active
    ws.title = 'CONSOLIDADO - COMPRAS'

    colunas = [
        'DATA',
        'ESTABELECIMENTO',
        'PRODUTO',
        'GRANDEZA',
        'QUANTIDADE P/ PRODUTO',
        'VALOR UNITÁRIO',
        'QUANTIDADE',
        'TOTAL'
    ]

    ws.append(colunas)

    caminho = salvar_arquivo()

    if not caminho:
        return

    try:
        wb.save(caminho)
        print("Sucesso")
    except PermissionError:
        print("Arquivo em uso")



