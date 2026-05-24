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
    # Inicializa a aplicação, criando a janela principal, o frame e os widgets (labels, entrys, buttons e radio buttons).
    def __init__(self):
        self.root = CTk()
        self.config = load_config()
        self.window()
        self.frame()
        self.widgets()
    
    # Configura a janela principal da aplicação, definindo o título, o ícone, o tamanho e a possibilidade de redimensionamento.
    def window(self):
        self.root.title('Leitor de Notas Fiscais')
        self.root.iconbitmap('assets/icons/logo.ico')
        self.root.geometry('800x800')
        self.root.resizable(False, False)

    def frame(self):
        self.frame_principal = CTkFrame(master=self.root, fg_color='#32a14f', border_color="#75d58f", border_width=3)
        self.frame_principal.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    # Cria os widgets da aplicação, incluindo labels, entrys, buttons e radio buttons, e os posiciona na janela utilizando o método place() para definir a posição relativa (relx e rely) e o tamanho (width e height) de cada widget.
    def widgets(self):
        # Imagens
        img_qrcode = Image.open('assets/images/qrcode.png')
        self.img_qrcode = CTkImage(light_image=img_qrcode, dark_image=img_qrcode, size=(35,35))

        # Labels
        self.lb_autoria = CTkLabel(master=self.frame_principal, text='Desenvolvido por Lucas Vinícius', font=('Arial', 12, 'bold'))
        self.lb_autoria.place(relx=0.380, rely=0.96)

        self.lb_titulo_principal = CTkLabel(master=self.frame_principal, text='SefazBot - Leitor de Notas', font=('Arial', 26, 'bold'))
        self.lb_titulo_principal.place(relx=0.300, rely=0.015)

        self.lb_celula = CTkLabel(master=self.frame_principal, text='Célula (do Excel)', font=('Arial', 18, 'bold'), text_color='white')
        self.lb_celula.place(relx=0.04, rely=0.12)

        self.lb_chave = CTkLabel(master=self.frame_principal, text='Chave da nota', font=('Arial', 18, 'bold'), text_color='white')
        self.lb_chave.place(relx=0.04, rely=0.22)

        # Entrys
        self.entry_celula = CTkEntry(master=self.frame_principal, placeholder_text='Informe a célula do Excel que deseja começar...', width=300, fg_color='#235D34', border_color='#235D34')
        self.entry_celula.place(relx=0.036, rely=0.155)

        self.entry_chave = CTkEntry(master=self.frame_principal, placeholder_text='Informe a chave da nota fiscal...', width=300, fg_color='#235D34', border_color='#235D34')
        self.entry_chave.place(relx=0.036, rely=0.255)

        # Labels de erro
        self.lb_erro_celula = CTkLabel(master=self.frame_principal, text='', font=('Arial', 12, 'bold'), text_color='red')
        self.lb_erro_celula.place(relx=0.04, rely=0.191)

        self.lb_erro_chave = CTkLabel(master=self.frame_principal, text='', font=('Arial', 12, 'bold'), text_color='red')
        self.lb_erro_chave.place(relx=0.04, rely=0.292)

        self.lb_erro_modo = CTkLabel(master=self.frame_principal, text='', font=('Arial', 12, 'bold'), text_color='red')
        self.lb_erro_modo.place(relx=0.039, rely=0.390)

        # Buttons
        self.btn_iniciar = CTkButton(master=self.frame_principal, text='Iniciar', font=('Arial', 15, 'bold'), width=110, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=self.iniciar_modo_sem_qrcode)
        self.btn_iniciar.place(relx=0.036, rely=0.430)

        self.btn_apagar_notas = CTkButton(master=self.frame_principal, text='Apagar notas', font=('Arial', 15, 'bold'), width=110, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=apagar_arquivo)
        self.btn_apagar_notas.place(relx=0.200, rely=0.430)

        self.btn_carregar_nota = CTkButton(master=self.frame_principal, text='Carregar notas', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=self.carregar_arquivo)
        self.btn_carregar_nota.place(relx=0.036, rely=0.490)

        self.btn_ler_qrcode = CTkButton(master=self.frame_principal, text='Ler QRCode', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", image=self.img_qrcode, compound='left', command=self.iniciar_modo_qrcode)
        self.btn_ler_qrcode.place(relx=0.036, rely=0.550)

        self.btn_gerar_modelo_planiilha = CTkButton(master=self.frame_principal, text='Gerar modelo de planilha', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=gerar_modelo_planilha)
        self.btn_gerar_modelo_planiilha.place(relx=0.036, rely=0.620)

        # RadioButtons
        self.rb_modo = StringVar()

        self.rb_web = CTkRadioButton(master=self.frame_principal, text='Coletar dados', variable=self.rb_modo, value='automacao_web', font=('Arial', 14, 'bold'), hover_color='#235D34', fg_color='#235D34', border_color="#64CA84")
        self.rb_web.place(relx=0.036, rely=0.325)

        self.rb_excel = CTkRadioButton(master=self.frame_principal, text='Inserir dados', variable=self.rb_modo, value='automacao_excel', font=('Arial', 14, 'bold'), hover_color='#235D34', fg_color='#235D34', border_color="#64CA84")
        self.rb_excel.place(relx=0.230, rely=0.325)

        self.rb_modo_completo = CTkRadioButton(master=self.frame_principal, text='Coletar e inserir dados', variable=self.rb_modo, value='automacao_completa', font=('Arial', 14, 'bold'), hover_color='#235D34', fg_color='#235D34', border_color="#64CA84")
        self.rb_modo_completo.place(relx=0.036, rely=0.365)

    # Limpa as mensagens de erro exibidas na interface, definindo o texto dos labels de erro como vazio e garantindo que a interface fique limpa para novas validações.
    def limpar_erros(self):
        self.lb_erro_celula.configure(text='')
        self.lb_erro_chave.configure(text='')
        self.lb_erro_modo.configure(text='')


    def validacoes(self, usar_qrcode=False):
        self.limpar_erros()
        self.celula = self.entry_celula.get()
        self.chave = self.entry_chave.get()
        modo = self.rb_modo.get()

        if not modo:
            self.lb_erro_modo.configure(text='Selecione um modo.')
            return False

        valido = True
        # Se não houver o uso do QRCode, o usuário irá informar manualmente a chave, e então haverá validação
        if not usar_qrcode:
            # Valida Chave para esses modos
            if modo in ['automacao_web', 'automacao_excel', 'automacao_completa']:
                if not valida_chave(self.chave):
                    self.lb_erro_chave.configure(text='Chave inválida.')
                    valido = False

        # Valida Célula para esses modos
        if modo in ['automacao_excel', 'automacao_completa']:
            if not valida_celula(self.celula):
                self.lb_erro_celula.configure(text='Célula inválida.')
                valido = False

        return valido
    
    # Carrega um arquivo CSV selecionado pelo usuário, extrai a chave da nota fiscal a partir do nome do arquivo e insere essa chave no campo de entrada correspondente na interface gráfica. Essa função é útil para facilitar o processo de carregamento de dados, permitindo que o usuário selecione um arquivo já existente em vez de digitar a chave manualmente.
    def carregar_arquivo(self):
        nome_arquivo = selecionar_arquivo()

        if not nome_arquivo:
            return
        
        nome_arquivo = os.path.basename(nome_arquivo)
        chave = nome_arquivo.replace('nf_', '').replace('.csv', '')

        self.entry_chave.delete(0, 'end')
        self.entry_chave.insert(0, chave)
        
    def modo_qrcode(self):
        self.limpar_erros()

        if not self.rb_modo.get():
            self.lb_erro_modo.configure(text='Selecione um modo')
            return

        qrcode = ler_qrcode()

        if qrcode:
            self.celula = self.entry_celula.get()
            self.chave = qrcode.split('p=')[-1].split('|')[0]

            self.executar_fluxo(url=qrcode)

    def modo_sem_qrcode(self):
            self.executar_fluxo()

    def iniciar_modo_qrcode(self):
        if self.validacoes(usar_qrcode=True):
            threading.Thread(target=self.modo_qrcode, daemon=True).start()

    def iniciar_modo_sem_qrcode(self):
        if self.validacoes():
            threading.Thread(target=self.modo_sem_qrcode, daemon=True).start()

    # Fluxo principal da aplicação, que é executado quando o usuário clica no botão "Iniciar". Dependendo do modo selecionado (coletar dados, inserir dados ou ambos), a função executa as ações correspondentes, como configurar o navegador, coletar os dados da nota fiscal e inserir os dados no Excel. O fluxo é executado em uma thread separada para evitar que a interface gráfica fique congelada durante a execução das tarefas.
    def executar_fluxo(self, url=None):
        if self.rb_modo.get() == 'automacao_web':
            messagebox.showinfo('Iniciando', 'Iniciando coleta de dados')
            sefaz = SefazBot(self.chave)

            if url:
                sefaz.configura_navegador(url, headless=True)
            else:
                sefaz.configura_navegador('https://nfce.sefaz.pe.gov.br/nfce/consulta', headless=False)

            if not url:
                sefaz.digita_chave()

            sefaz.coleta_dados()

        elif self.rb_modo.get() == 'automacao_excel':
            messagebox.showinfo('Iniciando', 'Iniciando automação Excel')
            excel = ExcelBot(self.chave)
            excel.celula_inicial(self.celula)
            excel.inserir_no_excel(self.config['nome_planilha'])

        elif self.rb_modo.get() == 'automacao_completa':
            messagebox.showinfo('Iniciando', 'Iniciando automação completa')
            sefaz = SefazBot(self.chave)

            if url:
                sefaz.configura_navegador(url, headless=True)
            else:
                sefaz.configura_navegador('https://nfce.sefaz.pe.gov.br/nfce/consulta', headless=False)

            if not url:
                sefaz.digita_chave()

            self.chave = sefaz.coleta_dados()

            excel = ExcelBot(self.chave)
            excel.celula_inicial(self.celula)
            excel.inserir_no_excel(self.config['nome_planilha'])

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = Application()
    app.run()


