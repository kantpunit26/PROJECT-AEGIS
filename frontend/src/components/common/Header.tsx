import React from 'react';
import { ShieldAlert, Activity, Menu, X } from 'lucide-react';

interface HeaderProps {
  systemHealth?: {
    status: string;
    version: string;
    primary_organism: string;
  };
  onToggleMobileMenu?: () => void;
  isMobileMenuOpen?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  systemHealth,
  onToggleMobileMenu,
  isMobileMenuOpen = false,
}) => {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/90 backdrop-blur-md px-3 sm:px-6 flex items-center justify-between sticky top-0 z-50">
      <div className="flex items-center space-x-2 sm:space-x-3">
        {/* Mobile Hamburger Toggle Button */}
        <button
          onClick={onToggleMobileMenu}
          className="lg:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none focus:ring-1 focus:ring-crimson-600 transition-colors"
          aria-label="Toggle Navigation Menu"
        >
          {isMobileMenuOpen ? <X className="w-5 h-5 text-crimson-400" /> : <Menu className="w-5 h-5" />}
        </button>

        {/* Logo Shield */}
        <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-lg bg-crimson-900/40 border border-crimson-700/60 flex items-center justify-center text-crimson-500 shadow-lg shadow-crimson-950/50 shrink-0">
          <ShieldAlert className="w-5 h-5 sm:w-6 sm:h-6 animate-pulse" />
        </div>

        {/* App Title */}
        <div>
          <div className="flex items-center space-x-1.5 sm:space-x-2">
            <span className="font-bold text-base sm:text-lg tracking-wider text-white">PROJECT AEGIS</span>
            <span className="text-[9px] sm:text-[10px] font-mono uppercase px-1.5 sm:px-2 py-0.5 rounded-full bg-crimson-950 text-crimson-400 border border-crimson-800/60 font-semibold tracking-wider">
              AMR Intel
            </span>
          </div>
          <p className="text-[11px] text-slate-400 hidden md:block">
            Advanced Genomic Epidemiology & Surveillance Platform
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-2 sm:space-x-4 text-xs font-mono">
        {/* Active Organism */}
        <div className="hidden sm:flex items-center space-x-2 bg-slate-800/70 border border-slate-700/60 px-2.5 sm:px-3 py-1.5 rounded-md">
          <Activity className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
          <span className="text-slate-400 hidden md:inline">Target:</span>
          <span className="text-emerald-300 font-semibold italic truncate max-w-[140px] md:max-w-none">
            K. pneumoniae
          </span>
        </div>

        {/* Live Engine Status */}
        <div className="flex items-center space-x-2 bg-slate-800/70 border border-slate-700/60 px-2.5 sm:px-3 py-1.5 rounded-md">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-slate-300 hidden sm:inline">v{systemHealth?.version || '2.0.0'}</span>
          <span className="text-emerald-400 font-semibold">ONLINE</span>
        </div>
      </div>
    </header>
  );
};
