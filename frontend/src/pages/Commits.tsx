import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useCommits } from '../hooks/useCommits';

export function Commits() {
  const [searchParams] = useSearchParams();
  const repoId = searchParams.get('repo') || '';
  const { commits, total, loading, error, page, setPage, authorFilter, setAuthorFilter } = useCommits(repoId);

  if (!repoId) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Lütfen bir depo seçin</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Commit'ler</h1>
        <div className="flex items-center space-x-4">
          <input
            type="text"
            placeholder="Yazar filtrele..."
            value={authorFilter}
            onChange={(e) => setAuthorFilter(e.target.value)}
            className="block w-64 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-800">{error}</p>
        </div>
      ) : (
        <div className="bg-white shadow rounded-lg">
          <div className="divide-y divide-gray-200">
            {commits.map((commit) => (
              <div
                key={commit.id}
                className="px-4 py-4 sm:px-6 hover:bg-gray-50"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {commit.message}
                    </p>
                    <p className="text-sm text-gray-500">
                      {commit.author_name} · {new Date(commit.author_date).toLocaleString('tr-TR')}
                    </p>
                  </div>
                  <div className="flex items-center space-x-4 text-sm">
                    <span className="text-green-600">+{commit.additions}</span>
                    <span className="text-red-600">-{commit.deletions}</span>
                    <span className="text-gray-500">{commit.files_changed} dosya</span>
                    <code className="text-gray-400 font-mono">{commit.sha.slice(0, 7)}</code>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="px-4 py-3 border-t border-gray-200 sm:px-6">
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-700">
                Toplam <span className="font-medium">{total}</span> commit
              </p>
              <div className="flex space-x-2">
                <button
                  onClick={() => setPage(Math.max(1, page - 1))}
                  disabled={page === 1}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50"
                >
                  Önceki
                </button>
                <span className="px-3 py-1 text-sm text-gray-700">
                  Sayfa {page}
                </span>
                <button
                  onClick={() => setPage(page + 1)}
                  disabled={commits.length < 50}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50"
                >
                  Sonraki
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
