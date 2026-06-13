import threading
from PIL import Image
from customtkinter import *
from tkinter import messagebox
from config.config_manager import load_config
from services.sefaz_service import SefazBot
from services.excel_service import ExcelBot
from utils.validators import valida_celula
from utils.funcs import *

set_appearance_mode('dark')

class Application:
    def __init__(self):
        self.root = CTk()
        self.config = load_config()
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
        self.lb_autoria = CTkLabel(master=self.frame_principal, text='Desenvolvido por Lucas Vinícius', font=('Arial', 12, 'bold'))
        self.lb_autoria.place(relx=0.293, rely=0.935)

        self.lb_titulo_principal = CTkLabel(master=self.frame_principal, text='SefazBot - Leitor de Notas', font=('Arial', 24, 'bold'))
        self.lb_titulo_principal.place(relx=0.195, rely=0.015)

        self.lb_celula = CTkLabel(master=self.frame_principal, text='Célula (do Excel)', font=('Arial', 18, 'bold'), text_color='white')
        self.lb_celula.place(relx=0.335, rely=0.12)

        self.lb_chave = CTkLabel(master=self.frame_principal, text='Chave da nota', font=('Arial', 18, 'bold'), text_color='white')
        self.lb_chave.place(relx=0.352, rely=0.300)

        # Entrys
        self.entry_celula = CTkEntry(master=self.frame_principal, placeholder_text='Informe a célula do Excel que deseja começar...', justify='center', width=300, fg_color='#235D34', border_color='#235D34')
        self.entry_celula.place(relx=0.18, rely=0.18)

        self.entry_chave = CTkEntry(master=self.frame_principal, placeholder_text='Informe a chave da nota fiscal...', justify='center', width=300, fg_color='#235D34', border_color='#235D34')
        self.entry_chave.place(relx=0.18, rely=0.360)

        # Labels de erro
        self.lb_erro_celula = CTkLabel(master=self.frame_principal, text='', font=('Arial', 12, 'bold'), text_color='red')
        self.lb_erro_celula.place(relx=0.15, rely=0.237)

        self.lb_erro_chave = CTkLabel(master=self.frame_principal, text='', font=('Arial', 12, 'bold'), text_color='red')
        self.lb_erro_chave.place(relx=0.20, rely=0.418)

        # Buttons
        self.btn_iniciar = CTkButton(master=self.frame_principal, text='Iniciar', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=lambda: self.iniciar(False))
        self.btn_iniciar.place(relx=0.242, rely=0.500)

        self.btn_ler_qrcode = CTkButton(master=self.frame_principal, text='Ler QRCode', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", image=self.img_qrcode, compound='left', command=lambda: self.iniciar(True))
        self.btn_ler_qrcode.place(relx=0.242, rely=0.600)

        self.btn_gerar_modelo_planiilha = CTkButton(master=self.frame_principal, text='Gerar modelo de planilha', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=gerar_modelo_planilha)
        self.btn_gerar_modelo_planiilha.place(relx=0.242, rely=0.700)

        self.btn_configuracoes = CTkButton(master=self.frame_principal, text='', font=('Arial', 15, 'bold'), width=30, height=30, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", image=self.img_gear, compound='left', command=abrir_configuracoes)
        self.btn_configuracoes.place(relx=0.910, rely=0.920)

    def limpar_erros(self):
        self.lb_erro_celula.configure(text='')
        self.lb_erro_chave.configure(text='')

    def validacoes(self, usar_qrcode=False):
        self.limpar_erros()

        celula = self.entry_celula.get()
        chave = self.entry_chave.get()

        valido = True

        if not valida_celula(celula):
            self.lb_erro_celula.configure(text='Célula inválida. Informe uma célula válida (ex: A1, B2, C3...).')
            valido = False

        if not usar_qrcode and not chave:
            self.lb_erro_chave.configure(text='Informe uma chave válida ou use o modo QRCode.')
            valido = False

        return valido

    def iniciar(self, usar_qrcode=False):

        if not self.validacoes(usar_qrcode):
            return

        self.iniciar_thread(lambda: self.executar(usar_qrcode))

    def iniciar_thread(self, target):
        threading.Thread(target=target,daemon=True).start()

    def executar(self, usar_qrcode=False):

        celula = self.entry_celula.get()

        if usar_qrcode:
            qrcode = ler_qrcode()

            if not qrcode:
                return

            chave = qrcode.split('p=')[-1].split('|')[0]
            self.fluxo_principal(chave=chave, celula=celula, url=qrcode)

        else:
            chave = self.entry_chave.get()
            self.fluxo_principal(chave=chave, celula=celula)

    def fluxo_principal(self, chave, celula, url=None):

        messagebox.showinfo('Iniciando', 'Iniciando automação...')

        sefaz = SefazBot(chave)

        if url:
            sefaz.configura_navegador(url, headless=True)

        else:
            sefaz.configura_navegador(self.config['url_site'], headless=False)
            sefaz.digita_chave()

        dados = sefaz.coleta_dados()

        if not dados:
            return

        excel = ExcelBot(dados)
        excel.inserir_no_excel(celula)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = Application()
    app.run()


