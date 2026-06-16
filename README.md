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
- Valor total da nota
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
2. Forneça a célula pela qual quer iniciar
3. Leia o QR Code ou insira a chave da nota manualmente
4. Exporte para o Excel (automático)

## Estrutura do Projeto

```text
LeitorSEFAZ/
├── assets/                 # Ícones e recursos visuais
├── src/
│   ├── config/             # Configurações da aplicação
│   │   ├── settings.json
│   │   └── config_manager.py
│   │
│   ├── services/           # Regras de negócio e automações
│   │   ├── excel_service.py
│   │   └── sefaz_service.py
│   │
│   ├── ui/                 # Interface gráfica
│   │   └── application.py
│   │
│   ├── utils/              # Funções auxiliares e validações
│   │   └── validators.py
│   │
│   └── main.py             # Ponto de entrada da aplicação
│
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
```

A aplicação segue uma arquitetura simples baseada em separação de responsabilidades:

- **config**: gerenciamento das configurações do sistema.
- **services**: comunicação com a SEFAZ e integração com Excel.
- **ui**: interface gráfica desenvolvida com CustomTkinter.
- **utils**: funções auxiliares e validações reutilizáveis.
- **assets**: recursos visuais utilizados pela aplicação.

## Status

✅ Funcional e em desenvolvimento ativo.

## Autor

Desenvolvido por **Lucas Vinícius**

- GitHub: [@devlucaass](https://github.com/devlucaass)

## Licença

MIT