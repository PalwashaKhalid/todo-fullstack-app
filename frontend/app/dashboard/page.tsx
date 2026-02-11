'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import { apiClient } from '@/lib/api-client';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const { user, signout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
  const [editTaskTitle, setEditTaskTitle] = useState('');
  const [editTaskDescription, setEditTaskDescription] = useState('');

  // Redirect if not authenticated
  useEffect(() => {
    if (!user) {
      router.push('/login');
    }
  }, [user, router]);

  // Fetch tasks
  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user, filter]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const url = filter === 'all'
        ? '/api/tasks/'
        : `/api/tasks/?completed=${filter === 'completed'}`;

      const response = await apiClient.get(url);

      if (response.success) {
        setTasks(response.data);
      } else {
        setError('Failed to load tasks');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      setError('Task title is required');
      return;
    }

    try {
      const response = await apiClient.post('/api/tasks/', {
        title: newTaskTitle,
        description: newTaskDescription || null,
        completed: false
      });

      if (response.success) {
        setNewTaskTitle('');
        setNewTaskDescription('');
        setShowAddForm(false);
        fetchTasks();
      } else {
        setError(response.message || 'Failed to create task');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  const handleToggleComplete = async (taskId: number, currentStatus: boolean) => {
    try {
      const response = await apiClient.patch(`/api/tasks/${taskId}/status`, {
        completed: !currentStatus
      });

      if (response.success) {
        fetchTasks();
      }
    } catch (err) {
      setError('Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await apiClient.delete(`/api/tasks/${taskId}`);
      fetchTasks();
    } catch (err) {
      setError('Failed to delete task');
    }
  };

  const handleStartEdit = (task: Task) => {
    setEditingTaskId(task.id);
    setEditTaskTitle(task.title);
    setEditTaskDescription(task.description || '');
  };

  const handleCancelEdit = () => {
    setEditingTaskId(null);
    setEditTaskTitle('');
    setEditTaskDescription('');
  };

  const handleUpdateTask = async (taskId: number) => {
    if (!editTaskTitle.trim()) {
      setError('Task title is required');
      return;
    }

    try {
      const response = await apiClient.put(`/api/tasks/${taskId}`, {
        title: editTaskTitle,
        description: editTaskDescription || null
      });

      if (response.success) {
        setEditingTaskId(null);
        setEditTaskTitle('');
        setEditTaskDescription('');
        fetchTasks();
      } else {
        setError(response.message || 'Failed to update task');
      }
    } catch (err) {
      setError('Failed to update task');
    }
  };

  const handleSignout = () => {
    signout();
    router.push('/login');
  };

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Task Dashboard</h1>
            <p className="text-sm text-gray-600">{user.email}</p>
          </div>
          <button
            onClick={handleSignout}
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-md"
          >
            Sign Out
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Message */}
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-800">{error}</div>
          </div>
        )}

        {/* Add Task Button */}
        <div className="mb-6">
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md"
          >
            {showAddForm ? 'Cancel' : '+ Add Task'}
          </button>
        </div>

        {/* Add Task Form */}
        {showAddForm && (
          <div className="mb-6 bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Create New Task</h2>
            <form onSubmit={handleAddTask}>
              <div className="mb-4">
                <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                  Title *
                </label>
                <input
                  type="text"
                  id="title"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter task title"
                  maxLength={200}
                />
              </div>
              <div className="mb-4">
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  id="description"
                  value={newTaskDescription}
                  onChange={(e) => setNewTaskDescription(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter task description (optional)"
                  rows={3}
                  maxLength={2000}
                />
              </div>
              <button
                type="submit"
                className="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md"
              >
                Create Task
              </button>
            </form>
          </div>
        )}

        {/* Filter Tabs */}
        <div className="mb-6 border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setFilter('all')}
              className={`${
                filter === 'all'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              All Tasks
            </button>
            <button
              onClick={() => setFilter('active')}
              className={`${
                filter === 'active'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Active
            </button>
            <button
              onClick={() => setFilter('completed')}
              className={`${
                filter === 'completed'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Completed
            </button>
          </nav>
        </div>

        {/* Task List */}
        {loading ? (
          <div className="text-center py-12">
            <div className="text-gray-600">Loading tasks...</div>
          </div>
        ) : tasks.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-600">No tasks found. Create your first task!</div>
          </div>
        ) : (
          <div className="space-y-4">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow"
              >
                {editingTaskId === task.id ? (
                  // Edit Mode
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Title *
                      </label>
                      <input
                        type="text"
                        value={editTaskTitle}
                        onChange={(e) => setEditTaskTitle(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        maxLength={200}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Description
                      </label>
                      <textarea
                        value={editTaskDescription}
                        onChange={(e) => setEditTaskDescription(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        rows={3}
                        maxLength={2000}
                      />
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleUpdateTask(task.id)}
                        className="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-md"
                      >
                        Save
                      </button>
                      <button
                        onClick={handleCancelEdit}
                        className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-md"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  // View Mode
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3 flex-1">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => handleToggleComplete(task.id, task.completed)}
                        className="mt-1 h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
                      />
                      <div className="flex-1">
                        <h3
                          className={`text-lg font-medium ${
                            task.completed ? 'line-through text-gray-500' : 'text-gray-900'
                          }`}
                        >
                          {task.title}
                        </h3>
                        {task.description && (
                          <p className="mt-1 text-sm text-gray-600">{task.description}</p>
                        )}
                        <p className="mt-2 text-xs text-gray-400">
                          Created: {new Date(task.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex space-x-2 ml-4">
                      <button
                        onClick={() => handleStartEdit(task)}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        className="text-red-600 hover:text-red-800 text-sm font-medium"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
