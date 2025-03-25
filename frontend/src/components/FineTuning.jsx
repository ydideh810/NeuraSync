import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

const FineTuning = () => {
  const [epochs, setEpochs] = useState(3);
  const [batchSize, setBatchSize] = useState(4);
  const [loading, setLoading] = useState(false);
  const [executionTime, setExecutionTime] = useState(null);

  const handleFineTune = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/fine-tune', {
        epochs,
        batch_size: batchSize
      });

      setExecutionTime(response.data.execution_time);
      toast.success('Fine-tuning completed successfully!');

    } catch (error) {
      toast.error('Fine-tuning failed.');
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4">Fine-Tuning</h2>

      <div className="flex gap-4">
        <input type="number" value={epochs} onChange={(e) => setEpochs(e.target.value)} placeholder="Epochs" />
        <input type="number" value={batchSize} onChange={(e) => setBatchSize(e.target.value)} placeholder="Batch Size" />
      </div>

      <button onClick={handleFineTune} className="bg-blue-500 text-white px-4 py-2 mt-4 rounded">
        {loading ? 'Running...' : 'Start Fine-Tuning'}
      </button>

      {executionTime && (
        <div className="mt-4">
          <p>Execution Time: {executionTime.toFixed(2)}s</p>
        </div>
      )}
    </div>
  );
};

export default FineTuning;
