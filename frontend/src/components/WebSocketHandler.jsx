
import { useEffect, useState } from 'react';

const WebSocketHandler = ({ onUpdate }) => {
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onopen = () => console.log('Connected to WebSocket');
    ws.onmessage = (event) => onUpdate(JSON.parse(event.data));
    ws.onclose = () => console.log('Disconnected from WebSocket');

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, [onUpdate]);

  return null;
};

export default WebSocketHandler;
