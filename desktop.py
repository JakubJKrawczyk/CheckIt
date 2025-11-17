import uvicorn
import webview
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.main import app

# POPRAWKA: Import musi pasować do Twojej struktury (utillities z dwoma 'l')
from backend.utillities.window_manager import window_manager

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    window_manager.create_window(
        title="Główne Okno",
        url="http://127.0.0.1:8000/"
    )

    # POPRAWKA: Uruchom pywebview w głównym wątku
    webview.start()