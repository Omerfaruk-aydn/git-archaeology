import { useState, useCallback } from 'react';

let globalSidebarOpen = true;

export function useUI() {
  const [sidebarOpen, setSidebarOpen] = useState(globalSidebarOpen);
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    return (localStorage.getItem('theme') as 'light' | 'dark') || 'light';
  });

  const toggleSidebar = useCallback(() => {
    globalSidebarOpen = !globalSidebarOpen;
    setSidebarOpen(globalSidebarOpen);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme((prev) => {
      const next = prev === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', next);
      return next;
    });
  }, []);

  return {
    sidebarOpen,
    theme,
    toggleSidebar,
    toggleTheme,
  };
}
