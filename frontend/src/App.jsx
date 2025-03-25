import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import RecoveryStatus from './components/RecoveryStatus';
import Checkpoint from './components/Checkpoint';
import TaskStatus from './components/TaskStatus';
import DeviceStatus from './components/DeviceStatus';

import './styles/global.css';

const App = () => {
  const [metrics, setMetrics] = useState([]);
  const [checkpoints, setCheckpoints] = useState([]);
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch metrics, checkpoint, and device data periodically
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [metricsRes, checkpointRes, deviceRes] = await Promise.all([
          axios.get('http://localhost:8000/api/metrics'),
          axios.get('http://localhost:8000/api/checkpoints'),
          axios.get('http://localhost:8000/api/devices')
        ]);

        setMetrics(metricsRes.data);
        setCheckpoints(checkpointRes.data);
        setDevices(deviceRes.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to fetch data');
        toast.error('Failed to fetch metrics data.');
        setLoading(false);
      }
    };

    const interval = setInterval(fetchData, 5000);  // Update every 5 seconds
    fetchData();

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="loading-screen">🚀 Loading data...</div>;
  }

  if (error) {
    return <div className="error-screen">❌ {error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <ToastContainer />

      {/* Header */}
      <header className="text-center mb-8">
        <h1 className="text-5xl font-extrabold text-blue-400">🔥 NEURA-SYNC Community Edition</h1>
        <p className="text-gray-400 mt-2">Decentralized Distributed AI Platform</p>
      </header>

      {/* Dashboard Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        {/* Recovery Status */}
        <div className="col-span-1">
          <RecoveryStatus />
        </div>

        {/* Checkpointing */}
        <div className="col-span-1">
          {checkpoints.length > 0 ? (
            checkpoints.map((chkpt, idx) => (
              <Checkpoint
                key={idx}
                taskId={chkpt.task_id}
                checkpointPath={chkpt.model_path}
              />
            ))
          ) : (
            <p className="text-gray-400">No checkpoints available</p>
          )}
        </div>

        {/* Device Metrics */}
        <div className="col-span-1">
          <DeviceStatus devices={devices} />
        </div>

        {/* Task Status */}
        <div className="col-span-2">
          <TaskStatus metrics={metrics} />
        </div>
      </div>

      {/* Footer */}
      <footer className="text-center text-gray-500 mt-10">
        Ⓒ 2025 NEURA-SYNC Community Edition | Distributed AI Platform
      </footer>
    </div>
  );
};

export default App;
