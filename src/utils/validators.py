from re import match

def valida_chave(chave):
        if len(chave) == 44:
            return chave.strip()

def valida_celula(celula):
        if match(r'^[a-zA-Z]{1,3}[0-9]+$', celula):
            return str(celula).strip().upper()