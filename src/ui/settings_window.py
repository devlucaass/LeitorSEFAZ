from tkinter import messagebox

from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkToplevel

from config.config_manager import ConfigManager
from config.constants import APP_ICON_PATH, EXCEL_PATH_KEY, SHEET_NAME_KEY
from utils.file_dialog import select_file


class SettingsWindow(CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.window()
        self.frames()
        self.labels()
        self.entries()
        self.buttons()
        self._load_config_values()

    def window(self):
        self.title("Painel de Configurações")
        self.iconbitmap(APP_ICON_PATH)
        self.geometry("500x500")
        self.resizable(False, False)

    def frames(self):
        self.main_frame = CTkFrame(
            master=self,
            fg_color="#32a14f",
            border_color="#75d58f",
            border_width=3
        )
        self.main_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def labels(self):
        self.lb_author = CTkLabel(
            master=self.main_frame,
            text="Desenvolvido por Lucas Vinícius",
            font=("Arial", 12, "bold"),
        )
        self.lb_author.place(relx=0.298, rely=0.935)

        self.lb_title = CTkLabel(
            master=self.main_frame,
            text="SefazBot - Configurações",
            font=("Arial", 24, "bold"),
        )
        self.lb_title.place(relx=0.220, rely=0.015)

        self.lb_excel_path = CTkLabel(
            master=self.main_frame,
            text="Nome do arquivo",
            font=("Arial", 18, "bold"),
            text_color="white",
        )
        self.lb_excel_path.place(relx=0.350, rely=0.12)

        self.lb_sheet_name = CTkLabel(
            master=self.main_frame,
            text="Aba da planilha",
            font=("Arial", 18, "bold"),
            text_color="white",
        )
        self.lb_sheet_name.place(relx=0.362, rely=0.300)

    def entries(self):
        self.entry_excel_path = CTkEntry(
            master=self.main_frame,
            placeholder_text="Informe o caminho do arquivo...",
            justify="center",
            width=300,
            fg_color="#235D34",
            border_color="#235D34",
        )
        self.entry_excel_path.place(relx=0.20, rely=0.18)

        self.entry_sheet_name = CTkEntry(
            master=self.main_frame,
            placeholder_text="Informe o nome da aba da planilha...",
            justify="center",
            width=300,
            fg_color="#235D34",
            border_color="#235D34",
        )
        self.entry_sheet_name.place(relx=0.20, rely=0.360)

    def buttons(self):
        self.btn_save_settings = CTkButton(
            master=self.main_frame,
            text="Salvar configurações",
            font=("Arial", 15, "bold"),
            width=239,
            height=35,
            fg_color="#235D34",
            border_color="#72A782",
            border_width=2,
            hover_color="#33844B",
            command=self._save_settings,
        )
        self.btn_save_settings.place(relx=0.252, rely=0.500)

        self.btn_select_spreadsheet = CTkButton(
            master=self.main_frame,
            text="Localizar planilha",
            font=("Arial", 15, "bold"),
            width=239,
            height=35,
            fg_color="#235D34",
            border_color="#72A782",
            border_width=2,
            hover_color="#33844B",
            command=self._select_spreadsheet,
        )
        self.btn_select_spreadsheet.place(relx=0.252, rely=0.600)

    def _load_config_values(self):
        config = ConfigManager.load_config()

        if not config:
            return

        self.entry_excel_path.insert(0, config[EXCEL_PATH_KEY])
        self.entry_sheet_name.insert(0, config[SHEET_NAME_KEY])

    def _select_spreadsheet(self):
        excel_path = select_file()

        if not excel_path:
            return

        self.entry_excel_path.delete(0, "end")
        self.entry_excel_path.insert(0, excel_path)

    def _save_settings(self):
        excel_path = self.entry_excel_path.get()
        sheet_name = self.entry_sheet_name.get()

        success = ConfigManager.save_config(excel_path, sheet_name)

        if success:
            messagebox.showinfo(
                "Alterações salvas", "Configurações salvas com sucesso!"
            )
        else:
            messagebox.showerror(
                "Não foi possível salvar",
                "Não foi possível salvar suas configurações.\n"
                "Verifique as informações e tente novamente."
            )
