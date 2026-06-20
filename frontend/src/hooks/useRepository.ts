import { useState, useEffect, useCallback } from 'react';
import { repositoryApi } from '../api/repositories';
import { Repository, PaginatedResponse } from '../types';

export function useRepository(id?: string) {
  const [repository, setRepository] = useState<Repository | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRepository = useCallback(async () => {
    if (!id) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await repositoryApi.get(id);
      setRepository(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Depo yüklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchRepository();
  }, [fetchRepository]);

  const clone = async () => {
    if (!id) return;
    try {
      await repositoryApi.clone(id);
      await fetchRepository();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Clone hatası');
    }
  };

  const sync = async () => {
    if (!id) return;
    try {
      await repositoryApi.sync(id);
      await fetchRepository();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Senkronizasyon hatası');
    }
  };

  return {
    repository,
    loading,
    error,
    clone,
    sync,
    refresh: fetchRepository,
  };
}

export function useRepositoryList() {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');

  const fetchRepositories = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await repositoryApi.list({
        page,
        page_size: 20,
        search: search || undefined,
      });
      setRepositories(response.items);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Depolar yüklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => {
    fetchRepositories();
  }, [fetchRepositories]);

  const create = async (data: { name: string; url: string; description?: string }) => {
    try {
      const newRepo = await repositoryApi.create(data);
      setRepositories((prev) => [newRepo, ...prev]);
      setTotal((prev) => prev + 1);
      return newRepo;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Depo oluşturulurken hata oluştu');
      throw err;
    }
  };

  const remove = async (id: string) => {
    try {
      await repositoryApi.delete(id);
      setRepositories((prev) => prev.filter((r) => r.id !== id));
      setTotal((prev) => prev - 1);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Depo silinirken hata oluştu');
      throw err;
    }
  };

  return {
    repositories,
    total,
    loading,
    error,
    page,
    setPage,
    search,
    setSearch,
    create,
    remove,
    refresh: fetchRepositories,
  };
}
