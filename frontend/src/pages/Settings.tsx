import { useState, useEffect } from 'react';
import { useAuth } from '../store/authStore';
import { providersApi, LLMProvider } from '../api/providers';

const PROVIDER_ICONS: Record<string, string> = {
  openai: '🤖', azure: '☁️', anthropic: '🧠', gemini: '✨', bedrock: '🏗️',
  openrouter: '🔀', together: '🤝', groq: '⚡', mistral: '🌊', cohere: '🔗',
  deepseek: '🔍', xai: '🚀', fireworks: '🎆', huggingface: '🤗', replicate: '🔄',
  baidu: '🐻', dashscope: '☁️', moonshot: '🌙', zhipuai: '💎', minimax: '📐',
  deepinfra: '🏗️', perplexity: '🔎', cloudflare: '🌐', local: '💻',
};

export function Settings() {
  const { user } = useAuth();
  const [providers, setProviders] = useState<LLMProvider[]>([]);
  const [loading, setLoading] = useState(true);
  const [settings, setSettings] = useState({
    theme: 'light',
    language: 'tr',
    notifications: true,
    defaultProvider: 'openai',
  });

  useEffect(() => {
    loadProviders();
  }, []);

  const loadProviders = async () => {
    try {
      const data = await providersApi.list();
      setProviders(data.providers);
    } catch (error) {
      console.error('Provider listesi yüklenemedi:', error);
    } finally {
      setLoading(false);
    }
  };

  const availableCount = providers.filter(p => p.available).length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Ayarlar</h1>
        <p className="mt-1 text-sm text-gray-500">Uygulama ayarlarınızı yönetin</p>
      </div>

      {/* Profile */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Profil Bilgileri</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">E-posta</label>
            <p className="mt-1 text-sm text-gray-900">{user?.email}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Kullanıcı Adı</label>
            <p className="mt-1 text-sm text-gray-900">{user?.username}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Tam Ad</label>
            <p className="mt-1 text-sm text-gray-900">{user?.full_name || 'Belirtilmemiş'}</p>
          </div>
        </div>
      </div>

      {/* LLM Provider */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-medium text-gray-900">Yapay Zeka Sağlayıcıları</h2>
          <span className="text-sm text-gray-500">
            {availableCount}/{providers.length} aktif
          </span>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Varsayılan Sağlayıcı</label>
          <select
            value={settings.defaultProvider}
            onChange={(e) => setSettings({ ...settings, defaultProvider: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            {providers.filter(p => p.available).map(p => (
              <option key={p.name} value={p.name}>
                {PROVIDER_ICONS[p.name] || '🔧'} {p.display_name}
              </option>
            ))}
            {providers.filter(p => p.available).length === 0 && (
              <option value="" disabled>Hiçbir API anahtarı yapılandırılmamış</option>
            )}
          </select>
        </div>

        {loading ? (
          <div className="text-center py-8 text-gray-500">Yükleniyor...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {providers.map((provider) => (
              <div
                key={provider.name}
                className={`border rounded-lg p-4 transition-all ${
                  provider.available
                    ? 'border-green-200 bg-green-50'
                    : 'border-gray-200 bg-gray-50 opacity-60'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{PROVIDER_ICONS[provider.name] || '🔧'}</span>
                    <div>
                      <h3 className="text-sm font-medium text-gray-900">{provider.display_name}</h3>
                      <p className="text-xs text-gray-500 mt-0.5">{provider.description}</p>
                    </div>
                  </div>
                  <span
                    className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                      provider.available
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-500'
                    }`}
                  >
                    {provider.available ? 'Aktif' : 'Pasif'}
                  </span>
                </div>
                {provider.website && (
                  <a
                    href={provider.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 inline-flex items-center text-xs text-indigo-600 hover:text-indigo-500"
                  >
                    {provider.website.replace('https://', '')} ↗
                  </a>
                )}
              </div>
            ))}
          </div>
        )}

        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h3 className="text-sm font-medium text-blue-900 mb-2">Nasıl Etkinleştirilir?</h3>
          <p className="text-sm text-blue-700">
            Sağlayıcıları etkinleştirmek için <code className="bg-blue-100 px-1 rounded">.env</code> dosyasında
            ilgili API anahtarlarını ayarlayın. Sağlayıcılar API anahtarı bulunan otomatik olarak etkinleşir.
          </p>
        </div>
      </div>

      {/* Application Settings */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Uygulama Ayarları</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Tema</label>
            <select
              value={settings.theme}
              onChange={(e) => setSettings({ ...settings, theme: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              <option value="light">Açık</option>
              <option value="dark">Karanlık</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Dil</label>
            <select
              value={settings.language}
              onChange={(e) => setSettings({ ...settings, language: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              <option value="tr">Türkçe</option>
              <option value="en">English</option>
            </select>
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="notifications"
              checked={settings.notifications}
              onChange={(e) => setSettings({ ...settings, notifications: e.target.checked })}
              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <label htmlFor="notifications" className="ml-2 block text-sm text-gray-900">
              Bildirimleri etkinleştir
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}
