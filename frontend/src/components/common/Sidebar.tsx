import React from 'react';
import {
  Globe,
  Dna,
  Binary,
  Layers,
  Network,
  TestTubes,
  FileSpreadsheet,
  AlertTriangle,
  TrendingUp,
  SlidersHorizontal,
  FolderGit2
} from 'lucide-react';

export type NavTab =
  | 'dashboard'
  | 'surveillance'
  | 'isolates'
  | 'amr'
  | 'typing'
  | 'comparative'
  | 'ast'
  | 'plasmids'
  | 'modelling'
  | 'reports';

interface SidebarProps {
  activeTab: NavTab;
  onTabChange: (tab: NavTab) => void;
  alertCount?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, onTabChange, alertCount = 1 }) => {
  const navItems = [
    { id: 'dashboard', label: 'Surveillance Hub', icon: Globe },
    { id: 'surveillance', label: '3D Geospatial', icon: Layers },
    { id: 'isolates', label: 'Genomic Registry', icon: Dna },
    { id: 'amr', label: 'AMRFinder & Determinants', icon: Binary },
    { id: 'typing', label: 'MLST & Kleborate', icon: Network },
    { id: 'comparative', label: 'Comparative & SNPs', icon: FolderGit2 },
    { id: 'ast', label: 'AST Concordance', icon: TestTubes },
    { id: 'plasmids', label: 'MOB-Suite Plasmids', icon: SlidersHorizontal },
    { id: 'modelling', label: 'SEIR Transmission', icon: TrendingUp },
    { id: 'reports', label: 'Alerts & Exports', icon: FileSpreadsheet, badge: alertCount },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/60 backdrop-blur-md flex flex-col justify-between p-3 select-none">
      <div className="space-y-1">
        <div className="px-3 py-2 text-[11px] font-mono uppercase tracking-wider text-slate-500 font-semibold">
          Surveillance Modules
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id as NavTab)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-crimson-900/30 text-white border border-crimson-700/50 shadow-sm shadow-crimson-950'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <div className="flex items-center space-x-2.5">
                <Icon className={`w-4 h-4 ${isActive ? 'text-crimson-500' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && item.badge > 0 && (
                <span className="px-1.5 py-0.5 text-[10px] font-mono bg-crimson-600 text-white rounded-full font-bold">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      <div className="p-3 border-t border-slate-800/80 bg-slate-950/40 rounded-lg text-slate-400 text-[11px] font-mono space-y-1">
        <div className="flex justify-between">
          <span>Engine:</span>
          <span className="text-slate-200">Nextflow Ready</span>
        </div>
        <div className="flex justify-between">
          <span>Database:</span>
          <span className="text-slate-200">PostGIS / WGS84</span>
        </div>
        <div className="flex justify-between">
          <span>Taxon:</span>
          <span className="text-emerald-400">K. pneumoniae</span>
        </div>
      </div>
    </aside>
  );
};
