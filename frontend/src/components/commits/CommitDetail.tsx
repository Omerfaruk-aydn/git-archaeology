import React from 'react';
import { Commit, FileChange } from '../../types';

interface CommitDetailProps {
  commit: Commit;
  fileChanges?: FileChange[];
  onAnalyze?: (commitId: string) => void;
}

export function CommitDetail({ commit, fileChanges, onAnalyze }: CommitDetailProps) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">{commit.message}</h2>
          <p className="text-sm text-gray-500 mt-1">
            {commit.author_name} · {new Date(commit.author_date).toLocaleString('tr-TR')}
          </p>
        </div>
        <code className="text-sm font-mono text-gray-500 bg-gray-100 px-2 py-1 rounded">
          {commit.sha}
        </code>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6 text-center">
        <div className="bg-gray-50 rounded-lg p-3">
          <p className="text-2xl font-bold text-green-600">+{commit.additions}</p>
          <p className="text-xs text-gray-500">Eklenen</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-3">
          <p className="text-2xl font-bold text-red-600">-{commit.deletions}</p>
          <p className="text-xs text-gray-500">Silinen</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-3">
          <p className="text-2xl font-bold text-gray-600">{commit.files_changed}</p>
          <p className="text-xs text-gray-500">Dosya</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-3">
          <p className="text-2xl font-bold text-indigo-600">
            {commit.analyzed ? 'Evet' : 'Hayır'}
          </p>
          <p className="text-xs text-gray-500">Analiz</p>
        </div>
      </div>

      {!commit.analyzed && onAnalyze && (
        <button
          onClick={() => onAnalyze(commit.id)}
          className="mb-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-sm"
        >
          Bu Commit'i Analiz Et
        </button>
      )}

      {commit.analysis_result && (
        <div className="mb-6 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-medium text-blue-900 mb-2">Analiz Sonucu</h3>
          <pre className="text-sm text-blue-800 whitespace-pre-wrap">
            {JSON.stringify(commit.analysis_result, null, 2)}
          </pre>
        </div>
      )}

      {fileChanges && fileChanges.length > 0 && (
        <div>
          <h3 className="font-medium text-gray-900 mb-3">Değişen Dosyalar</h3>
          <div className="space-y-2">
            {fileChanges.map((fc) => (
              <div key={fc.id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                <div className="flex items-center space-x-2">
                  <span className={`text-xs font-medium px-2 py-1 rounded ${
                    fc.change_type === 'added' ? 'bg-green-100 text-green-800' :
                    fc.change_type === 'deleted' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {fc.change_type}
                  </span>
                  <span className="text-sm text-gray-700">{fc.file_path}</span>
                </div>
                <div className="text-sm">
                  <span className="text-green-600">+{fc.additions}</span>
                  <span className="text-red-600 ml-2">-{fc.deletions}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
