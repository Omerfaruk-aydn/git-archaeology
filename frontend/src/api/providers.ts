import { apiClient } from './client';

export interface LLMProvider {
  name: string;
  display_name: string;
  description: string;
  website: string;
  available: boolean;
}

export const providersApi = {
  list: async (): Promise<{ providers: LLMProvider[]; count: number }> => {
    const response = await apiClient.get('/llm/providers');
    return response.data;
  },

  listAvailable: async (): Promise<{ providers: string[]; count: number }> => {
    const response = await apiClient.get('/llm/providers/available');
    return response.data;
  },
};
