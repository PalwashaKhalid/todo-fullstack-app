'use client';

import { useState } from 'react';
import EditTaskModal from './EditTaskModal';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
  onTaskDeleted: () => void;
}

export default function TaskList({ tasks, onTaskUpdated, onTaskDeleted }: TaskListProps) {
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);

  const handleToggleComplete = async (taskId: number, currentStatus: boolean) => {
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${taskId}/status`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({ completed: !currentStatus }),
        }
      );

      if (response.ok) {
        onTaskUpdated();
      }
    } catch (err) {
      console.error('Failed to update task status:', err);
    }
  };

  const handleDelete = async (taskId: number) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setDeletingTaskId(taskId);

    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${taskId}`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (response.ok || response.status === 204) {
        onTaskDeleted();
      }
    } catch (err) {
      console.error('Failed to delete task:', err);
    } finally {
      setDeletingTaskId(null);
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="bg-white shadow rounded-lg p-8 text-center">
        <p className="text-gray-500">No tasks yet. Create your first task above!</p>
      </div>
    );
  }

  return (
    <>
      <div className="bg-white shadow rounded-lg divide-y divide-gray-200">
        {tasks.map((task) => (
          <div
            key={task.id}
            className="p-4 hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => handleToggleComplete(task.id, task.completed)}
                className="mt-1 h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
              />

              <div className="flex-1 min-w-0">
                <h3
                  className={`text-lg font-medium ${
                    task.completed
                      ? 'line-through text-gray-400'
                      : 'text-gray-900'
                  }`}
                >
                  {task.title}
                </h3>
                {task.description && (
                  <p
                    className={`mt-1 text-sm ${
                      task.completed ? 'text-gray-400' : 'text-gray-600'
                    }`}
                  >
                    {task.description}
                  </p>
                )}
                <p className="mt-2 text-xs text-gray-400">
                  Created: {new Date(task.created_at).toLocaleString()}
                </p>
              </div>

              <div className="flex space-x-2">
                <button
                  onClick={() => setEditingTask(task)}
                  className="px-3 py-1 text-sm font-medium text-blue-600 hover:text-blue-800 focus:outline-none"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(task.id)}
                  disabled={deletingTaskId === task.id}
                  className="px-3 py-1 text-sm font-medium text-red-600 hover:text-red-800 focus:outline-none disabled:opacity-50"
                >
                  {deletingTaskId === task.id ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {editingTask && (
        <EditTaskModal
          task={editingTask}
          onClose={() => setEditingTask(null)}
          onTaskUpdated={() => {
            setEditingTask(null);
            onTaskUpdated();
          }}
        />
      )}
    </>
  );
}
