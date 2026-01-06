# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Zbierz wszystkie submoduły uvicorn
uvicorn_imports = collect_submodules('uvicorn')

# Zbierz wszystkie submoduły i ewentualne dane openpyxl (pandas engine dla .xlsx)
openpyxl_imports = collect_submodules('openpyxl')
openpyxl_datas = collect_data_files('openpyxl')

a = Analysis(
    ['desktop.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/dist', 'frontend/dist'),  # React build (Vite używa 'dist')
        ('backend', 'backend'),              # Cały backend folder
    ] + openpyxl_datas,
    hiddenimports=[
        # PyWebView
        'webview',
        'webview.platforms.winforms',  # Windows
        
        # FastAPI i Starlette
        'fastapi',
        'starlette',
        'starlette.applications',
        'starlette.middleware',
        'starlette.middleware.cors',
        'starlette.routing',
        'starlette.responses',
        'starlette.websockets',
        
        # Uvicorn
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.http.h11_impl',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.protocols.websockets.wsproto_impl',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        
        # Pydantic
        'pydantic',
        'pydantic_core',
        'pydantic.deprecated',
        'pydantic.json_schema',
        
        # Pandas i Excel
        'pandas',
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.cell._writer',
        'xlrd',
        'et_xmlfile',
        
        # Inne
        'asyncio',
        'json',
        'threading',
        'tkinter',
        'requests',
        'concurrent.futures',
        'tkinter.filedialog',
    ] + uvicorn_imports + openpyxl_imports,
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
    a.binaries,
    a.datas,
    [],
    name='CheckIt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Zmień na True do debugowania, potem False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Dodaj 'icon.ico' jeśli masz
)