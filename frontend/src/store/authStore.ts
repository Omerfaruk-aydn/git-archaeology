import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '../api/client';
import { User, AuthTokens } from '../types';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [tokens, setTokens] = useState<AuthTokens | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedTokens = apiClient.getTokens();
    if (storedTokens) {
      setTokens(storedTokens);
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const userData = await apiClient.get<User>('/auth/me');
      setUser(userData);
    } catch (error) {
      console.error('Kullanıcı bilgileri alınamadı:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response = await apiClient.post<AuthTokens>('/auth/login', {
      email,
      password,
    });
    setTokens(response);
    apiClient.setTokens(response);
    await fetchUser();
  };

  const register = async (email: string, username: string, password: string) => {
    const response = await apiClient.post<AuthTokens>('/auth/register', {
      email,
      username,
      password,
    });
    setTokens(response);
    apiClient.setTokens(response);
    await fetchUser();
  };

  const logout = useCallback(() => {
    setTokens(null);
    setUser(null);
    apiClient.setTokens(null);
  }, []);

  return {
    user,
    tokens,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!tokens,
  };
}
