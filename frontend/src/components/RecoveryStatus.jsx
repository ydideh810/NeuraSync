import React, { useState, useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const RecoveryStatus = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onmessage = (event) => {
      const task = JSON.parse(event.data);

      setEvents((prevEvents) => [task, ...prevEvents]);

      if (task.status === 'FAILED') {
        toast.error(`Task ${task.task_id} FAILED on ${task.device}`);
      } else if (task.status === 'RECOVERED') {
        toast.success(`Task ${task.task_id} RECOVERED on ${task.device}`);
      }
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4">Real-Time Recovery Status</h2>
      <ToastContainer />

      <ul className="space-y-2">
        {events.map((event, index) => (
          <li
            key={index}
            className={`p-2 rounded-lg ${event.status === 'FAILED' ? 'bg-red-500' : 'bg-green-500'}`}
          >
            <strong>Task ID:</strong> {event.task_id} <br />
            <strong>Device:</strong> {event.device} <br />
            <strong>Status:</strong> {event.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RecoveryStatus;
