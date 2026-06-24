import json
from tkinter import messagebox

CAMINHO_CONFIG = 'src/config/settings.json'

def load_config():
    try:
        with open(CAMINHO_CONFIG, 'r', encoding='utf-8') as file:
            return json.load(file)
        
    except Exception:
        messagebox.showerror('Erro', 'Arquivo de configuração com erros. Verifique e tente novamente.')
        return {}
    
def save_config(caminho_excel, nome_planilha):
    config = {
        'caminho_excel': caminho_excel,
        'nome_planilha': nome_planilha
    }
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)
    
