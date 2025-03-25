import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';

const Benchmark = () => {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onmessage = (event) => {
      const newData = JSON.parse(event.data);

      const formattedData = newData.map((item, index) => ({
        name: item.device,
        throughput: item.throughput,
        latency: item.latency,
        memory: item.memory_usage,
        cpu: item.cpu_util,
        gpu: item.gpu_util
      }));

      setMetrics(formattedData);
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4">Benchmarking Metrics</h2>

      <LineChart width={800} height={400} data={metrics}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />

        <Line type="monotone" dataKey="throughput" stroke="#82ca9d" name="Throughput" />
        <Line type="monotone" dataKey="latency" stroke="#8884d8" name="Latency" />
        <Line type="monotone" dataKey="memory" stroke="#ffc658" name="Memory Usage" />
        <Line type="monotone" dataKey="cpu" stroke="#ff7300" name="CPU Utilization" />
        <Line type="monotone" dataKey="gpu" stroke="#00C49F" name="GPU Utilization" />
      </LineChart>
    </div>
  );
};

export default Benchmark;
