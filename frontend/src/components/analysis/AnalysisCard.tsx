import React from 'react';
import { Analysis } from '../../types';

interface AnalysisCardProps {
  analysis: Analysis;
  onClick?: () => void;
}

export function AnalysisCard({ analysis, onClick }: AnalysisCardProps) {
  const statusStyles: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    running: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  const statusLabels: Record<string, string> = {
    pending: 'Beklemede',
    running: 'Çalışıyor',
    completed: 'Tamamlandı',
    failed: 'Başarısız',
  };

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg p-4 shadow hover:shadow-md transition-shadow cursor-pointer"
    >
      <div className="flex items-center justify-between">
        <div>
          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusStyles[analysis.status]}`}>
            {statusLabels[analysis.status]}
          </span>
          {analysis.status === 'running' && (
            <div className="mt-2">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{ width: `${analysis.progress}%` }}
                />
              </div>
              <p className="text-xs text-gray-500 mt-1">{Math.round(analysis.progress)}%</p>
            </div>
          )}
        </div>
        <div className="text-sm text-gray-500">
          <p>{analysis.processed_commits}/{analysis.total_commits} commit</p>
          {analysis.started_at && (
            <p className="text-xs">{new Date(analysis.started_at).toLocaleString('tr-TR')}</p>
          )}
        </div>
      </div>
      {analysis.error_message && (
        <p className="mt-2 text-sm text-red-600">{analysis.error_message}</p>
      )}
    </div>
  );
}
