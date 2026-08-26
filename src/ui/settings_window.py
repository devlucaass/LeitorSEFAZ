from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkToplevel


class SettingsWindow(CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.windows()
        self.frames()
        self.labels()
        self.entries()
        self.buttons()

    def windows(self):
        self.title("Painel de Configurações")
        self.iconbitmap("assets/icons/logo.ico")
        self.geometry("500x500")
        self.resizable(False, False)

    def frames(self):
        self.main_frame = CTkFrame(
            master=self, fg_color="#32a14f", border_color="#75d58f", border_width=3
        )
        self.main_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def labels(self):
        self.lb_author = CTkLabel(
            master=self.main_frame,
            text="Desenvolvido por Lucas Vinícius",
            font=("Arial", 12, "bold")
        )
        self.lb_author.place(relx=0.298, rely=0.935)

        self.lb_title = CTkLabel(
            master=self.main_frame,
            text="SefazBot - Configurações",
            font=("Arial", 24, "bold")
        )
        self.lb_title.place(relx=0.220, rely=0.015)

        self.lb_excel_path = CTkLabel(
            master=self.main_frame,
            text="Nome do arquivo",
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        self.lb_excel_path.place(relx=0.350, rely=0.12)

        self.lb_sheet_name = CTkLabel(
            master=self.main_frame,
            text="Aba da planilha",
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        self.lb_sheet_name.place(relx=0.362, rely=0.300)

    def entries(self):
        self.entry_excel_path = CTkEntry(
            master=self.main_frame,
            placeholder_text="Informe o caminho do arquivo...",
            justify="center",
            width=300,
            fg_color="#235D34",
            border_color="#235D34"
        )
        self.entry_excel_path.place(relx=0.20, rely=0.18)

        self.entry_sheet_name = CTkEntry(
            master=self.main_frame,
            placeholder_text="Informe o nome da aba da planilha...",
            justify="center",
            width=300,
            fg_color="#235D34",
            border_color="#235D34"
        )
        self.entry_sheet_name.place(relx=0.20, rely=0.360)

    def buttons(self):
        self.btn_salvar_configuracoes = CTkButton(
            master=self.main_frame,
            text="Salvar configurações",
            font=("Arial", 15, "bold"),
            width=239,
            height=35,
            fg_color="#235D34",
            border_color="#72A782",
            border_width=2,
            hover_color="#33844B"
        )
        self.btn_salvar_configuracoes.place(relx=0.252, rely=0.500)

        self.btn_select_spreadsheet = CTkButton(
            master=self.main_frame,
            text="Localizar planilha",
            font=("Arial", 15, "bold"),
            width=239,
            height=35,
            fg_color="#235D34",
            border_color="#72A782",
            border_width=2,
            hover_color="#33844B"
        )
        self.btn_select_spreadsheet.place(relx=0.252, rely=0.600)
