import React, { useState } from 'react';

interface GenerateReportFormProps {
  repositoryId: string;
  onSubmit: (data: {
    repository_id: string;
    report_type: string;
    format: string;
    branch?: string;
    start_date?: string;
    end_date?: string;
    file_paths?: string[];
  }) => void;
  loading?: boolean;
}

export function GenerateReportForm({ repositoryId, onSubmit, loading }: GenerateReportFormProps) {
  const [reportType, setReportType] = useState('full');
  const [format, setFormat] = useState('markdown');
  const [branch, setBranch] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [filePaths, setFilePaths] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      repository_id: repositoryId,
      report_type: reportType,
      format,
      branch: branch || undefined,
      start_date: startDate || undefined,
      end_date: endDate || undefined,
      file_paths: filePaths ? filePaths.split(',').map(f => f.trim()) : undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-medium text-gray-900">Rapor Oluştur</h3>
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
            <option value="architecture">Mimari Rapor</option>
            <option value="legacy">Legacy Kod Raporu</option>
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
            <option value="pdf">PDF</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Dal (Opsiyonel)</label>
          <input
            type="text"
            value={branch}
            onChange={(e) => setBranch(e.target.value)}
            placeholder="main"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Dosya Yolları (Opsiyonel)</label>
          <input
            type="text"
            value={filePaths}
            onChange={(e) => setFilePaths(e.target.value)}
            placeholder="src/app.py, src/utils.py"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Başlangıç Tarihi</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Bitiş Tarihi</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>
      </div>
      <button
        type="submit"
        disabled={loading}
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
      >
        {loading ? 'Oluşturuluyor...' : 'Rapor Oluştur'}
      </button>
    </form>
  );
}
