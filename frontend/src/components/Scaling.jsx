import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Scaling = () => {
  const [scaling, setScaling] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onmessage = (event) => {
      const newData = JSON.parse(event.data);
      setScaling(newData);
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4">Scaling & Rebalancing Actions</h2>

      <div className="grid grid-cols-1 gap-4">
        {scaling.map((action, index) => (
          <div key={index} className={`p-3 rounded-md shadow-md ${
            action[1] === "SCALE_UP" ? "bg-green-500" : "bg-red-500"
          }`}>
            <p>Device: <strong>{action[0]}</strong></p>
            <p>Action: <strong>{action[1]}</strong></p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Scaling;
