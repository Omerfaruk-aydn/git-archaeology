import { apiClient } from './client';
import { Commit, CommitDetail, PaginatedResponse } from '../types';

export const commitApi = {
  list: (params: {
    repo_id: string;
    page?: number;
    page_size?: number;
    author?: string;
    start_date?: string;
    end_date?: string;
  }) => apiClient.get<PaginatedResponse<Commit>>('/commits', params),

  get: (sha: string, repoId: string) =>
    apiClient.get<CommitDetail>(`/commits/${sha}`, { repo_id: repoId }),

  analyze: (sha: string, repoId: string, focusAreas?: string[]) =>
    apiClient.post(`/commits/${sha}/analyze`, { repo_id: repoId, focus_areas: focusAreas }),

  explainChange: (sha: string, repoId: string, filePath: string) =>
    apiClient.get<{ explanation: string }>(`/commits/${sha}/explain`, {
      repo_id: repoId,
      file_path: filePath,
    }),
};
