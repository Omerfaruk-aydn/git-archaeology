import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useRepositoryList } from '../hooks/useRepository';
import { useDebounce } from '../hooks/useDebounce';

export function Repositories() {
  const {
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
  } = useRepositoryList();

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newRepo, setNewRepo] = useState({ name: '', url: '', description: '' });
  const [creating, setCreating] = useState(false);

  const debouncedSearch = useDebounce(search, 300);

  const handleCreate = async () => {
    if (!newRepo.name || !newRepo.url) return;

    try {
      setCreating(true);
      await create(newRepo);
      setShowCreateModal(false);
      setNewRepo({ name: '', url: '', description: '' });
    } catch (err) {
      console.error('Depo oluşturulurken hata:', err);
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Bu depoyu silmek istediğinizden emin misiniz?')) {
      try {
        await remove(id);
      } catch (err) {
        console.error('Depo silinirken hata:', err);
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Depolar</h1>
          <p className="mt-1 text-sm text-gray-500">Git depolarınızı yönetin</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Yeni Depo Ekle
        </button>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-3 border-b border-gray-200">
          <input
            type="text"
            placeholder="Depo ara..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
          </div>
        ) : error ? (
          <div className="p-4 text-red-600">{error}</div>
        ) : (
          <div className="divide-y divide-gray-200">
            {repositories.map((repo) => (
              <div key={repo.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <Link
                      to={`/repositories/${repo.id}`}
                      className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                    >
                      {repo.name}
                    </Link>
                    <p className="text-sm text-gray-500 truncate">{repo.url}</p>
                    {repo.description && (
                      <p className="text-sm text-gray-500 mt-1">{repo.description}</p>
                    )}
                  </div>
                  <div className="flex items-center space-x-4">
                    <StatusBadge status={repo.is_analyzed ? 'analyzed' : 'pending'} />
                    <button
                      onClick={() => handleDelete(repo.id)}
                      className="text-sm text-red-600 hover:text-red-800"
                    >
                      Sil
                    </button>
                  </div>
                </div>
              </div>
            ))}
            {repositories.length === 0 && (
              <div className="px-4 py-8 text-center text-gray-500">
                {search ? 'Arama sonucu bulunamadı' : 'Henüz depo eklenmemiş'}
              </div>
            )}
          </div>
        )}

        {total > 20 && (
          <div className="px-4 py-3 border-t border-gray-200 sm:px-6">
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-700">
                Toplam <span className="font-medium">{total}</span> depo
              </p>
              <div className="flex space-x-2">
                <button
                  onClick={() => setPage(Math.max(1, page - 1))}
                  disabled={page === 1}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50"
                >
                  Önceki
                </button>
                <span className="px-3 py-1 text-sm text-gray-700">Sayfa {page}</span>
                <button
                  onClick={() => setPage(page + 1)}
                  disabled={repositories.length < 20}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50"
                >
                  Sonraki
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {showCreateModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" onClick={() => setShowCreateModal(false)}>
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>

            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Yeni Depo Ekle</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Depo Adı</label>
                    <input
                      type="text"
                      value={newRepo.name}
                      onChange={(e) => setNewRepo({ ...newRepo, name: e.target.value })}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Git URL</label>
                    <input
                      type="text"
                      value={newRepo.url}
                      onChange={(e) => setNewRepo({ ...newRepo, url: e.target.value })}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      placeholder="https://github.com/user/repo.git"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Açıklama</label>
                    <textarea
                      value={newRepo.description}
                      onChange={(e) => setNewRepo({ ...newRepo, description: e.target.value })}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      rows={3}
                    />
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  onClick={handleCreate}
                  disabled={!newRepo.name || !newRepo.url || creating}
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
                >
                  {creating ? 'Oluşturuluyor...' : 'Oluştur'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  İptal
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    analyzed: 'bg-green-100 text-green-800',
    pending: 'bg-gray-100 text-gray-800',
  };

  const labels: Record<string, string> = {
    analyzed: 'Analiz Edildi',
    pending: 'Beklemede',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles[status]}`}
    >
      {labels[status]}
    </span>
  );
}
