from re import match

# Valida a chave informada pelo usuário, garantindo que ela tenha sempre 44 dígitos.
def valida_chave(chave):
        if len(chave) == 44:
            return chave.strip()

# Valida a célula informada pelo usuário, para que atenda os padrões do Excel. 
def valida_celula(celula):
        if match(r'^[a-zA-Z]{1,3}[0-9]+$', celula):
            return str(celula).strip().upper()