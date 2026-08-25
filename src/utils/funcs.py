from tkinter import filedialog


def buscar_arquivo():
    file_path = filedialog.askopenfilename(
        title='Selecione uma planilha',
        filetypes=[('Arquivos Excel', '*.xlsx')]
    )

    if not file_path:
        return None

    return file_path

def save_file():
    file_path = filedialog.asksaveasfilename(
        initialfile='spreadsheet_template.xlsx',
        defaultextension='.xlsx',
        filetypes=[('Arquivos Excel', '*.xlsx *.xlsm'), ('Todos os arquivos', '*.*')],
        title='Salvar modelo da planilha'
    )

    if not file_path:
        return
    
    return file_path





