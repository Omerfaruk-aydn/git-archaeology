import { useState, useEffect, useCallback } from 'react';
import { analysisApi } from '../api/analyses';
import { Analysis, AnalysisResult, AnalysisConfig, PaginatedResponse } from '../types';

export function useAnalysis(id?: string) {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalysis = useCallback(async () => {
    if (!id) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await analysisApi.get(id);
      setAnalysis(data);

      if (data.status === 'completed') {
        const resultData = await analysisApi.getResult(id);
        setResult(resultData);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analiz yüklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchAnalysis();
  }, [fetchAnalysis]);

  const refresh = useCallback(async () => {
    if (!id) return;
    try {
      const data = await analysisApi.get(id);
      setAnalysis(data);

      if (data.status === 'completed') {
        const resultData = await analysisApi.getResult(id);
        setResult(resultData);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analiz güncellenirken hata oluştu');
    }
  }, [id]);

  return {
    analysis,
    result,
    loading,
    error,
    refresh,
  };
}

export function useAnalysisList(repoId?: string) {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);

  const fetchAnalyses = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await analysisApi.list({
        repo_id: repoId,
        page,
        page_size: 20,
      });
      setAnalyses(response.items);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analizler yüklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  }, [repoId, page]);

  useEffect(() => {
    fetchAnalyses();
  }, [fetchAnalyses]);

  const startAnalysis = async (config: AnalysisConfig) => {
    try {
      const newAnalysis = await analysisApi.create(config);
      setAnalyses((prev) => [newAnalysis, ...prev]);
      setTotal((prev) => prev + 1);
      return newAnalysis;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analiz başlatılırken hata oluştu');
      throw err;
    }
  };

  return {
    analyses,
    total,
    loading,
    error,
    page,
    setPage,
    startAnalysis,
    refresh: fetchAnalyses,
  };
}
