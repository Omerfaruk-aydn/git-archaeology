import React from 'react';

interface CommitFiltersProps {
  authorFilter: string;
  onAuthorChange: (value: string) => void;
  dateFrom?: string;
  onDateFromChange?: (value: string) => void;
  dateTo?: string;
  onDateToChange?: (value: string) => void;
}

export function CommitFilters({
  authorFilter,
  onAuthorChange,
  dateFrom,
  onDateFromChange,
  dateTo,
  onDateToChange,
}: CommitFiltersProps) {
  return (
    <div className="bg-white rounded-lg p-4 shadow mb-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Yazar</label>
          <input
            type="text"
            value={authorFilter}
            onChange={(e) => onAuthorChange(e.target.value)}
            placeholder="Yazar adı veya email..."
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>
        {onDateFromChange && (
          <div>
            <label className="block text-sm font-medium text-gray-700">Başlangıç Tarihi</label>
            <input
              type="date"
              value={dateFrom || ''}
              onChange={(e) => onDateFromChange(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
        )}
        {onDateToChange && (
          <div>
            <label className="block text-sm font-medium text-gray-700">Bitiş Tarihi</label>
            <input
              type="date"
              value={dateTo || ''}
              onChange={(e) => onDateToChange(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
        )}
      </div>
    </div>
  );
}
