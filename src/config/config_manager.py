import json
from tkinter import messagebox

def load_config():
    try:
        with open('src/config/settings.json', 'r', encoding='utf-8') as file:
            return json.load(file)
        
    except Exception:
        messagebox.showerror('Erro', 'Arquivo de configuração com erros. Verifique e tente novamente.')
        return {}
      
    
    
