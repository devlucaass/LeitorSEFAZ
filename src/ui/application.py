import threading
from tkinter import messagebox

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

from config.constants import (
    APP_ICON_PATH,
    GEAR_IMAGE_PATH,
    QRCODE_IMAGE_PATH,
    URL_SEFAZ,
)
from services.excel_bot import ExcelBot
from services.sefaz_client import SefazClient
from ui.settings_window import SettingsWindow
from utils.qrcode import QRCode
from utils.validators import Validators

set_appearance_mode("dark")


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
        self.root.title("Leitor de Notas Fiscais")
        self.root.iconbitmap(APP_ICON_PATH)
        self.root.geometry("500x500")
        self.root.resizable(False, False)

    def frames(self):
        self.main_frame = CTkFrame(
            master=self.root, fg_color="#32a14f", border_color="#75d58f", border_width=3
        )
        self.main_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def images(self):
        img_qrcode = Image.open(QRCODE_IMAGE_PATH)
        img_gear = Image.open(GEAR_IMAGE_PATH)

        self.img_qrcode = CTkImage(
            light_image=img_qrcode, dark_image=img_qrcode, size=(35, 35)
        )
        self.img_gear = CTkImage(
            light_image=img_gear, dark_image=img_gear, size=(20, 20)
        )

    def labels(self):
        self.lb_author = CTkLabel(
            master=self.main_frame,
            text="Desenvolvido por Lucas Vinícius",
            font=("Arial", 12, "bold"),
        )
        self.lb_author.place(relx=0.293, rely=0.935)

        self.lb_title = CTkLabel(
            master=self.main_frame,
            text="SefazBot - Leitor de Notas",
            font=("Arial", 24, "bold"),
        )
        self.lb_title.place(relx=0.195, rely=0.015)

        self.lb_excel_cell = CTkLabel(
            master=self.main_frame,
            text="Célula (do Excel)",
            font=("Arial", 18, "bold"),
            text_color="white",
        )
        self.lb_excel_cell.place(relx=0.335, rely=0.12)

        self.lb_access_key = CTkLabel(
            master=self.main_frame,
            text="Chave da nota",
            font=("Arial", 18, "bold"),
            text_color="white",
        )
        self.lb_access_key.place(relx=0.352, rely=0.300)

        self.lb_error_excel_cell = CTkLabel(
            master=self.main_frame,
            text="",
            font=("Arial", 12, "bold"),
            text_color="red",
        )
        self.lb_error_excel_cell.place(relx=0.15, rely=0.237)

        self.lb_error_access_key = CTkLabel(
            master=self.main_frame,
            text="",
            font=("Arial", 12, "bold"),
            text_color="red",
        )
        self.lb_error_access_key.place(relx=0.20, rely=0.418)

    def entries(self):
        self.entry_excel_cell = CTkEntry(
            master=self.main_frame,
            placeholder_text="Informe a célula do Excel que deseja começar...",
            justify="center",
            width=300,
            fg_color="#235D34",
            border_color="#235D34",
        )
        self.entry_excel_cell.place(relx=0.18, rely=0.18)

        self.entry_access_key = CTkEntry(
            master=self.main_frame,
            placeholder_text="Informe a chave da nota fiscal...",
            justify="center",
            width=300,
            fg_color="#235D34",
            border_color="#235D34",
        )
        self.entry_access_key.place(relx=0.18, rely=0.360)

    def buttons(self):
        self.btn_start = CTkButton(
            master=self.main_frame,
            text="Iniciar",
            font=("Arial", 15, "bold"),
            width=239,
            height=35,
            fg_color="#235D34",
            border_color="#72A782",
            border_width=2,
            hover_color="#33844B",
            command=self.start,
        )
        self.btn_start.place(relx=0.242, rely=0.500)

        self.btn_read_qrcode = CTkButton(
            master=self.main_frame,
            text="Ler QRCode",
            font=("Arial", 15, "bold"),
            width=239,
            height=35,
            fg_color="#235D34",
            border_color="#72A782",
            border_width=2,
            hover_color="#33844B",
            image=self.img_qrcode,
            compound="left",
            command=self.start_qrcode,
        )
        self.btn_read_qrcode.place(relx=0.242, rely=0.600)

        self.btn_create_spreadsheet_template = CTkButton(
            master=self.main_frame,
            text="Gerar modelo de planilha",
            font=("Arial", 15, "bold"),
            width=239,
            height=35,
            fg_color="#235D34",
            border_color="#72A782",
            border_width=2,
            hover_color="#33844B",
            command=ExcelBot.create_spreadsheet_template,
        )
        self.btn_create_spreadsheet_template.place(relx=0.242, rely=0.700)

        self.btn_settings = CTkButton(
            master=self.main_frame,
            text="",
            font=("Arial", 15, "bold"),
            width=30,
            height=30,
            fg_color="#235D34",
            border_color="#72A782",
            border_width=2,
            hover_color="#33844B",
            image=self.img_gear,
            compound="left",
            command=self._open_window_settings,
        )
        self.btn_settings.place(relx=0.910, rely=0.920)

    def _open_window_settings(self):
        self.settings_window = SettingsWindow(self.root)

        self.settings_window.transient(self.root)
        self.settings_window.grab_set()

        self.settings_window.protocol("WM_DELETE_WINDOW", self._close_window_settings)

        self.root.withdraw()

    def _close_window_settings(self):
        self.settings_window.destroy()
        self.root.deiconify()

    def _clear_errors_messages(self):
        self.lb_error_excel_cell.configure(text="")
        self.lb_error_access_key.configure(text="")

    def _validations(self, use_qrcode=False):
        self._clear_errors_messages()

        access_key = self._get_access_key_input()
        excel_cell = self._get_excel_cell_input()

        is_valid = True

        if not Validators.validate_excel_cell(excel_cell):
            self.lb_error_excel_cell.configure(
                text="Célula inválida. Informe uma célula válida (ex: A1, B2, C3...)."
            )
            is_valid = False

        if not use_qrcode and not Validators.validate_access_key(access_key):
            self.lb_error_access_key.configure(
                text="Informe uma chave válida ou use o modo QRCode."
            )
            is_valid = False

        return is_valid

    def _get_access_key_input(self):
        return self.entry_access_key.get()

    def _get_excel_cell_input(self):
        return self.entry_excel_cell.get()

    def _run_sefaz(self, access_key, url=None):
        sefaz_client = SefazClient()

        if url:
            if not sefaz_client.configure_browser(url, headless=True):
                messagebox.showerror(
                    "Erro", "Verifique sua conexão com a internet e tente novamente."
                )
                return []
        else:
            if not sefaz_client.configure_browser(URL_SEFAZ):
                messagebox.showerror(
                    "Erro", "Verifique sua conexão com a internet e tente novamente."
                )
                return []

            if not sefaz_client.enter_access_key(access_key):
                messagebox.showerror(
                    "Erro", "Não foi possível realizar a consulta da nota fiscal."
                )
                return []

        return sefaz_client.collect_data()

    def _run_excel(self, data, excel_cell):
        excel_bot = ExcelBot(data)

        if not excel_bot.insert_data(excel_cell):
            messagebox.showerror(
                "Erro", "Não foi possível inserir os dados na planilha."
            )

            return

        messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")

    def _start_thread(self, target, args=()):
        threading.Thread(target=target, args=args, daemon=True).start()

    def _run_process(self, access_key, excel_cell):
        data = self._run_sefaz(access_key)

        if not data:
            messagebox.showerror("Erro", "Não foi possível obter dados da nota fiscal.")

            return

        self._run_excel(data, excel_cell)

    def _run_qrcode_process(self, excel_cell):
        url, access_key = QRCode.read_qrcode()

        if not url:
            return

        data = self._run_sefaz(access_key, url)

        if not data:
            messagebox.showerror("Erro", "Não foi possível obter dados da nota fiscal.")
            return

        self._run_excel(data, excel_cell)

    def start(self):
        if not self._validations():
            return

        messagebox.showinfo("Iniciando", "Clique em OK para prosseguir...")

        access_key = self._get_access_key_input()
        excel_cell = self._get_excel_cell_input()

        self._start_thread(self._run_process, args=(access_key, excel_cell))

    def start_qrcode(self):
        if not self._validations(use_qrcode=True):
            return

        excel_cell = self._get_excel_cell_input()

        self._start_thread(self._run_qrcode_process, args=(excel_cell,))

    def run(self):
        self.root.mainloop()
