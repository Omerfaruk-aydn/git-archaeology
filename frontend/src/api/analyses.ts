import { apiClient } from './client';
import { Analysis, AnalysisResult, AnalysisConfig, PaginatedResponse } from '../types';

export const analysisApi = {
  list: (params?: { repo_id?: string; status?: string; page?: number; page_size?: number }) =>
    apiClient.get<PaginatedResponse<Analysis>>('/analyses', params),

  get: (id: string) =>
    apiClient.get<Analysis>(`/analyses/${id}`),

  create: (config: AnalysisConfig) =>
    apiClient.post<Analysis>('/analyses', config),

  getResult: (id: string) =>
    apiClient.get<AnalysisResult>(`/analyses/${id}/result`),

  delete: (id: string) =>
    apiClient.delete(`/analyses/${id}`),
};
