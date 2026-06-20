import { apiClient } from './client';
import { Repository, PaginatedResponse } from '../types';

export const repositoryApi = {
  list: (params?: { page?: number; page_size?: number; search?: string }) =>
    apiClient.get<PaginatedResponse<Repository>>('/repositories', params),

  get: (id: string) =>
    apiClient.get<Repository>(`/repositories/${id}`),

  create: (data: { name: string; url: string; description?: string; default_branch?: string }) =>
    apiClient.post<Repository>('/repositories', data),

  update: (id: string, data: Partial<Repository>) =>
    apiClient.put<Repository>(`/repositories/${id}`, data),

  delete: (id: string) =>
    apiClient.delete(`/repositories/${id}`),

  clone: (id: string) =>
    apiClient.post(`/repositories/${id}/clone`),

  sync: (id: string) =>
    apiClient.post(`/repositories/${id}/sync`),
};
