import os
import cv2
import pyautogui
import pyperclip
from time import sleep
from pyzbar import pyzbar
from utils.validators import valida_chave
from tkinter import messagebox, filedialog

# Copia o nome da planilha e salva na Área de Transferência.
def copiar_foco():
    pyautogui.press('alt')
    sleep(0.1)
    pyautogui.press('c')
    sleep(0.1)
    pyautogui.press('o')
    sleep(0.1)
    pyautogui.press('r')
    sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    planilha_em_foco = pyperclip.paste()
    pyautogui.press('esc')

    return planilha_em_foco.strip()

# Valida o nome da planilha e compara com o nome padrão. Se não tiverem o mesmo nome, o programa para.
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

# Lê QRCodes e retorna seu valor em string.
def ler_qrcode():
    cam = cv2.VideoCapture(0)
    encontrado = False

    while True:
        resultado, frame = cam.read()
        if not resultado:
            break

        qrcodes = pyzbar.decode(frame)
        for qr in qrcodes:
            url = qr.data.decode('utf-8')
            chave = url.split('p=')[-1].split('|')[0]

            if valida_chave(chave):
                encontrado = True
                cam.release()
                cv2.destroyAllWindows()
                return url
            else:
                cam.release()
                cv2.destroyAllWindows()
                messagebox.showwarning('Erro', f'QR Code inválido: {url}')

        cv2.imshow('Leitor de QRCode', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    if not encontrado:
        return False
    