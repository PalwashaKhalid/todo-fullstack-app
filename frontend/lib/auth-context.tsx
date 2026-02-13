'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from './api-client';

interface User {
  id: number;
  email: string;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  signin: (email: string, password: string) => Promise<{ success: boolean; message?: string }>;
  signup: (email: string, password: string) => Promise<{ success: boolean; message?: string }>;
  signout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  // Start with false to avoid hydration issues - we'll load auth state immediately on mount
  const [isLoading, setIsLoading] = useState(false);

  // Load token from cookies on mount
  useEffect(() => {
    // Only run on client side
    if (typeof window === 'undefined') return;

    try {
      // Get token from cookie
      const cookies = document.cookie.split(';');
      const tokenCookie = cookies.find(c => c.trim().startsWith('auth_token='));
      const userCookie = cookies.find(c => c.trim().startsWith('auth_user='));

      if (tokenCookie && userCookie) {
        const storedToken = tokenCookie.split('=')[1];
        const storedUser = decodeURIComponent(userCookie.split('=')[1]);

        setToken(storedToken);
        setUser(JSON.parse(storedUser));
        apiClient.setToken(storedToken);
      }
    } catch (error) {
      console.error('Error loading auth from cookies:', error);
    }
  }, []);

  const signin = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/api/auth/signin', { email, password });

      if (response.success && response.data) {
        const { token: newToken, user: newUser } = response.data;
        setToken(newToken);
        setUser(newUser);
        apiClient.setToken(newToken);

        // Persist to cookies (expires in 7 days)
        const expires = new Date();
        expires.setDate(expires.getDate() + 7);
        document.cookie = `auth_token=${newToken}; path=/; expires=${expires.toUTCString()}`;
        document.cookie = `auth_user=${encodeURIComponent(JSON.stringify(newUser))}; path=/; expires=${expires.toUTCString()}`;

        return { success: true };
      }

      return { success: false, message: response.message || 'Sign in failed' };
    } catch (error) {
      return { success: false, message: 'Network error' };
    }
  };

  const signup = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/api/auth/signup', { email, password });

      if (response.success && response.data) {
        const { token: newToken, user: newUser } = response.data;
        setToken(newToken);
        setUser(newUser);
        apiClient.setToken(newToken);

        // Persist to cookies (expires in 7 days)
        const expires = new Date();
        expires.setDate(expires.getDate() + 7);
        document.cookie = `auth_token=${newToken}; path=/; expires=${expires.toUTCString()}`;
        document.cookie = `auth_user=${encodeURIComponent(JSON.stringify(newUser))}; path=/; expires=${expires.toUTCString()}`;

        return { success: true };
      }

      return { success: false, message: response.message || 'Sign up failed' };
    } catch (error) {
      return { success: false, message: 'Network error' };
    }
  };

  const signout = () => {
    setToken(null);
    setUser(null);
    apiClient.setToken(null);

    // Clear cookies
    document.cookie = 'auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    document.cookie = 'auth_user=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, signin, signup, signout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
