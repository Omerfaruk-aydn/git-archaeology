import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { repositoryApi } from '../api/repositories';
import { analysisApi } from '../api/analyses';
import { Repository, Analysis } from '../types';

export function Dashboard() {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [recentAnalyses, setRecentAnalyses] = useState<Analysis[]>([]);
  const [stats, setStats] = useState({
    totalRepos: 0,
    totalAnalyses: 0,
    completedAnalyses: 0,
    failedAnalyses: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  async function loadDashboardData() {
    try {
      setLoading(true);

      const [reposResponse, analysesResponse] = await Promise.all([
        repositoryApi.list({ page: 1, page_size: 5 }),
        analysisApi.list({ page: 1, page_size: 10 }),
      ]);

      setRepositories(reposResponse.items);
      setRecentAnalyses(analysesResponse.items);
      setStats({
        totalRepos: reposResponse.total,
        totalAnalyses: analysesResponse.total,
        completedAnalyses: analysesResponse.items.filter((a) => a.status === 'completed').length,
        failedAnalyses: analysesResponse.items.filter((a) => a.status === 'failed').length,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Veriler yüklenirken hata oluştu');
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  const hasData = repositories.length > 0 || recentAnalyses.length > 0;

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold">GitArch'e Hoş Geldiniz</h1>
        <p className="mt-2 text-indigo-100">
          Git depolarınızın geçmişini analiz edin, kod değişikliklerinin hikayesini keşfedin.
        </p>
        <div className="mt-4 flex flex-wrap gap-3">
          <Link
            to="/repositories"
            className="inline-flex items-center px-4 py-2 bg-white text-indigo-600 rounded-lg font-medium hover:bg-indigo-50 transition-colors"
          >
            <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Yeni Depo Ekle
          </Link>
          <Link
            to="/reports"
            className="inline-flex items-center px-4 py-2 bg-white/20 text-white rounded-lg font-medium hover:bg-white/30 transition-colors"
          >
            Raporları Görüntüle
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <StatCard title="Toplam Depo" value={stats.totalRepos} icon="repository" color="blue" />
        <StatCard title="Toplam Analiz" value={stats.totalAnalyses} icon="analysis" color="purple" />
        <StatCard title="Tamamlanan" value={stats.completedAnalyses} icon="check" color="green" />
        <StatCard title="Başarısız" value={stats.failedAnalyses} icon="error" color="red" />
      </div>

      {!hasData && (
        <div className="bg-white shadow rounded-lg p-8 text-center">
          <div className="mx-auto w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Başlamaya Hazır mısınız?</h3>
          <p className="text-gray-500 mb-4">Henüz depo eklenmemiş. İlk Git deponuzu ekleyerek başlayın.</p>
          <Link
            to="/repositories"
            className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors"
          >
            Depo Ekle
          </Link>
        </div>
      )}

      {hasData && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-medium text-gray-900">Son Eklenen Depolar</h2>
                <Link
                  to="/repositories"
                  className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                >
                  Tümünü Gör
                </Link>
              </div>
            </div>
            <div className="divide-y divide-gray-200">
              {repositories.map((repo) => (
                <Link
                  key={repo.id}
                  to={`/repositories/${repo.id}`}
                  className="block hover:bg-gray-50 px-4 py-4 sm:px-6"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">{repo.name}</p>
                      <p className="text-sm text-gray-500 truncate">{repo.url}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      {repo.is_analyzed ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          Analiz Edildi
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          Beklemede
                        </span>
                      )}
                    </div>
                  </div>
                </Link>
              ))}
              {repositories.length === 0 && (
                <div className="px-4 py-8 text-center text-gray-500">
                  Henüz depo eklenmemiş.
                </div>
              )}
            </div>
          </div>

          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-medium text-gray-900">Son Analizler</h2>
                <Link
                  to="/analyses"
                  className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                >
                  Tümünü Gör
                </Link>
              </div>
            </div>
            <div className="divide-y divide-gray-200">
              {recentAnalyses.map((analysis) => (
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
                    </div>
                    <div className="flex items-center space-x-2">
                      <StatusBadge status={analysis.status} />
                      {analysis.status === 'running' && (
                        <div className="w-16 bg-gray-200 rounded-full h-2">
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
              {recentAnalyses.length === 0 && (
                <div className="px-4 py-8 text-center text-gray-500">
                  Henüz analiz yapılmamış.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({ title, value, icon, color }: { title: string; value: number; icon: string; color: string }) {
  const colors: Record<string, { bg: string; icon: string; text: string }> = {
    blue: { bg: 'bg-blue-50', icon: 'text-blue-600', text: 'text-blue-600' },
    purple: { bg: 'bg-purple-50', icon: 'text-purple-600', text: 'text-purple-600' },
    green: { bg: 'bg-green-50', icon: 'text-green-600', text: 'text-green-600' },
    red: { bg: 'bg-red-50', icon: 'text-red-600', text: 'text-red-600' },
  };

  const c = colors[color] || colors.blue;

  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className={`w-10 h-10 ${c.bg} rounded-lg flex items-center justify-center`}>
              <span className={`${c.icon} text-lg`}>
                {icon === 'repository' && '📁'}
                {icon === 'analysis' && '🔍'}
                {icon === 'check' && '✓'}
                {icon === 'error' && '✗'}
              </span>
            </div>
          </div>
          <div className="ml-4 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd className={`text-2xl font-bold ${c.text}`}>{value}</dd>
            </dl>
          </div>
        </div>
      </div>
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
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[status] || 'bg-gray-100 text-gray-800'}`}
    >
      {labels[status] || status}
    </span>
  );
}
