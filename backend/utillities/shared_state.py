import json
from backend.models.window import window
class SharedState:
    def __init__(self):
        self.subscribers = {}
        self.windows = []

    async def add_subscriber(self, window_id, websocket):
        self.subscribers[window_id] = websocket

    async def remove_subscriber(self, window_id):
        if window_id in self.subscribers:
            del self.subscribers[window_id]

    async def send_to_window(self, window_id, payload):
        if window_id in self.subscribers:
            await self.subscribers[window_id].send_text(json.dumps(payload))
            return True
        return False

shared_state = SharedState()