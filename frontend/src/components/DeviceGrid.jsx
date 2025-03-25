import React from 'react';

const DeviceGrid = ({ devices }) => {
  return (
    <div className="grid grid-cols-4 gap-4">
      {devices.map((device, index) => (
        <div key={index} className="p-4 bg-gray-800 rounded-lg shadow-lg">
          <h3 className="text-lg font-bold">{device.name}</h3>
          <p>CPU: {device.cpu}%</p>
          <p>RAM: {device.ram}%</p>
          <p>GPU: {device.gpu}</p>
        </div>
      ))}
    </div>
  );
};

export default DeviceGrid;
