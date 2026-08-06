import cv2
from pyzbar import pyzbar
from openpyxl import Workbook
from utils.validators import valida_chave
from tkinter import messagebox, filedialog

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

from openpyxl import Workbook
from tkinter import messagebox

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
        messagebox.showinfo("Sucesso", "Modelo da planilha criado com sucesso!")
    except PermissionError:
        messagebox.showerror("Arquivo em uso", "Feche a planilha antes de gerar o modelo.")


# Lê QRCodes e retorna seu valor em string.
def ler_qrcode():
    cam = cv2.VideoCapture(0)

    try:
        while True:
            resultado, frame = cam.read()

            if not resultado:
                break

            qrcodes = pyzbar.decode(frame)

            for qr in qrcodes:
                url = qr.data.decode('utf-8')
                chave = url.split('p=')[-1].split('|')[0]

                if valida_chave(chave):
                    return url

                messagebox.showwarning('Erro', f'QR Code inválido: {url}')
                return False

            cv2.imshow('Leitor de QRCode', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        return False

    finally:
        cam.release()
        cv2.destroyAllWindows()
