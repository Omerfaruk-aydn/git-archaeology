import { apiClient } from './client';
import { Report, PaginatedResponse } from '../types';

export const reportApi = {
  generate: (data: {
    repository_id: string;
    report_type: string;
    branch?: string;
    start_date?: string;
    end_date?: string;
    file_paths?: string[];
    format?: string;
  }) => apiClient.post<Report>('/reports', data),

  getArcheologicalReport: (repoId: string, filePath: string) =>
    apiClient.get<{ content: string; format: string }>(`/reports/${repoId}/archeological/${filePath}`),
};
