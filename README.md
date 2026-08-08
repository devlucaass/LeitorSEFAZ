# LeitorSEFAZ

Aplicação desktop desenvolvida em Python para consulta de notas fiscais através do portal da SEFAZ-PE. Os dados são coletados automaticamente e armazenados em uma planilha Excel.

## Sobre o Projeto

O LeitorSEFAZ foi desenvolvido para automatizar o processo de consulta de notas fiscais eletrônicas no portal da SEFAZ-PE e registrar as informações em uma planilha Excel, reduzindo a necessidade de preenchimento manual.

## Funcionalidades

- Leitura de QR Code pela câmera.
- Inserção manual da chave de acesso ou via QR Code.
- Consulta automática de notas fiscais na SEFAZ-PE.
- Armazenamento automático dos dados em planilha Excel.

## Interface

![Tela Principal](assets/screenshots/main_screen.png)

## Dados Coletados

- Chave de acesso
- Data de emissão
- Valor total dos itens
- Informações do emitente

## Tecnologias Utilizadas

- Python
- OpenCV
- Selenium
- Xlwings
- Pillow
- Pyzbar
- CustomTkinter

## Instalação

### Clone o repositório
```powershell
git clone https://github.com/devlucaass/LeitorSEFAZ.git
cd LeitorSEFAZ
```

### Crie o ambiente virtual
```powershell
python -m venv venv
```
### Ative o ambiente virtual (Powershell)
```powershell
.\venv\Scripts\Activate.ps1
```

### Instale as dependências
```powershell
pip install -r requirements.txt
```

### Execute o projeto
```powershell
python src/main.py
```

## Como Utilizar

1. Abra o programa
2. Gere uma planilha modelo no botão "Gerar modelo de planilha"
3. Salve a planilha modelo onde preferir
4. Vá em configurações
5. Clique em "Localizar planilha" e selecione ela
6. Salve as configurações e feche a janela
7. Forneça a célula pela qual quer iniciar
8. Leia o QR Code ou insira a chave da nota manualmente (OBS.: se inserir manualmente, resolva o CAPTCHA do site)
9. Aguarde a planilha abrir sozinha ou deixe a planilha modelo aberta

## Status

✅ Funcional e em desenvolvimento ativo.

## Autor

Desenvolvido por **Lucas Vinícius**

- GitHub: [@devlucaass](https://github.com/devlucaass)

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
