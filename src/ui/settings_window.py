from customtkinter import (
    CTk,
    CTkToplevel,
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkButton
)

from utils.funcs import buscar_arquivo

class SettingsWindow(CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.window()
        self.frame()
        self.widgets()

    def window(self):
        self.title('Painel de Configurações')
        self.iconbitmap('assets/icons/logo.ico')
        self.geometry('500x500')
        self.resizable(False, False)

    def frame(self):
        self.frame_principal = CTkFrame(master=self, fg_color='#32a14f', border_color="#75d58f", border_width=3)
        self.frame_principal.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def widgets(self):
        # Labels
        self.lb_autoria = CTkLabel(master=self.frame_principal, text='Desenvolvido por Lucas Vinícius', font=('Arial', 12, 'bold'))
        self.lb_autoria.place(relx=0.298, rely=0.935)

        self.lb_titulo_principal = CTkLabel(master=self.frame_principal, text='SefazBot - Configurações', font=('Arial', 24, 'bold'))
        self.lb_titulo_principal.place(relx=0.220, rely=0.015)

        self.lb_caminho_planilha = CTkLabel(master=self.frame_principal, text='Nome do arquivo', font=('Arial', 18, 'bold'), text_color='white')
        self.lb_caminho_planilha.place(relx=0.350, rely=0.12)

        self.lb_aba_planilha = CTkLabel(master=self.frame_principal, text='Aba da planilha', font=('Arial', 18, 'bold'), text_color='white')
        self.lb_aba_planilha.place(relx=0.362, rely=0.300)
        
        # Entries
        self.entry_caminho_planilha = CTkEntry(master=self.frame_principal, placeholder_text='Informe o caminho do arquivo...', justify='center', width=300, fg_color='#235D34', border_color='#235D34')
        self.entry_caminho_planilha.place(relx=0.20, rely=0.18)

        self.entry_aba_planilha = CTkEntry(master=self.frame_principal, placeholder_text='Informe o nome da aba da planilha...', justify='center', width=300, fg_color='#235D34', border_color='#235D34')
        self.entry_aba_planilha.place(relx=0.20, rely=0.360)

        # Buttons
        self.btn_salvar_configuracoes = CTkButton(master=self.frame_principal, text='Salvar configurações', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B")
        self.btn_salvar_configuracoes.place(relx=0.252, rely=0.500)

        self.btn_buscar_caminho_planilha = CTkButton(master=self.frame_principal, text='Localizar planilha', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=self.selecionar_planilha)
        self.btn_buscar_caminho_planilha.place(relx=0.252, rely=0.600)

    def selecionar_planilha(self):
        caminho = buscar_arquivo()

        if caminho:
            self.entry_caminho_planilha.delete(0, 'end')
            self.entry_caminho_planilha.insert(0, caminho)
        

if __name__ == '__main__':
    root = CTk()
    root.withdraw()

    settings_window = SettingsWindow(root)
    settings_window.mainloop()