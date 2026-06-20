import React from 'react';

interface ReportCardProps {
  report: {
    id: string;
    report_type: string;
    format: string;
    generated_at: string;
    metadata?: Record<string, unknown>;
  };
  onView?: (id: string) => void;
  onDownload?: (id: string) => void;
}

export function ReportCard({ report, onView, onDownload }: ReportCardProps) {
  const typeLabels: Record<string, string> = {
    full: 'Kapsamlı Rapor',
    summary: 'Özet Rapor',
    security: 'Güvenlik Raporu',
    architecture: 'Mimari Rapor',
    legacy: 'Legacy Kod Raporu',
  };

  const typeColors: Record<string, string> = {
    full: 'bg-indigo-100 text-indigo-800',
    summary: 'bg-blue-100 text-blue-800',
    security: 'bg-red-100 text-red-800',
    architecture: 'bg-green-100 text-green-800',
    legacy: 'bg-yellow-100 text-yellow-800',
  };

  return (
    <div className="bg-white rounded-lg p-4 shadow hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${typeColors[report.report_type]}`}>
            {typeLabels[report.report_type]}
          </span>
          <p className="text-sm text-gray-500 mt-2">
            {new Date(report.generated_at).toLocaleString('tr-TR')}
          </p>
          {report.metadata && (
            <p className="text-xs text-gray-400 mt-1">
              {report.format.toUpperCase()} formatında
            </p>
          )}
        </div>
        <div className="flex space-x-2">
          {onView && (
            <button
              onClick={() => onView(report.id)}
              className="px-3 py-1 text-sm text-indigo-600 hover:text-indigo-800"
            >
              Görüntüle
            </button>
          )}
          {onDownload && (
            <button
              onClick={() => onDownload(report.id)}
              className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
            >
              İndir
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
