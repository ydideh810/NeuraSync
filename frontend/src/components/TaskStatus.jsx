import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TaskStatus = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axios.get('http://localhost:8000/metrics');
        const taskData = response.data.tasks;

        const formattedTasks = Object.keys(taskData).map((taskId) => ({
          id: taskId,
          status: taskData[taskId],
        }));

        setTasks(formattedTasks);
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
      }
    };

    fetchTasks();
    const interval = setInterval(fetchTasks, 2000);  // Update every 2s

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4">Task Status</h2>
      <div className="overflow-y-auto h-60">
        {tasks.length > 0 ? (
          <ul>
            {tasks.map((task) => (
              <li
                key={task.id}
                className={`p-2 rounded ${
                  task.status === 'Success'
                    ? 'bg-green-500'
                    : task.status === 'Running'
                    ? 'bg-yellow-500'
                    : 'bg-red-500'
                }`}
              >
                Task {task.id} – {task.status}
              </li>
            ))}
          </ul>
        ) : (
          <p>No tasks running</p>
        )}
      </div>
    </div>
  );
};

export default TaskStatus;
