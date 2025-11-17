import React, { useState, useEffect, useRef } from 'react';

interface MessagePayload {
  from: string;
  text: string;
}

function App() {
  const [myWindowId, setMyWindowId] = useState('unknown');
  const [messageLog, setMessageLog] = useState<string[]>([]);
  const [targetWindowId, setTargetWindowId] = useState('main_1');
  const [dataToSend, setDataToSend] = useState('');
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const winId = params.get('window_id') || 'main_1';
    setMyWindowId(winId);

    ws.current = new WebSocket(`ws://127.0.0.1:8000/ws/${winId}`);

    ws.current.onmessage = (event) => {
      setMessageLog((prev) => [...prev, `Odebrano: ${event.data}`]);
    };

    ws.current.onopen = () => {
      setMessageLog((prev) => [...prev, 'Połączono z WebSocket']);
    };

    return () => {
      ws.current?.close();
    };
  }, []);

  const createNewWindow = () => {
    fetch('http://127.0.0.1:8000/api/window/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: 'Nowe Okno' }),
    });
  };

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
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>ID Tego Okna: {myWindowId}</h1>
      <button onClick={createNewWindow}>Stwórz Nowe Okno</button>

      <hr style={{ margin: '20px 0' }} />

      <h2>Wyślij Dane</h2>
      <div>
        <label>ID Odbiorcy:</label>
        <input
          value={targetWindowId}
          onChange={(e) => setTargetWindowId(e.target.value)}
        />
      </div>
      <div>
        <label>Dane:</label>
        <input
          value={dataToSend}
          onChange={(e) => setDataToSend(e.target.value)}
        />
      </div>
      <button onClick={sendMessage}>Wyślij</button>

      <hr style={{ margin: '20px 0' }} />
      
      <h2>Log Wiadomości</h2>
      <div style={{ background: '#f0f0f0', minHeight: '100px', padding: '10px' }}>
        {messageLog.map((msg, index) => (
          <div key={index}>{msg}</div>
        ))}
      </div>
    </div>
  );
}

export default App;