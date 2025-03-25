import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const LoadBalancer = () => {
  const [deviceStatus, setDeviceStatus] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchDeviceStatus = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/device-status');
      setDeviceStatus(response.data);
    } catch (error) {
      console.error('Failed to fetch device status:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchDeviceStatus();
  }, []);

  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4">Load Balancer</h2>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={deviceStatus}>
          <XAxis dataKey="device" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="cpu" fill="#82ca9d" name="CPU" />
          <Bar dataKey="gpu" fill="#8884d8" name="GPU" />
          <Bar dataKey="memory" fill="#ffc658" name="Memory" />
        </BarChart>
      </ResponsiveContainer>

      {loading && <p>Loading...</p>}
    </div>
  );
};

export default LoadBalancer;
