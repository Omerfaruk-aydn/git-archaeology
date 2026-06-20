import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { repositoryApi } from '../api/repositories';
import { analysisApi } from '../api/analyses';
import { commitApi } from '../api/commits';
import { Repository, Analysis, Commit } from '../types';

export function RepositoryDetail() {
  const { id } = useParams<{ id: string }>();
  const [repository, setRepository] = useState<Repository | null>(null);
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [commits, setCommits] = useState<Commit[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'commits' | 'analyses'>('overview');

  useEffect(() => {
    if (id) {
      loadRepositoryData(id);
    }
  }, [id]);

  async function loadRepositoryData(repoId: string) {
    try {
      setLoading(true);
      const [repo, analysesResp, commitsResp] = await Promise.all([
        repositoryApi.get(repoId),
        analysisApi.list({ repo_id: repoId, page: 1, page_size: 5 }),
        commitApi.list({ repo_id: repoId, page: 1, page_size: 20 }),
      ]);

      setRepository(repo);
      setAnalyses(analysesResp.items);
      setCommits(commitsResp.items);
    } catch (err) {
      console.error('Depo verileri yüklenirken hata:', err);
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

  if (!repository) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Depo bulunamadı</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">{repository.name}</h1>
            <p className="mt-1 text-sm text-gray-500">{repository.url}</p>
            {repository.description && (
              <p className="mt-2 text-sm text-gray-600">{repository.description}</p>
            )}
          </div>
          <div className="flex space-x-3">
            {!repository.local_path ? (
              <button
                onClick={() => handleClone(repository.id)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Klonla
              </button>
            ) : (
              <>
                <button
                  onClick={() => handleSync(repository.id)}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Senkronize Et
                </button>
                <Link
                  to={`/analyses/new?repo=${repository.id}`}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                  Yeni Analiz Başlat
                </Link>
              </>
            )}
          </div>
        </div>

        <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
          <div>
            <dt className="text-sm font-medium text-gray-500">Varsayılan Dal</dt>
            <dd className="mt-1 text-sm text-gray-900">{repository.default_branch}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Yerel Yol</dt>
            <dd className="mt-1 text-sm text-gray-900 truncate">
              {repository.local_path || 'Klonlanmamış'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Son Analiz</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {repository.last_analyzed_at
                ? new Date(repository.last_analyzed_at).toLocaleDateString('tr-TR')
                : 'Hiç'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Durum</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {repository.is_analyzed ? 'Analiz Edildi' : 'Analiz Edilmedi'}
            </dd>
          </div>
        </div>
      </div>

      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {(['overview', 'commits', 'analyses'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab === 'overview' && 'Genel Bakış'}
              {tab === 'commits' && "Commit'ler"}
              {tab === 'analyses' && 'Analizler'}
            </button>
          ))}
        </nav>
      </div>

      {activeTab === 'overview' && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Genel Bakış</h2>
          <p className="text-gray-600">
            Bu depo için detaylı analiz başlatmak için "Yeni Analiz Başlat" butonunu kullanın.
          </p>
        </div>
      )}

      {activeTab === 'commits' && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Son Commit'ler</h2>
          </div>
          <div className="divide-y divide-gray-200">
            {commits.map((commit) => (
              <Link
                key={commit.id}
                to={`/commits/${commit.sha}?repo=${repository.id}`}
                className="block hover:bg-gray-50 px-4 py-4 sm:px-6"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{commit.message}</p>
                    <p className="text-sm text-gray-500">
                      {commit.author_name} · {new Date(commit.author_date).toLocaleDateString('tr-TR')}
                    </p>
                  </div>
                  <div className="flex items-center space-x-4 text-sm">
                    <span className="text-green-600">+{commit.additions}</span>
                    <span className="text-red-600">-{commit.deletions}</span>
                    <span className="text-gray-500">{commit.files_changed} dosya</span>
                    <code className="text-gray-400">{commit.sha.slice(0, 7)}</code>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'analyses' && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Analizler</h2>
          </div>
          <div className="divide-y divide-gray-200">
            {analyses.map((analysis) => (
              <Link
                key={analysis.id}
                to={`/analyses/${analysis.id}`}
                className="block hover:bg-gray-50 px-4 py-4 sm:px-6"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      Analiz #{analysis.id.slice(0, 8)}
                    </p>
                    <p className="text-sm text-gray-500">
                      {analysis.processed_commits}/{analysis.total_commits} commit
                    </p>
                  </div>
                  <StatusBadge status={analysis.status} />
                </div>
              </Link>
            ))}
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

async function handleClone(repoId: string) {
  try {
    await repositoryApi.clone(repoId);
    window.location.reload();
  } catch (err) {
    console.error('Clone hatası:', err);
  }
}

async function handleSync(repoId: string) {
  try {
    await repositoryApi.sync(repoId);
    window.location.reload();
  } catch (err) {
    console.error('Sync hatası:', err);
  }
}
