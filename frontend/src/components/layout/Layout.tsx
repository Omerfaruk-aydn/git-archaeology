import React from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { useUI } from '../../store/uiStore';

interface LayoutProps {
  children: React.ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const { sidebarOpen, toggleSidebar } = useUI();

  return (
    <div className="min-h-screen bg-gray-100">
      <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} />

      <div className={`flex flex-col flex-1 min-h-screen transition-all duration-200 ${
        sidebarOpen ? 'lg:pl-64' : ''
      }`}>
        <Header onMenuClick={toggleSidebar} />

        <main className="flex-1 p-4 sm:p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
