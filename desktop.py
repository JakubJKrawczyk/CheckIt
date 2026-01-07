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

from updater import check_and_maybe_update

from bottle import debug

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.main import app

# POPRAWKA: Import musi pasować do Twojej struktury (utillities z dwoma 'l')
from backend.utillities.window_manager import window_manager

BACKEND_URL = "http://127.0.0.1:21370"
REACT_DEV_URL = "http://localhost:21371"

# Default update endpoint (remote EXE; version is extracted from filename)
DEFAULT_UPDATE_URL = "https://apps.jakubkrawczyk.com/checkit"


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
    uvicorn.run(app, host="127.0.0.1", port=21370, log_level="info")
    print("[BACKEND] running")


def run_startup_loader(task_fn):
    stop = threading.Event()

    def spinner():
        frames = ["|", "/", "-", "\\"]
        idx = 0
        while not stop.is_set():
            sys.stdout.write(f"\rChecking update... {frames[idx % len(frames)]}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.12)
        sys.stdout.write("\rChecking update... done.   \n")
        sys.stdout.flush()

    t = threading.Thread(target=spinner, daemon=True)
    t.start()
    try:
        task_fn()
    finally:
        stop.set()
        t.join(timeout=1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Uruchamia aplikację CheckIt z opcją trybu deweloperskiego.")
    parser.add_argument(
    '--dev',
    action='store_true',
    help='Uruchamia aplikację w trybie deweloperskim. Pywebview łączy się z serwerem Hot Reload Reacta (np. 5173).'
    )
    parser.add_argument(
    '--update-url',
    type=str,
    default=None,
    help='Pojedynczy URL do najnowszego EXE (wersja wyciągana z nazwy pliku).'
    )
    args = parser.parse_args()

    update_url = args.update_url or os.environ.get('CHECKIT_UPDATE_URL') or DEFAULT_UPDATE_URL

    def _do_update_check():
        # Downloads remote exe and updates if newer (only for packaged EXE)
        check_and_maybe_update(update_url=update_url, show_ui=True)

    run_startup_loader(_do_update_check)

 
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