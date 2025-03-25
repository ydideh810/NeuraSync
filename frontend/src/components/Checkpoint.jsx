import React from 'react';

const Checkpoint = ({ taskId, checkpointPath }) => {
  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold">Checkpoint Info</h2>
      <p>Task ID: {taskId}</p>
      <p>Checkpoint Path: {checkpointPath}</p>
    </div>
  );
};

export default Checkpoint;
