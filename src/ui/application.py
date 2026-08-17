import threading

from PIL import Image
from tkinter import messagebox
from customtkinter import (
    set_appearance_mode,
    CTk,
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkButton,
    CTkImage
)

from services.sefaz_client import SefazClient
from services.excel_bot import ExcelBot
from utils.validators import valida_celula
from ui.settings_window import SettingsWindow

from utils.funcs import (
    gerar_modelo_planilha,
    ler_qrcode
)

set_appearance_mode('dark')

class Application:
    def __init__(self):
        self.root = CTk()
        self.window()
        self.frame()
        self.widgets()
    
    def window(self):
        self.root.title('Leitor de Notas Fiscais')
        self.root.iconbitmap('assets/icons/logo.ico')
        self.root.geometry('500x500')
        self.root.resizable(False, False)

    def frame(self):
        self.frame_principal = CTkFrame(master=self.root, fg_color='#32a14f', border_color="#75d58f", border_width=3)
        self.frame_principal.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def widgets(self):
        # Imagens
        img_qrcode = Image.open('assets/images/qrcode.png')
        img_gear = Image.open('assets/images/gear.png')

        self.img_qrcode = CTkImage(light_image=img_qrcode, dark_image=img_qrcode, size=(35,35))
        self.img_gear = CTkImage(light_image=img_gear, dark_image=img_gear, size=(20,20))

        # Labels
        self.lb_author = CTkLabel(master=self.frame_principal, text='Desenvolvido por Lucas Vinícius', font=('Arial', 12, 'bold'))
        self.lb_author.place(relx=0.293, rely=0.935)

        self.lb_title = CTkLabel(master=self.frame_principal, text='SefazBot - Leitor de Notas', font=('Arial', 24, 'bold'))
        self.lb_title.place(relx=0.195, rely=0.015)

        self.lb_excel_cell = CTkLabel(master=self.frame_principal, text='Célula (do Excel)', font=('Arial', 18, 'bold'), text_color='white')
        self.lb_excel_cell.place(relx=0.335, rely=0.12)

        self.lb_access_key = CTkLabel(master=self.frame_principal, text='Chave da nota', font=('Arial', 18, 'bold'), text_color='white')
        self.lb_access_key.place(relx=0.352, rely=0.300)

        # Entries
        self.entry_excel_cell = CTkEntry(master=self.frame_principal, placeholder_text='Informe a célula do Excel que deseja começar...', justify='center', width=300, fg_color='#235D34', border_color='#235D34')
        self.entry_excel_cell.place(relx=0.18, rely=0.18)

        self.entry_access_key = CTkEntry(master=self.frame_principal, placeholder_text='Informe a chave da nota fiscal...', justify='center', width=300, fg_color='#235D34', border_color='#235D34')
        self.entry_access_key.place(relx=0.18, rely=0.360)

        # Labels de erro
        self.lb_error_excel_cell = CTkLabel(master=self.frame_principal, text='', font=('Arial', 12, 'bold'), text_color='red')
        self.lb_error_excel_cell.place(relx=0.15, rely=0.237)

        self.lb_error_access_key = CTkLabel(master=self.frame_principal, text='', font=('Arial', 12, 'bold'), text_color='red')
        self.lb_error_access_key.place(relx=0.20, rely=0.418)

        # Buttons
        self.btn_start = CTkButton(master=self.frame_principal, text='Iniciar', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=lambda: self.start(False))
        self.btn_start.place(relx=0.242, rely=0.500)

        self.btn_read_qrcode = CTkButton(master=self.frame_principal, text='Ler QRCode', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", image=self.img_qrcode, compound='left', command=lambda: self.start(True))
        self.btn_read_qrcode.place(relx=0.242, rely=0.600)

        self.btn_generate_spreadsheet_template = CTkButton(master=self.frame_principal, text='Gerar modelo de planilha', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=gerar_modelo_planilha)
        self.btn_generate_spreadsheet_template.place(relx=0.242, rely=0.700)

        self.btn_settings = CTkButton(master=self.frame_principal, text='', font=('Arial', 15, 'bold'), width=30, height=30, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", image=self.img_gear, compound='left', command=self.open_window_settings)
        self.btn_settings.place(relx=0.910, rely=0.920)

    def open_window_settings(self):
        self.root.withdraw()

        self.settings_window = SettingsWindow(self.root)
        self.settings_window.protocol("WM_DELETE_WINDOW", self.close_window_settings)

    def close_window_settings(self):
        self.settings_window.destroy()
        self.root.deiconify()

    def clear_errors_messages(self):
        self.lb_error_excel_cell.configure(text='')
        self.lb_erro_chave.configure(text='')

    def validations(self, usar_qrcode=False):
        self.clear_errors_messages()

        excel_cell = self.entry_celula.get()
        access_key = self.entry_access_key.get()

        valido = True

        if not valida_celula(excel_cell):
            self.lb_error_excel_cell.configure(text='Célula inválida. Informe uma célula válida (ex: A1, B2, C3...).')
            valido = False

        if not usar_qrcode and not access_key:
            self.lb_erro_chave.configure(text='Informe uma chave válida ou use o modo QRCode.')
            valido = False

        return valido

    def start(self, usar_qrcode=False):

        if not self.validations(usar_qrcode):
            return

        self.start_thread(lambda: self.run(usar_qrcode))

    def start_thread(self, target):
        threading.Thread(target=target,daemon=True).start()

    def run(self, usar_qrcode=False):

        excel_cell = self.entry_celula.get()

        if usar_qrcode:
            qrcode = ler_qrcode()

            if not qrcode:
                return

            chave = qrcode.split('p=')[-1].split('|')[0]
            self.fluxo_principal(chave=chave, celula=excel_cell, url=qrcode)

        else:
            chave = self.entry_access_key.get()
            self.fluxo_principal(chave=chave, celula=excel_cell)

    def fluxo_principal(self, chave, celula, url=None):

        messagebox.showinfo('Iniciando', 'Iniciando automação...')

        sefaz = SefazClient(chave)

        if url:
            sefaz.configura_navegador(url, headless=True)

        else:
            sefaz.configura_navegador(URL_SEFAZ, headless=False)
            sefaz.digita_chave()

        dados = sefaz.coleta_dados()

        if not dados:
            return

        excel = ExcelBot(dados)
        excel.inserir_no_excel(celula)

    def run(self):
        self.root.mainloop()
