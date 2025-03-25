import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from 'recharts';

const TaskHistory = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await axios.get('http://localhost:8000/history');
        setHistory(response.data);
      } catch (error) {
        console.error('Failed to fetch task history:', error);
      }
    };

    fetchHistory();
  }, []);

  const formatDataForChart = () => {
    return history.map((item, index) => ({
      name: `Task ${index + 1}`,
      execution_time: item.execution_time,
      status: item.status === "Success" ? 1 : 0
    }));
  };

  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4">Task History</h2>

      <BarChart width={600} height={300} data={formatDataForChart()}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="execution_time" fill="#8884d8" name="Execution Time (s)" />
        <Bar dataKey="status" fill="#82ca9d" name="Success (1) / Fail (0)" />
      </BarChart>
    </div>
  );
};

export default TaskHistory;
