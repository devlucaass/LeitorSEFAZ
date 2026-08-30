[🇧🇷 Português](README.md) | 🇺🇸 English

# LeitorSEFAZ

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

Desktop application built in Python for querying electronic invoices (NFC-e) through the SEFAZ-PE portal. Data is automatically collected and stored in an Excel spreadsheet.

## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Interface](#interface)
- [Collected Data](#collected-data)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [Status](#status)
- [Author](#author)
- [License](#license)

## About the Project

LeitorSEFAZ was built to automate the process of querying electronic invoices (NFC-e) on the SEFAZ-PE portal and recording the information in an Excel spreadsheet, reducing the need for manual data entry.

## Features

- QR Code reading via camera.
- Manual entry of the access key or via QR Code.
- Automatic invoice lookup on SEFAZ-PE.
- Automatic data storage in an Excel spreadsheet.
- Support for multiple browsers: Firefox, Chrome, and Edge.

## Interface

![Main Screen](assets/screenshots/main_screen.png)

## Collected Data

- Issue date
- Establishment
- Product
- Unit of measurement
- Purchased quantity
- Unit price
- Quantity
- Total value

## Technologies Used

- Python
- OpenCV
- Selenium
- Xlwings
- Pillow
- Pyzbar
- CustomTkinter

## Prerequisites

- Python 3.10 or higher
- One of the supported browsers installed: Mozilla Firefox, Google Chrome, or Microsoft Edge
- Microsoft Excel installed on the computer (for xlwings integration)

## Installation

### Clone the repository
```powershell
git clone https://github.com/devlucaass/LeitorSEFAZ.git
cd LeitorSEFAZ
```

### Create the virtual environment
```powershell
python -m venv venv
```

### Activate the virtual environment (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```

### Install the dependencies
```powershell
pip install -r requirements.txt
```

### Run the project
```powershell
python src/main.py
```

## How to Use

1. Open the program.
2. Generate a spreadsheet template using the "Generate spreadsheet template" button.
3. Save the template wherever you prefer.
4. Go to settings.
5. Click "Locate spreadsheet" and select it.
6. Choose the browser you want to use (Firefox, Chrome, or Edge).
7. Save the settings and close the window.
8. Provide the cell you want to start from.
9. Choose how to provide the access key:
   - **QR Code**: click "Read QR Code" and point the camera at the invoice's code (no CAPTCHA required).
   - **Manual**: type the key into the field and click "Start" — you'll need to solve the site's CAPTCHA.
10. Wait for the spreadsheet to open automatically, or keep the template already open.

## Status

✅ Functional and under active development.

## Author

Developed by **Lucas Vinícius**

- GitHub: [@devlucaass](https://github.com/devlucaass)

## License

This project is licensed under the MIT License. See the LICENSE file for more details.