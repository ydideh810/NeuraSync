import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactFlow from 'react-flow-renderer';

const ModelVisualization = () => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onmessage = (event) => {
      const newData = JSON.parse(event.data);
      setData(newData);
    };

    return () => {
      socket.close();
    };
  }, []);

  const elements = data.map((layer, index) => ({
    id: `layer-${index}`,
    data: { label: `${layer.layer} (${layer.memory_usage}GB)` },
    position: { x: Math.random() * 400, y: Math.random() * 400 }
  }));

  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold">Model Sharding Visualization</h2>
      <div className="h-96">
        <ReactFlow elements={elements} />
      </div>
      <img src="http://localhost:8000/static/sharding_graph.png" alt="Sharding Graph" className="w-full mt-4" />
    </div>
  );
};

export default ModelVisualization;
