import cv2
import subprocess
from pyzbar import pyzbar
from openpyxl import Workbook
from utils.validators import valida_chave
from tkinter import messagebox, filedialog

def abrir_configuracoes():
    subprocess.Popen(['notepad.exe', 'src/config/settings.json'])

def salvar_arquivo():
    caminho = filedialog.asksaveasfilename(
        initialfile='modelo_planilha.xlsx',
        defaultextension='.xlsx',
        filetypes=[('Arquivos Excel', '*.xlsx'), ('Todos os arquivos', '*.*')],
        title='Salvar modelo da planilha'
    )

    if not caminho:
        return
    
    return caminho

def gerar_modelo_planilha():
    wb = Workbook()

    ws = wb.active
    ws.title = 'CONSOLIDADO - COMPRAS'

    colunas = ['DATA', 'ESTABELECIMENTO', 'PRODUTO', 'GRANDEZA', 'QUANTIDADE P/ PRODUTO', 'VALOR UNITÁRIO', 'QUANTIDADE', 'TOTAL']

    ws.append(colunas)

    caminho = salvar_arquivo()

    if not caminho:
        return
    
    wb.save(caminho)

    messagebox.showinfo('Sucesso', 'Modelo da planilha criado com sucesso!')


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

if __name__ == '__main__':
    abrir_configuracoes()
    