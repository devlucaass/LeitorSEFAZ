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
        self.root.geometry('500x500')
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
        self.btn_iniciar = CTkButton(master=self.frame_principal, text='Iniciar', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=self.iniciar_modo_sem_qrcode)
        self.btn_iniciar.place(relx=0.242, rely=0.500
        )

        self.btn_ler_qrcode = CTkButton(master=self.frame_principal, text='Ler QRCode', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", image=self.img_qrcode, compound='left', command=self.iniciar_modo_qrcode)
        self.btn_ler_qrcode.place(relx=0.242, rely=0.600)

        self.btn_gerar_modelo_planiilha = CTkButton(master=self.frame_principal, text='Gerar modelo de planilha', font=('Arial', 15, 'bold'), width=239, height=35, fg_color='#235D34', border_color="#72A782", border_width=2, hover_color="#33844B", command=gerar_modelo_planilha)
        self.btn_gerar_modelo_planiilha.place(relx=0.242, rely=0.700)

    # Limpa as mensagens de erro exibidas na interface, definindo o texto dos labels de erro como vazio e garantindo que a interface fique limpa para novas validações.
    def limpar_erros(self):
        self.lb_erro_celula.configure(text='')
        self.lb_erro_chave.configure(text='')

    def validacoes(self, usar_qrcode=False):
        self.limpar_erros()
        self.celula = self.entry_celula.get()
        self.chave = self.entry_chave.get()

        valido = True

        if not valida_celula(self.celula):
            self.lb_erro_celula.configure(text='Célula inválida. Informe uma célula válida (ex: A1, B2, C3...).')
            valido = False

        if not usar_qrcode and not self.chave:
            self.lb_erro_chave.configure(text='Informe uma chave válida ou use o modo QRCode.')
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

        qrcode = ler_qrcode()

        if qrcode:
            self.celula = self.entry_celula.get()
            self.chave = qrcode.split('p=')[-1].split('|')[0]

            self.main(url=qrcode)

    def modo_sem_qrcode(self):
            self.main()

    def iniciar_modo_qrcode(self):
        if self.validacoes(usar_qrcode=True):
            threading.Thread(target=self.modo_qrcode, daemon=True).start()

    def iniciar_modo_sem_qrcode(self):
        if self.validacoes():
            threading.Thread(target=self.modo_sem_qrcode, daemon=True).start()

    # Fluxo principal da aplicação, que é executado quando o usuário clica no botão "Iniciar". Dependendo do modo selecionado (coletar dados, inserir dados ou ambos), a função executa as ações correspondentes, como configurar o navegador, coletar os dados da nota fiscal e inserir os dados no Excel. O fluxo é executado em uma thread separada para evitar que a interface gráfica fique congelada durante a execução das tarefas.
    def main(self, url=None):
            messagebox.showinfo('Iniciando', 'Iniciando automação...')
            sefaz = SefazBot(self.chave)

            if url:
                sefaz.configura_navegador(url, headless=True)
            else:
                sefaz.configura_navegador('https://nfce.sefaz.pe.gov.br/nfce/consulta', headless=False)

            if not url:
                sefaz.digita_chave()

            dados = sefaz.coleta_dados()

            excel = ExcelBot(dados)
            excel.inserir_no_excel(self.config['caminho_excel'], self.celula)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = Application()
    app.run()


