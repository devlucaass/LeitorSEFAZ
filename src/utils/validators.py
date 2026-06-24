from re import match
from pathlib import Path

def valida_chave(chave):
    chave = str(chave).strip()

    return len(chave) == 44 and chave.isdigit()

def valida_celula(celula):
    celula = str(celula).strip()

    if match(r'^[A-Za-z]{1,3}[0-9]+$', celula):
        return celula.upper()

    return None

def valida_caminho_excel(caminho):
    if not caminho:
        return False
    
    arquivo = Path(caminho)
    
    return arquivo.exists() and arquivo.suffix.lower() in {'.xlsx', '.xlsm'}

def valida_nome_planilha(nome_planilha):
    return bool(nome_planilha.strip())

