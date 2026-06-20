import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAnalysis } from '../hooks/useAnalysis';

export function AnalysisDetail() {
  const { id } = useParams<{ id: string }>();
  const { analysis, result, loading, error } = useAnalysis(id);
  const [activeTab, setActiveTab] = useState<'summary' | 'insights' | 'files' | 'authors'>('summary');

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Analiz bulunamadı</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">
              Analiz #{analysis.id.slice(0, 8)}
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              Başlangıç: {new Date(analysis.created_at).toLocaleString('tr-TR')}
            </p>
          </div>
          <StatusBadge status={analysis.status} />
        </div>

        {analysis.status === 'running' && (
          <div className="mt-4">
            <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
              <span>
                {analysis.processed_commits}/{analysis.total_commits} commit işlendi
              </span>
              <span>%{analysis.progress.toFixed(1)}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${analysis.progress}%` }}
              />
            </div>
          </div>
        )}

        {analysis.error_message && (
          <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-sm text-red-800">{analysis.error_message}</p>
          </div>
        )}
      </div>

      {analysis.status === 'completed' && result && (
        <>
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {(['summary', 'insights', 'files', 'authors'] as const).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab
                      ? 'border-indigo-500 text-indigo-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab === 'summary' && 'Özet'}
                  {tab === 'insights' && 'İçgörüler'}
                  {tab === 'files' && 'Dosyalar'}
                  {tab === 'authors' && 'Yazarlar'}
                </button>
              ))}
            </nav>
          </div>

          {activeTab === 'summary' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Özet</h2>
              <p className="text-gray-600 whitespace-pre-wrap">{result.summary}</p>

              <div className="mt-6 grid grid-cols-3 gap-4">
                <div className="bg-gray-50 rounded-lg p-4">
                  <dt className="text-sm font-medium text-gray-500">Toplam Commit</dt>
                  <dd className="mt-1 text-2xl font-semibold text-gray-900">
                    {result.statistics.total_commits}
                  </dd>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <dt className="text-sm font-medium text-gray-500">Eklenen Satır</dt>
                  <dd className="mt-1 text-2xl font-semibold text-green-600">
                    +{result.statistics.total_additions}
                  </dd>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <dt className="text-sm font-medium text-gray-500">Silinen Satır</dt>
                  <dd className="mt-1 text-2xl font-semibold text-red-600">
                    -{result.statistics.total_deletions}
                  </dd>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'insights' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">İçgörüler</h2>
              <ul className="space-y-3">
                {result.insights.map((insight, index) => (
                  <li key={index} className="flex items-start">
                    <span className="flex-shrink-0 w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 text-sm font-medium">
                      {index + 1}
                    </span>
                    <p className="ml-3 text-gray-600">{insight}</p>
                  </li>
                ))}
              </ul>

              <h3 className="mt-6 text-lg font-medium text-gray-900 mb-4">Öneriler</h3>
              <ul className="space-y-2">
                {result.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start">
                    <span className="flex-shrink-0 text-green-500 mr-2">•</span>
                    <p className="text-gray-600">{rec}</p>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {activeTab === 'files' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">En Çok Değişen Dosyalar</h2>
              <div className="space-y-2">
                {result.file_hotspots.map((file, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between py-2 border-b border-gray-100"
                  >
                    <code className="text-sm text-gray-900">{file.path}</code>
                    <span className="text-sm text-gray-500">{file.changes} değişiklik</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'authors' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Yazar Katkısı</h2>
              <div className="space-y-4">
                {result.author_contributions.map((author, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">{author.name}</p>
                        <p className="text-sm text-gray-500">{author.commits} commit</p>
                      </div>
                      <div className="text-sm text-right">
                        <p className="text-green-600">+{author.additions}</p>
                        <p className="text-red-600">-{author.deletions}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
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
