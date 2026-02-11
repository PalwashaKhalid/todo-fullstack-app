'use client';

import { useState, useEffect } from 'react';
import CreateTaskForm from '@/components/CreateTaskForm';
import TaskList from '@/components/TaskList';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchTasks = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setTasks(data.data);
        setError('');
      } else {
        setError(data.message || 'Failed to load tasks');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleTaskCreated = () => {
    fetchTasks();
  };

  const handleTaskUpdated = () => {
    fetchTasks();
  };

  const handleTaskDeleted = () => {
    fetchTasks();
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-600">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div className="px-4 py-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">My Tasks</h1>

        {error && (
          <div className="mb-6 rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-800">{error}</div>
          </div>
        )}

        <CreateTaskForm onTaskCreated={handleTaskCreated} />

        <TaskList
          tasks={tasks}
          onTaskUpdated={handleTaskUpdated}
          onTaskDeleted={handleTaskDeleted}
        />
      </div>
    </div>
  );
}
