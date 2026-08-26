from tkinter import filedialog


def select_file():
    return filedialog.askopenfilename(
        title='Selecione uma planilha',
        filetypes=[('Arquivos Excel', '*.xlsx')]
    )

def save_file():
    return filedialog.asksaveasfilename(
        initialfile='spreadsheet_template.xlsx',
        defaultextension='.xlsx',
        filetypes=[('Arquivos Excel', '*.xlsx *.xlsm'), ('Todos os arquivos', '*.*')],
        title='Salvar modelo da planilha'
    )





