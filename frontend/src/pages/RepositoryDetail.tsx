import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
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
  const [showAnalysisForm, setShowAnalysisForm] = useState(false);
  const [startingAnalysis, setStartingAnalysis] = useState(false);
  const [analysisConfig, setAnalysisConfig] = useState({
    max_commits: 50,
    llm_provider: 'openrouter',
    llm_model: 'openai/gpt-4o-mini',
    focus_areas: ['security', 'performance'],
    include_diffs: true,
    batch_size: 10,
  });

  useEffect(() => {
    if (id) loadRepositoryData(id);
  }, [id]);

  async function loadRepositoryData(repoId: string) {
    try {
      setLoading(true);
      const [repo, analysesResp, commitsResp] = await Promise.all([
        repositoryApi.get(repoId),
        analysisApi.list({ repo_id: repoId, page: 1, page_size: 10 }).catch(() => ({ items: [], total: 0 })),
        commitApi.list({ repo_id: repoId, page: 1, page_size: 20 }).catch(() => ({ items: [], total: 0 })),
      ]);
      setRepository(repo);
      setAnalyses(analysesResp.items);
      setCommits(commitsResp.items);
    } catch (err) {
      console.error('Depo verileri yuklenirken hata:', err);
    } finally {
      setLoading(false);
    }
  }

  async function handleStartAnalysis() {
    if (!id) return;
    setStartingAnalysis(true);
    try {
      await analysisApi.create({
        repository_id: id,
        ...analysisConfig,
        branch: repository?.default_branch,
      });
      setShowAnalysisForm(false);
      await loadRepositoryData(id);
      setActiveTab('analyses');
    } catch (err) {
      console.error('Analiz baslatma hatasi:', err);
      alert('Analiz baslatilamadi: ' + (err instanceof Error ? err.message : 'Bilinmeyen hata'));
    } finally {
      setStartingAnalysis(false);
    }
  }

  async function handleClone() {
    if (!id) return;
    try {
      await repositoryApi.clone(id);
      window.location.reload();
    } catch (err) {
      alert('Klonlama hatasi');
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!repository) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Depo bulunamadi</p>
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
              <button onClick={handleClone}
                className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Klonla
              </button>
            ) : (
              <>
                <button onClick={() => setShowAnalysisForm(!showAnalysisForm)}
                  className="px-4 py-2 text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                  {showAnalysisForm ? 'Iptal' : 'Yeni Analiz Baslat'}
                </button>
              </>
            )}
          </div>
        </div>

        <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
          <div>
            <dt className="text-sm font-medium text-gray-500">Varsayilan Dal</dt>
            <dd className="mt-1 text-sm text-gray-900">{repository.default_branch}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Yerel Yol</dt>
            <dd className="mt-1 text-sm text-gray-900 truncate">{repository.local_path || 'Klonlanmamis'}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Son Analiz</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {repository.last_analyzed_at ? new Date(repository.last_analyzed_at).toLocaleDateString('tr-TR') : 'Hic'}
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

      {showAnalysisForm && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Yeni Analiz Baslat</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Maksimum Commit</label>
              <input type="number" value={analysisConfig.max_commits}
                onChange={(e) => setAnalysisConfig({ ...analysisConfig, max_commits: parseInt(e.target.value) || 50 })}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">LLM Saglayici</label>
              <select value={analysisConfig.llm_provider}
                onChange={(e) => setAnalysisConfig({ ...analysisConfig, llm_provider: e.target.value })}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
                <option value="openrouter">OpenRouter (GPT-4o-mini)</option>
                <option value="openai">OpenAI</option>
                <option value="anthropic">Anthropic</option>
                <option value="local">Local (Ollama)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Batch Boyutu</label>
              <input type="number" value={analysisConfig.batch_size}
                onChange={(e) => setAnalysisConfig({ ...analysisConfig, batch_size: parseInt(e.target.value) || 10 })}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>
            <div className="flex items-center">
              <input type="checkbox" id="include_diffs" checked={analysisConfig.include_diffs}
                onChange={(e) => setAnalysisConfig({ ...analysisConfig, include_diffs: e.target.checked })}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="include_diffs" className="ml-2 block text-sm text-gray-900">Diff'leri dahil et</label>
            </div>
          </div>
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Odak Alanlari</label>
            <div className="flex flex-wrap gap-2">
              {['security', 'performance', 'architecture', 'dependency', 'refactor'].map((area) => (
                <label key={area} className="inline-flex items-center">
                  <input type="checkbox" checked={analysisConfig.focus_areas.includes(area)}
                    onChange={(e) => {
                      const areas = e.target.checked
                        ? [...analysisConfig.focus_areas, area]
                        : analysisConfig.focus_areas.filter((a) => a !== area);
                      setAnalysisConfig({ ...analysisConfig, focus_areas: areas });
                    }}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <span className="ml-1 text-sm text-gray-700">{area}</span>
                </label>
              ))}
            </div>
          </div>
          <div className="mt-6">
            <button onClick={handleStartAnalysis} disabled={startingAnalysis}
              className="px-6 py-2 text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50">
              {startingAnalysis ? 'Baslatiliyor...' : 'Analizi Baslat'}
            </button>
          </div>
        </div>
      )}

      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {(['overview', 'commits', 'analyses'] as const).map((tab) => (
            <button key={tab} onClick={() => setActiveTab(tab)}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}>
              {tab === 'overview' && 'Genel Bakis'}
              {tab === 'commits' && "Commit'ler"}
              {tab === 'analyses' && 'Analizler'}
            </button>
          ))}
        </nav>
      </div>

      {activeTab === 'overview' && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Genel Bakis</h2>
          <p className="text-gray-600">
            Bu depo icin analiz baslatmak icin "Yeni Analiz Baslat" butonunu kullanin.
          </p>
        </div>
      )}

      {activeTab === 'commits' && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Son Commit'ler</h2>
          </div>
          {commits.length === 0 ? (
            <div className="px-4 py-8 text-center text-gray-500">Henuz commit yok</div>
          ) : (
            <div className="divide-y divide-gray-200">
              {commits.map((commit) => (
                <div key={commit.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">{commit.message}</p>
                      <p className="text-sm text-gray-500">
                        {commit.author_name} - {new Date(commit.author_date).toLocaleDateString('tr-TR')}
                      </p>
                    </div>
                    <div className="flex items-center space-x-4 text-sm">
                      <span className="text-green-600">+{commit.additions}</span>
                      <span className="text-red-600">-{commit.deletions}</span>
                      <span className="text-gray-500">{commit.files_changed} dosya</span>
                      <code className="text-gray-400">{commit.sha.slice(0, 7)}</code>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'analyses' && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Analizler</h2>
          </div>
          {analyses.length === 0 ? (
            <div className="px-4 py-8 text-center text-gray-500">Henuz analiz yok</div>
          ) : (
            <div className="divide-y divide-gray-200">
              {analyses.map((analysis) => (
                <div key={analysis.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900">Analiz #{analysis.id.slice(0, 8)}</p>
                      <p className="text-sm text-gray-500">
                        {analysis.processed_commits}/{analysis.total_commits} commit
                      </p>
                    </div>
                    <StatusBadge status={analysis.status} />
                  </div>
                  {analysis.status === 'running' && (
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-indigo-600 h-2 rounded-full" style={{ width: `${analysis.progress}%` }} />
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
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
    running: 'Calisiyor',
    completed: 'Tamamlandi',
    failed: 'Basarisiz',
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[status] || 'bg-gray-100 text-gray-800'}`}>
      {labels[status] || status}
    </span>
  );
}
