import React from 'react';
import { ShieldAlert, Activity, Database, Globe2, Radio } from 'lucide-react';

interface HeaderProps {
  systemHealth?: {
    status: string;
    version: string;
    primary_organism: string;
  };
}

export const Header: React.FC<HeaderProps> = ({ systemHealth }) => {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/90 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-50">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-lg bg-crimson-900/40 border border-crimson-700/60 flex items-center justify-center text-crimson-500 shadow-lg shadow-crimson-950/50">
          <ShieldAlert className="w-6 h-6 animate-pulse" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="font-bold text-lg tracking-wider text-white">PROJECT AEGIS 2.0</span>
            <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded-full bg-crimson-950 text-crimson-400 border border-crimson-800/60 font-semibold tracking-wider">
              AMR Intelligence
            </span>
          </div>
          <p className="text-xs text-slate-400 hidden sm:block">
            Advanced Genomic Epidemiology & Surveillance Platform
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-5 text-xs font-mono">
        {/* Active Organism */}
        <div className="hidden md:flex items-center space-x-2 bg-slate-800/70 border border-slate-700/60 px-3 py-1.5 rounded-md">
          <Activity className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-slate-400">Target Taxon:</span>
          <span className="text-emerald-300 font-semibold italic">Klebsiella pneumoniae</span>
        </div>

        {/* Live Engine Status */}
        <div className="flex items-center space-x-2 bg-slate-800/70 border border-slate-700/60 px-3 py-1.5 rounded-md">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-slate-300">CORE v{systemHealth?.version || '2.0.0'}</span>
          <span className="text-emerald-400 font-semibold">ONLINE</span>
        </div>
      </div>
    </header>
  );
};

