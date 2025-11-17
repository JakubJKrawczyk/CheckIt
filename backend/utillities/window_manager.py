import webview

class WindowManager:
    def __init__(self):
        self._next_id = 1

    def generate_window_id(self, prefix="window"):
        window_id = f"{prefix}_{self._next_id}"
        self._next_id += 1
        return window_id

    def create_window(self, title, url):

        window_id = self.generate_window_id("main")

        config = {
            "title": title,
            "url": f"{url}?window_id={window_id}",
            "width": 800,
            "height": 600,
        }

        webview.create_window(**config)

        return window_id

window_manager = WindowManager()