import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { useAnalysisList } from '../hooks/useAnalysis';

export function Analysis() {
  const [searchParams] = useSearchParams();
  const repoId = searchParams.get('repo') || undefined;
  const { analyses, total, loading, error, page, setPage, refresh } = useAnalysisList(repoId);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Analizler</h1>
          <p className="mt-1 text-sm text-gray-500">Depo analizlerinizi görüntüleyin</p>
        </div>
        <button
          onClick={refresh}
          className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          Yenile
        </button>
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
            {analyses.map((analysis) => (
              <Link
                key={analysis.id}
                to={`/analyses/${analysis.id}`}
                className="block hover:bg-gray-50 px-4 py-4 sm:px-6"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">
                      Analiz #{analysis.id.slice(0, 8)}
                    </p>
                    <p className="text-sm text-gray-500">
                      {analysis.processed_commits}/{analysis.total_commits} commit
                    </p>
                    <p className="text-sm text-gray-500">
                      {new Date(analysis.created_at).toLocaleString('tr-TR')}
                    </p>
                  </div>
                  <div className="flex items-center space-x-4">
                    <StatusBadge status={analysis.status} />
                    {analysis.status === 'running' && (
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-indigo-600 h-2 rounded-full"
                          style={{ width: `${analysis.progress}%` }}
                        />
                      </div>
                    )}
                  </div>
                </div>
              </Link>
            ))}
            {analyses.length === 0 && (
              <div className="px-4 py-8 text-center text-gray-500">
                Henüz analiz yapılmamış
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    running: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  const labels: Record<string, string> = {
    pending: 'Beklemede',
    running: 'Çalışıyor',
    completed: 'Tamamlandı',
    failed: 'Başarısız',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[status]}`}
    >
      {labels[status]}
    </span>
  );
}
