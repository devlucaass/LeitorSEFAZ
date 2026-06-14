from re import match

def valida_chave(chave):
    chave = str(chave).strip()

    return len(chave) == 44 and chave.isdigit()

def valida_celula(celula):
    celula = str(celula).strip()

    if match(r'^[A-Za-z]{1,3}[0-9]+$', celula):
        return celula.upper()

    return None