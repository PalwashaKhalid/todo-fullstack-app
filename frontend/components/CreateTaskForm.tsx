'use client';

import { useState } from 'react';

interface CreateTaskFormProps {
  onTaskCreated: () => void;
}

export default function CreateTaskForm({ onTaskCreated }: CreateTaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!title.trim()) {
      setError('Task title is required');
      return;
    }

    if (title.length > 200) {
      setError('Task title must be 200 characters or less');
      return;
    }

    if (description && description.length > 2000) {
      setError('Task description must be 2000 characters or less');
      return;
    }

    setIsSubmitting(true);

    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim() || null,
        }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // Clear form
        setTitle('');
        setDescription('');
        setError('');
        // Notify parent to refresh task list
        onTaskCreated();
      } else {
        setError(data.message || 'Failed to create task');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 mb-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Create New Task</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-800">{error}</div>
          </div>
        )}

        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter task title"
            maxLength={200}
          />
          <p className="mt-1 text-xs text-gray-500">{title.length}/200 characters</p>
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description (optional)
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Enter task description"
            maxLength={2000}
          />
          <p className="mt-1 text-xs text-gray-500">{description.length}/2000 characters</p>
        </div>

        <button
          type="submit"
          disabled={isSubmitting || !title.trim()}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting ? 'Creating...' : 'Create Task'}
        </button>
      </form>
    </div>
  );
}
