import React from 'react';
import { useAuth } from '../../store/authStore';

interface HeaderProps {
  onMenuClick: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-40 flex items-center justify-between h-16 bg-white border-b border-gray-200 px-4">
      <button
        onClick={onMenuClick}
        className="p-1 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
      >
        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <div className="flex items-center space-x-4">
        {user && (
          <>
            <span className="text-sm text-gray-700">
              {user.full_name || user.username}
            </span>
            <button
              onClick={logout}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Çıkış
            </button>
          </>
        )}
      </div>
    </header>
  );
}
