import React from 'react';

interface AnalysisProgressProps {
  progress: number;
  status: string;
  totalCommits: number;
  processedCommits: number;
}

export function AnalysisProgress({ progress, status, totalCommits, processedCommits }: AnalysisProgressProps) {
  const statusColors: Record<string, string> = {
    pending: 'text-yellow-600',
    running: 'text-blue-600',
    completed: 'text-green-600',
    failed: 'text-red-600',
  };

  const statusLabels: Record<string, string> = {
    pending: 'Beklemede',
    running: 'Çalışıyor',
    completed: 'Tamamlandı',
    failed: 'Başarısız',
  };

  return (
    <div className="bg-white rounded-lg p-6 shadow">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">Analiz Durumu</h3>
        <span className={`text-sm font-medium ${statusColors[status]}`}>
          {statusLabels[status]}
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
        <div
          className="bg-indigo-600 h-3 rounded-full transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>
      <div className="flex justify-between text-sm text-gray-500">
        <span>{processedCommits}/{totalCommits} commit işlendi</span>
        <span>%{Math.round(progress)}</span>
      </div>
    </div>
  );
}
