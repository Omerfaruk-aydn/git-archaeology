import React from 'react';
import { Link } from 'react-router-dom';
import { Repository } from '../../types';

interface RepositoryListProps {
  repositories: Repository[];
  loading?: boolean;
}

export function RepositoryList({ repositories, loading }: RepositoryListProps) {
  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="animate-pulse bg-white rounded-lg p-4 shadow">
            <div className="h-4 bg-gray-200 rounded w-1/3 mb-2"></div>
            <div className="h-3 bg-gray-200 rounded w-2/3"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {repositories.map((repo) => (
        <Link
          key={repo.id}
          to={`/repositories/${repo.id}`}
          className="block bg-white rounded-lg p-4 shadow hover:shadow-md transition-shadow"
        >
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-medium text-gray-900">{repo.name}</h3>
              <p className="text-sm text-gray-500 mt-1">{repo.description || repo.url}</p>
            </div>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              {repo.commit_count !== undefined && (
                <span>{repo.commit_count} commit</span>
              )}
              {repo.contributor_count !== undefined && (
                <span>{repo.contributor_count} katkıda bulunan</span>
              )}
              <span className={`px-2 py-1 rounded-full text-xs ${
                repo.is_analyzed ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {repo.is_analyzed ? 'Analiz Edildi' : 'Analiz Edilmedi'}
              </span>
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
