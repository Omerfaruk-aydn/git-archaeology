import { useState, useEffect, useCallback } from 'react';
import { commitApi } from '../api/commits';
import { Commit, CommitDetail } from '../types';

export function useCommits(repoId: string) {
  const [commits, setCommits] = useState<Commit[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [authorFilter, setAuthorFilter] = useState('');

  const fetchCommits = useCallback(async () => {
    if (!repoId) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await commitApi.list({
        repo_id: repoId,
        page,
        page_size: 50,
        author: authorFilter || undefined,
      });
      setCommits(response.items);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Commit\'ler yüklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  }, [repoId, page, authorFilter]);

  useEffect(() => {
    fetchCommits();
  }, [fetchCommits]);

  return {
    commits,
    total,
    loading,
    error,
    page,
    setPage,
    authorFilter,
    setAuthorFilter,
    refresh: fetchCommits,
  };
}

export function useCommit(sha: string, repoId: string) {
  const [commit, setCommit] = useState<CommitDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCommit = useCallback(async () => {
    if (!sha || !repoId) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await commitApi.get(sha, repoId);
      setCommit(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Commit yüklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  }, [sha, repoId]);

  useEffect(() => {
    fetchCommit();
  }, [fetchCommit]);

  const analyze = async (focusAreas?: string[]) => {
    try {
      await commitApi.analyze(sha, repoId, focusAreas);
      await fetchCommit();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analiz hatası');
      throw err;
    }
  };

  const explainChange = async (filePath: string) => {
    try {
      const result = await commitApi.explainChange(sha, repoId, filePath);
      return result.explanation;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Açıklama hatası');
      throw err;
    }
  };

  return {
    commit,
    loading,
    error,
    analyze,
    explainChange,
    refresh: fetchCommit,
  };
}
