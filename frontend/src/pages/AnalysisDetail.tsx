import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAnalysis } from '../hooks/useAnalysis';

export function AnalysisDetail() {
  const { id } = useParams<{ id: string }>();
  const { analysis, result, loading, error } = useAnalysis(id);
  const [activeTab, setActiveTab] = useState<'summary' | 'insights' | 'files' | 'authors'>('summary');

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Analiz bulunamadi</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Analiz #{analysis.id.slice(0, 8)}</h1>
            <p className="mt-1 text-indigo-100">
              {new Date(analysis.created_at).toLocaleString('tr-TR')} - {analysis.total_commits} commit
            </p>
          </div>
          <StatusBadge status={analysis.status} />
        </div>
        {analysis.status === 'running' && (
          <div className="mt-4">
            <div className="flex items-center justify-between text-sm text-indigo-100 mb-2">
              <span>{analysis.processed_commits}/{analysis.total_commits} commit islendi</span>
              <span>%{analysis.progress.toFixed(1)}</span>
            </div>
            <div className="w-full bg-white/20 rounded-full h-3">
              <div className="bg-white h-3 rounded-full transition-all duration-300" style={{ width: `${analysis.progress}%` }} />
            </div>
          </div>
        )}
      </div>

      {analysis.error_message && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-sm text-red-800">{analysis.error_message}</p>
        </div>
      )}

      {analysis.status === 'completed' && result && (
        <>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <StatCard label="Toplam Commit" value={result.statistics.total_commits} color="indigo" />
            <StatCard label="Eklenen Satir" value={`+${result.statistics.total_additions}`} color="green" />
            <StatCard label="Silinen Satir" value={`-${result.statistics.total_deletions}`} color="red" />
            <StatCard label="Yazar Sayisi" value={result.author_contributions.length} color="purple" />
          </div>

          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {(['summary', 'insights', 'files', 'authors'] as const).map((tab) => (
                <button key={tab} onClick={() => setActiveTab(tab)}
                  className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}>
                  {tab === 'summary' && 'Ozet'}
                  {tab === 'insights' && 'Icgoruler'}
                  {tab === 'files' && 'Dosyalar'}
                  {tab === 'authors' && 'Yazarlar'}
                </button>
              ))}
            </nav>
          </div>

          {activeTab === 'summary' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Genel Ozet</h2>
              <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{result.summary}</p>
              {result.time_period && (result.time_period.start || result.time_period.end) && (
                <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-500">
                    Analiz Araligi: {result.time_period.start ? new Date(result.time_period.start).toLocaleDateString('tr-TR') : '?'}
                    {' - '}
                    {result.time_period.end ? new Date(result.time_period.end).toLocaleDateString('tr-TR') : '?'}
                  </p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'insights' && (
            <div className="space-y-6">
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Icgoruler</h2>
                <div className="space-y-3">
                  {result.insights.map((insight: string, index: number) => (
                    <div key={index} className="flex items-start p-3 bg-blue-50 rounded-lg">
                      <span className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 text-sm font-bold">
                        {index + 1}
                      </span>
                      <p className="ml-3 text-gray-700">{insight}</p>
                    </div>
                  ))}
                </div>
              </div>
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">Oneriler</h2>
                <div className="space-y-3">
                  {result.recommendations.map((rec: string, index: number) => (
                    <div key={index} className="flex items-start p-3 bg-green-50 rounded-lg">
                      <span className="flex-shrink-0 w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 text-sm font-bold">
                        {index + 1}
                      </span>
                      <p className="ml-3 text-gray-700">{rec}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'files' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">En Cok Degisen Dosyalar</h2>
              {result.file_hotspots.length === 0 ? (
                <p className="text-gray-500">Dosya degisikligi bulunamadi</p>
              ) : (
                <div className="space-y-2">
                  {result.file_hotspots.map((file: any, index: number) => (
                    <div key={index} className="flex items-center justify-between py-3 px-4 bg-gray-50 rounded-lg hover:bg-gray-100">
                      <div className="flex items-center min-w-0 flex-1">
                        <span className="flex-shrink-0 w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 text-sm font-bold mr-3">
                          {index + 1}
                        </span>
                        <code className="text-sm text-gray-900 truncate">{file.path}</code>
                      </div>
                      <div className="flex items-center space-x-4 text-sm ml-4">
                        <span className="text-gray-500">{file.changes} degisiklik</span>
                        {file.additions > 0 && <span className="text-green-600">+{file.additions}</span>}
                        {file.deletions > 0 && <span className="text-red-600">-{file.deletions}</span>}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'authors' && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Yazar Katkilari</h2>
              {result.author_contributions.length === 0 ? (
                <p className="text-gray-500">Yazar bilgisi bulunamadi</p>
              ) : (
                <div className="space-y-4">
                  {result.author_contributions.map((author: any, index: number) => {
                    const totalChanges = author.additions + author.deletions;
                    const additionsPercent = totalChanges > 0 ? (author.additions / totalChanges) * 100 : 50;
                    return (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center">
                            <div className="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center mr-3">
                              <span className="text-indigo-600 font-bold text-sm">
                                {author.name.charAt(0).toUpperCase()}
                              </span>
                            </div>
                            <div>
                              <p className="font-medium text-gray-900">{author.name}</p>
                              <p className="text-sm text-gray-500">{author.commits} commit</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-green-600 font-medium">+{author.additions}</p>
                            <p className="text-sm text-red-600 font-medium">-{author.deletions}</p>
                          </div>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div className="bg-green-500 h-2 rounded-l-full" style={{ width: `${additionsPercent}%` }} />
                        </div>
                        <div className="flex justify-between text-xs text-gray-500 mt-1">
                          <span>Eklenen: %{additionsPercent.toFixed(0)}</span>
                          <span>Silinen: %{(100 - additionsPercent).toFixed(0)}</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

function StatCard({ label, value, color }: { label: string; value: any; color: string }) {
  const colors: Record<string, string> = {
    indigo: 'bg-indigo-50 text-indigo-700',
    green: 'bg-green-50 text-green-700',
    red: 'bg-red-50 text-red-700',
    purple: 'bg-purple-50 text-purple-700',
  };
  return (
    <div className={`rounded-lg p-4 ${colors[color] || 'bg-gray-50 text-gray-700'}`}>
      <p className="text-sm font-medium opacity-75">{label}</p>
      <p className="mt-1 text-2xl font-bold">{value}</p>
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
    running: 'Calisiyor',
    completed: 'Tamamlandi',
    failed: 'Basarisiz',
  };
  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${styles[status] || 'bg-gray-100 text-gray-800'}`}>
      {labels[status] || status}
    </span>
  );
}
