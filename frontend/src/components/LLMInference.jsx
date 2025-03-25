import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

const LLMInference = () => {
  const [prompt, setPrompt] = useState('');
  const [output, setOutput] = useState('');
  const [executionTime, setExecutionTime] = useState(0);
  const [loading, setLoading] = useState(false);

  const handleInference = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/infer', { prompt });

      setOutput(response.data.output);
      setExecutionTime(response.data.execution_time);
      toast.success('Inference completed successfully!');

    } catch (error) {
      toast.error('Inference failed.');
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4">LLM Inference</h2>

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows="5"
        className="w-full p-2 rounded border-gray-700 bg-gray-800 text-white"
        placeholder="Enter prompt..."
      />

      <button
        onClick={handleInference}
        className="bg-blue-500 text-white px-4 py-2 rounded mt-4"
        disabled={loading}
      >
        {loading ? 'Running...' : 'Run Inference'}
      </button>

      {output && (
        <div className="mt-6">
          <h3 className="text-lg font-bold">Output:</h3>
          <p className="p-4 bg-gray-800 rounded">{output}</p>
          <p className="text-sm">Execution Time: {executionTime.toFixed(2)}s</p>
        </div>
      )}
    </div>
  );
};

export default LLMInference;
