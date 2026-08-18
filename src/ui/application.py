import threading

from customtkinter import (
    CTk,
    CTkButton,
    CTkEntry,
    CTkFrame,
    CTkImage,
    CTkLabel,
    set_appearance_mode,
)
from PIL import Image

from config.config_manager import load_config
from services.excel_bot import ExcelBot
from services.sefaz_client import SefazClient
from ui.settings_window import SettingsWindow
from utils.funcs import gerar_modelo_planilha, read_qrcode
from utils.validators import valida_celula

set_appearance_mode('dark')

class Application:
    def __init__(self):
        self.root = CTk()
        self.window()
        self.frames()
        self.images()
        self.labels()
        self.entries()
        self.buttons()

    def window(self):
        self.root.title('Leitor de Notas Fiscais')
        self.root.iconbitmap('assets/icons/logo.ico')
        self.root.geometry('500x500')
        self.root.resizable(False, False)

    def frames(self):
        self.main_frame = CTkFrame(master=self.root, fg_color='#32a14f', border_color="#75d58f", border_width=3)
        self.main_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def images(self):
        img_qrcode = Image.open('assets/images/qrcode.png')
        img_gear = Image.open('assets/images/gear.png')

        self.img_qrcode = CTkImage(light_image=img_qrcode, dark_image=img_qrcode, size=(35,35))
        self.img_gear = CTkImage(light_image=img_gear, dark_image=img_gear, size=(20,20))

    def labels(self):
        self.lb_author = CTkLabel(master=self.main_frame, text='Desenvolvido por Lucas Vinícius', font=('Arial', 12, 'bold'))
        self.lb_author.place(relx=0.293, rely=0.935)

        self.lb_title = CTkLabel(master=self.main_frame, text='SefazBot - Leitor de Notas', font=('Arial', 24, 'bold'))
        self.lb_title.place(relx=0.195, rely=0.015)

        self.lb_excel_cell = CTkLabel(master=self.main_frame, text='Célula (do Excel)', font=('Arial', 18, 'bold'), text_color='white')
        self.lb_excel_cell.place(relx=0.335, rely=0.12)

        self.lb_access_key = CTkLabel(master=self.main_frame, text='Chave da nota', font=('Arial', 18, 'bold'), text_color='white')
        self.lb_access_key.place(relx=0.352, rely=0.300)

        self.lb_error_excel_cell = CTkLabel(master=self.main_frame, text='', font=('Arial', 12, 'bold'), text_color='red')
        self.lb_error_excel_cell.place(relx=0.15, rely=0.237)

        self.lb_error_access_key = CTkLabel(master=self.main_frame, text='', font=('Arial', 12, 'bold'), text_color='red')
        self.lb_error_access_key.place(relx=0.20, rely=0.418)

    def entries(self):
        self.entry_excel_cell = CTkEntry(master=self.main_frame, placeholder_text='Informe a célula do Excel que deseja começar...', justify='center', width=300, fg_color='#235D34', border_color='#235D34')
        self.entry_excel_cell.place(relx=0.18, rely=0.18)

        self.entry_access_key = CTkEntry(master=self.main_frame, placeholder_text='Informe a chave da nota fiscal...', justify='center', width=300, fg_color='#235D34', border_color='#235D34')
        self.entry_access_key.place(relx=0.18, rely=0.360)

    def buttons(self):
        self.btn_start = CTkButton(master=self.main_frame, text='Iniciar', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=lambda: self.start(False))
        self.btn_start.place(relx=0.242, rely=0.500)

        self.btn_read_qrcode = CTkButton(master=self.main_frame, text='Ler QRCode', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", image=self.img_qrcode, compound='left', command=lambda: self.start(True))
        self.btn_read_qrcode.place(relx=0.242, rely=0.600)

        self.btn_generate_spreadsheet_template = CTkButton(master=self.main_frame, text='Gerar modelo de planilha', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=gerar_modelo_planilha)
        self.btn_generate_spreadsheet_template.place(relx=0.242, rely=0.700)

        self.btn_settings = CTkButton(master=self.main_frame, text='', font=('Arial', 15, 'bold'), width=30, height=30, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", image=self.img_gear, compound='left', command=self._open_window_settings)
        self.btn_settings.place(relx=0.910, rely=0.920)

    def _open_window_settings(self):
        self.root.withdraw()

        self.settings_window = SettingsWindow(self.root)
        self.settings_window.protocol("WM_DELETE_WINDOW", self._close_window_settings)

    def _close_window_settings(self):
        self.settings_window.destroy()
        self.root.deiconify()

    def _clear_errors_messages(self):
        self.lb_error_excel_cell.configure(text='')
        self.lb_erro_chave.configure(text='')

    def validations(self, use_qrcode=False):
        self._clear_errors_messages()

        excel_cell = self.entry_excel_cell.get()
        access_key = self.entry_access_key.get()

        is_valid = True

        if not valida_celula(excel_cell):
            self.lb_error_excel_cell.configure(text='Célula inválida. Informe uma célula válida (ex: A1, B2, C3...).')
            is_valid = False

        if not use_qrcode and not access_key:
            self.lb_erro_chave.configure(text='Informe uma chave válida ou use o modo QRCode.')
            is_valid = False

        return is_valid

    def start(self, use_qrcode=False):

        if not self.validations(use_qrcode):
            return

        self.start_thread(lambda: self.run_app(use_qrcode))

    def start_thread(self, target):
        threading.Thread(target=target,daemon=True).start()

    def run_app(self, use_qrcode=False):

        excel_cell = self.entry_excel_cell.get()

        if use_qrcode:
            qrcode = read_qrcode()

            if not qrcode:
                return

            access_key = qrcode.split('p=')[-1].split('|')[0]
            self.main(access_key=access_key, excel_cell=excel_cell, url=qrcode)

        else:
            access_key = self.entry_access_key.get()
            self.main(access_key=access_key, excel_cell=excel_cell)

    def main(self, access_key, excel_cell, url=None):

        print("Iniciando automação...")

        sefaz = SefazClient(access_key)

        if url:
            sefaz.configure_browser(url, headless=True)

        else:
            sefaz.configure_browser(load_config('sefaz_url'), headless=False)
            sefaz.enter_access_key()

        data = sefaz.collect_data()

        if not data:
            return

        excel = ExcelBot(data)
        excel.insert_data(excel_cell)

    def run(self):
        self.root.mainloop()
