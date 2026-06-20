import React from 'react';
import { Commit } from '../../types';

interface CommitListProps {
  commits: Commit[];
  loading?: boolean;
  onSelect?: (commit: Commit) => void;
}

export function CommitList({ commits, loading, onSelect }: CommitListProps) {
  if (loading) {
    return (
      <div className="space-y-2">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="animate-pulse bg-white rounded-lg p-4 shadow">
            <div className="h-4 bg-gray-200 rounded w-2/3 mb-2"></div>
            <div className="h-3 bg-gray-200 rounded w-1/3"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="divide-y divide-gray-200">
        {commits.map((commit) => (
          <div
            key={commit.id}
            onClick={() => onSelect?.(commit)}
            className="px-4 py-4 sm:px-6 hover:bg-gray-50 cursor-pointer"
          >
            <div className="flex items-center justify-between">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {commit.message}
                </p>
                <p className="text-sm text-gray-500">
                  {commit.author_name} · {new Date(commit.author_date).toLocaleString('tr-TR')}
                </p>
              </div>
              <div className="flex items-center space-x-4 text-sm">
                <span className="text-green-600">+{commit.additions}</span>
                <span className="text-red-600">-{commit.deletions}</span>
                <span className="text-gray-500">{commit.files_changed} dosya</span>
                <code className="text-gray-400 font-mono">{commit.sha.slice(0, 7)}</code>
                {commit.analyzed && (
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                    Analiz Edildi
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
