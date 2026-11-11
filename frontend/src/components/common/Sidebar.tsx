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
  FolderGit2,
  X,
  Cpu,
  Radio
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
  | 'ai-engine'
  | 'one-health'
  | 'reports';

interface SidebarProps {
  activeTab: NavTab;
  onTabChange: (tab: NavTab) => void;
  alertCount?: number;
  isMobileOpen?: boolean;
  onCloseMobile?: () => void;
  selectedOrganism?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  onTabChange,
  alertCount = 1,
  isMobileOpen = false,
  onCloseMobile,
  selectedOrganism = 'Klebsiella pneumoniae',
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Surveillance Hub', icon: Globe },
    { id: 'surveillance', label: '3D Geospatial', icon: Layers },
    { id: 'isolates', label: 'Genomic Registry', icon: Dna },
    { id: 'amr', label: 'AMRFinder & Determinants', icon: Binary },
    { id: 'typing', label: 'MLST & Kleborate', icon: Network },
    { id: 'comparative', label: 'Comparative & SNPs', icon: FolderGit2 },
    { id: 'ast', label: 'AST Concordance', icon: TestTubes },
    { id: 'plasmids', label: 'MOB-Suite Plasmids', icon: SlidersHorizontal },
    { id: 'ai-engine', label: 'AI Deep MIC & Copilot', icon: Cpu, badgeText: 'AI' },
    { id: 'one-health', label: 'One Health & Wastewater', icon: Radio, badgeText: 'WBE' },
    { id: 'modelling', label: 'SEIR Transmission', icon: TrendingUp },
    { id: 'reports', label: 'Alerts & Exports', icon: FileSpreadsheet, badge: alertCount },
  ];


  const handleSelectTab = (tabId: NavTab) => {
    onTabChange(tabId);
    if (onCloseMobile) {
      onCloseMobile();
    }
  };

  const navContent = (
    <>
      <div className="space-y-1">
        <div className="flex items-center justify-between px-3 py-2 text-[11px] font-mono uppercase tracking-wider text-slate-500 font-semibold">
          <span>Surveillance Modules</span>
          {onCloseMobile && (
            <button
              onClick={onCloseMobile}
              className="lg:hidden p-1 text-slate-400 hover:text-white rounded"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => handleSelectTab(item.id as NavTab)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-crimson-900/30 text-white border border-crimson-700/50 shadow-sm shadow-crimson-950'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <div className="flex items-center space-x-2.5 truncate">
                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-crimson-500' : 'text-slate-400'}`} />
                <span className="truncate">{item.label}</span>
              </div>
              {item.badge && item.badge > 0 && (
                <span className="px-1.5 py-0.5 text-[10px] font-mono bg-crimson-600 text-white rounded-full font-bold ml-2">
                  {item.badge}
                </span>
              )}
              {(item as any).badgeText && (
                <span className="px-1.5 py-0.5 text-[9px] font-mono bg-emerald-950 text-emerald-400 border border-emerald-800/60 rounded font-bold ml-2">
                  {(item as any).badgeText}
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
          <span className="text-emerald-400 font-semibold italic truncate max-w-[120px]">{selectedOrganism}</span>
        </div>
      </div>
    </>
  );

  return (
    <>
      {/* Desktop Persistent Sidebar (>= 1024px) */}
      <aside className="hidden lg:flex w-64 border-r border-slate-800 bg-slate-900/60 backdrop-blur-md flex-col justify-between p-3 select-none shrink-0">
        {navContent}
      </aside>

      {/* Mobile Drawer Overlay (< 1024px) */}
      {isMobileOpen && (
        <div className="lg:hidden fixed inset-0 z-50 flex">
          {/* Backdrop Blur Dimmer */}
          <div
            className="fixed inset-0 bg-black/70 backdrop-blur-sm transition-opacity"
            onClick={onCloseMobile}
          />

          {/* Drawer Panel */}
          <div className="relative w-72 max-w-[85vw] bg-slate-900/95 border-r border-slate-800 p-4 flex flex-col justify-between shadow-2xl z-10 overflow-y-auto">
            {navContent}
          </div>
        </div>
      )}
    </>
  );
};
