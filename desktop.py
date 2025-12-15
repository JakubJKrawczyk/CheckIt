import asyncio
import argparse
import logging

import requests
import uvicorn
import webview
import threading
import sys
import os
import time

from bottle import debug

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.main import app

# POPRAWKA: Import musi pasować do Twojej struktury (utillities z dwoma 'l')
from backend.utillities.window_manager import window_manager

BACKEND_URL = "http://127.0.0.1:8000"
REACT_DEV_URL = "http://localhost:5173"

def check_react_server(url):
    for i in range(1,10):
        try:
            response = requests.get(REACT_DEV_URL)
            if response.status_code == 200:
                return
        except requests.ConnectionError:
            pass
        time.sleep(5)
    logging.error("Front nie został uruchomiony! Uruchom front i spróbuj ponownie.")
    sys.exit(1)



def start_backend_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    print("[BACKEND] running")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Uruchamia aplikację CheckIt z opcją trybu deweloperskiego.")
    parser.add_argument(
    '--dev',
    action='store_true',
    help='Uruchamia aplikację w trybie deweloperskim. Pywebview łączy się z serwerem Hot Reload Reacta (np. 5173).'
    )
    args = parser.parse_args()

 
    t = threading.Thread(target=start_backend_server)
    t.daemon = True
    t.start()

    url_to_load = BACKEND_URL

    if args.dev:
        print("Uruchamianie serwera FRONTEND: " + REACT_DEV_URL)
        url_to_load = REACT_DEV_URL

        t_check = threading.Thread(target=check_react_server, args=(url_to_load,))
        t_check.start()
        t_check.join()
        

    asyncio.run(window_manager.create_window(
        title="CheckIt",
        url=url_to_load,
        width=1200,
        height=1000
    ))
    webview.start(debug=True)