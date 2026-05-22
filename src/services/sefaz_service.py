import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox
from utils.funcs import criar_pasta


class SefazBot:

    # Inicializa a classe, recebendo a chave como parâmetro e garante que a pasta de saída para as NFs seja criada.
    def __init__(self, chave):
        criar_pasta('data/notas_fiscais')

        self.driver = None
        self.chave = chave

    # Recebe a URL como parâmetro e define as configurações de janela, podendo rodar em segundo plano (headless).
    def configura_navegador(self, site, headless=False):
        try:
            options = Options()
            options.set_preference('dom.webnotifications.enabled', False)
            options.set_preference('layout.css.devPixelsPerPx', '0.7')

            if headless:
                options.add_argument('--headless')

            self.driver = webdriver.Firefox(options=options)
            self.driver.maximize_window()
        
            self.driver.get(site)

        except Exception:
            messagebox.showerror('Erro', f'Ocorreu um erro inesperado. Fechando navegador...')
            self.driver.quit()

    # Insere a chave informada pelo usuário no site e abre o CAPTCHA para o usuário resolver manualmente. Ao identificar a resolução do CAPTCHA, prossegue automaticamente.
    def digita_chave(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,'chave'))).send_keys(self.chave)
            
            iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title,'reCAPTCHA')]")))
            self.driver.switch_to.frame(iframe)

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()
            
            WebDriverWait(self.driver, 600).until(lambda d: d.find_element(By.ID, "recaptcha-anchor").get_attribute("aria-checked") == "true")

            self.driver.switch_to.default_content()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Consultar')]"))).click()

        except Exception:
            messagebox.showerror('Erro', f'Ocorreu um erro inesperado. Fechando navegador...')
            self.driver.quit()

    # Faz uma varredura no site (WebScrapping), buscando as informações de compra.
    def coleta_dados(self):
        try:
            # Aguarda o máximo de tempo para o usuário resolver o CAPTCHA
            WebDriverWait(self.driver, 600, poll_frequency=1).until(EC.presence_of_element_located((By.ID,'tabResult')))

            # Verifica se os valores da tabela estão carregados (Nome do produto, Valor unitário, Quantidade, etc)
            WebDriverWait(self.driver, 60, poll_frequency=1).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'txtTit')))

            linhas = self.driver.find_elements(By.CSS_SELECTOR,'#tabResult tbody tr')

            dados = []

            data = self.driver.find_element(By.XPATH, '//strong[contains(text(), "Data de Emissão")]/parent::li').text
            data = data.split("Data de Emissão:")[-1].split("\n")[0].split(" - ")[0].strip().split(" ")[0]

            estabelecimento = self.driver.find_element(By.ID, 'u20').text

            for linha in linhas:
                spans = linha.find_elements(By.CLASS_NAME,'txtTit')
        
                if spans:                
                
                    produto = linha.find_element(By.CLASS_NAME,'txtTit').text

                    quantidade = linha.find_element(By.CLASS_NAME,'Rqtd').text.replace('Qtde.:','').strip()
                    quantidade = quantidade.replace(".", ",")

                    grandeza = linha.find_element(By.CLASS_NAME,'RUN').text.replace('UN:','').strip()

                    valor_unitario = linha.find_element(By.CLASS_NAME,'RvlUnit').text
                    valor_unitario = valor_unitario.split(":")[-1].strip().replace(".", ",")

                    valor_total = linha.find_element(By.XPATH,'./td[2]').text
                    valor_total = valor_total.split("\n")[-1].replace(".", ",")

                    dados.append({
                        "data": data,
                        "estabelecimento": estabelecimento,
                        "produto": produto,
                        "grandeza": grandeza,
                        "quantidade_comprada": '-',
                        "valor_unitario": str(valor_unitario),
                        "quantidade": str(quantidade),
                        "valor_total": str(valor_total)
                    })

            # Transforma a lista em um DataFrame para converter em um arquivo .csv
            df = pd.DataFrame(dados)
            df.to_csv(f"data/notas_fiscais/nf_{self.chave[:44]}.csv",index=False,encoding="utf-8")

        except Exception:
            messagebox.showerror('Erro', f'Ocorreu um erro inesperado. Fechando navegador...')

        finally:
            self.driver.quit()

        return self.chave[:44]