# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


pyzbar_path = Path("venv/Lib/site-packages/pyzbar")

binaries = [
    (str(pyzbar_path / "libiconv.dll"), "pyzbar"),
    (str(pyzbar_path / "libzbar-64.dll"), "pyzbar"),
]


a = Analysis(
    ["src/main.py"],
    pathex=[],
    binaries=binaries,
    datas=[
        ("assets/icons", "assets/icons"),
        ("assets/images", "assets/images"),
        ("src/config/settings.json", "config"),
    ],
    hiddenimports=[
        "selenium.webdriver.chrome.webdriver",
        "selenium.webdriver.firefox.webdriver",
        "selenium.webdriver.edge.webdriver",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="LeitorSEFAZ",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/icons/logo.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="LeitorSEFAZ",
)