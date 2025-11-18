/* eslint-disable @typescript-eslint/no-unused-vars */

import { useState, useEffect, useRef } from 'react';

interface MessagePayload {
  from: string;
  text: string;
}

function App() {
  const [myWindowId, _setMyWindowId] = useState(() => {
  const params = new URLSearchParams(window.location.search);
  return params.get('window_id') || 'main_1';
  });
  const [_messageLog, setMessageLog] = useState<string[]>([]);
  const [targetWindowId, _setTargetWindowId] = useState('main_1');
  const [dataToSend, setDataToSend] = useState('');
  const ws = useRef<WebSocket | null>(null);

   useEffect(() => {
    ws.current = new WebSocket(`ws://127.0.0.1:8000/ws/${myWindowId}`);

    ws.current.onmessage = (event) => {
      setMessageLog((prev) => [...prev, `Odebrano: ${event.data}`]);
    };

    ws.current.onopen = () => {
      setMessageLog((prev) => [...prev, 'Połączono z WebSocket']);
    };

    return () => {
      ws.current?.close();
    };
  }, [myWindowId]);

  // @ts-expect-error itis
  const createNewWindow = () => {
    fetch('http://127.0.0.1:8000/api/window/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: 'Nowe Okno' }),
    });
  };

  // @ts-expect-error itis
  const sendMessage = () => {
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      console.error("WebSocket nie jest połączony.");
      return;
    }

    const msg = {
      type: 'send_to_window',
      target: targetWindowId,
      payload: { from: myWindowId, text: dataToSend } as MessagePayload,
    };
    ws.current.send(JSON.stringify(msg));
    setDataToSend('');
  };

  return (
    <div>
      hujniaasdawd
    </div>
  );
}

export default App;