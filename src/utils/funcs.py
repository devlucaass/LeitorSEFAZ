import os
import cv2
import pyautogui
import pyperclip
from pyzbar import pyzbar
from openpyxl import Workbook
from utils.validators import valida_chave
from tkinter import messagebox, filedialog
from config.config_manager import load_config

config = load_config()

pyautogui.PAUSE = config['sleep']

# Copia o nome de planilha em foco
def copiar_foco():
    pyautogui.press('alt')
    pyautogui.press('c')
    pyautogui.press('o')
    pyautogui.press('r')
    pyautogui.hotkey('ctrl', 'c')
    planilha_em_foco = pyperclip.paste()
    pyautogui.press('esc')

    return planilha_em_foco.strip()

# Verifica se a planilha correta está em foco
def validar_planilha(padrao):
    aba_excel = copiar_foco()
    if aba_excel == padrao:
        pyperclip.copy('')
        return True
    else:
        pyperclip.copy('')
        messagebox.showerror('Erro', 'Planilha não encontrada ou fora de foco')
        return False

def criar_pasta(nome_pasta):
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)

def apagar_arquivo():
    nome_arquivo = selecionar_arquivo()

    if not nome_arquivo:
        return

    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)
        messagebox.showinfo('Sucesso', 'O arquivo foi removido com sucesso!')

def selecionar_arquivo():
    arquivo = filedialog.askopenfilename(
        title='Selecione o arquivo',
        initialdir='data/notas_fiscais',
        filetypes=[('Arquivos CSV', '*.csv'), ('Todos os arquivos', '*.*')]
    )
    return arquivo

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

    colunas = ['PRODUTO', 'VALOR', 'ITENS', 'GRANDEZA', 'QUANTIDADE DE PRODUTO', 'VALOR UNITÁRIO', 'QUANTIDADE', 'TOTAL']

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

    