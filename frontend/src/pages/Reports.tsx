import { useState } from 'react';

export function Reports() {
  const [reportType, setReportType] = useState('full');
  const [format, setFormat] = useState('markdown');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Raporlar</h1>
        <p className="mt-1 text-sm text-gray-500">Analiz raporlarınızı görüntüleyin ve oluşturun</p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Yeni Rapor Oluştur</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Rapor Türü</label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              <option value="full">Kapsamlı Rapor</option>
              <option value="summary">Özet Rapor</option>
              <option value="security">Güvenlik Raporu</option>
              <option value="architecture">Mimari Analiz</option>
              <option value="legacy">Legacy Kod Analizi</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Format</label>
            <select
              value={format}
              onChange={(e) => setFormat(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              <option value="markdown">Markdown</option>
              <option value="html">HTML</option>
            </select>
          </div>
        </div>
        <button className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
          Rapor Oluştur
        </button>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Önceki Raporlar</h2>
        </div>
        <div className="px-4 py-8 text-center text-gray-500">
          Henüz rapor oluşturulmamış
        </div>
      </div>
    </div>
  );
}
