import React, { useEffect, useState } from 'react';
import { Header } from './components/common/Header';
import { Sidebar, NavTab } from './components/common/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { Surveillance } from './pages/Surveillance';
import { Isolates } from './pages/Isolates';
import { AMRExplorer } from './pages/AMRExplorer';
import { ComparativeGenomics } from './pages/ComparativeGenomics';
import { ASTValidation } from './pages/ASTValidation';
import { PlasmidRecon } from './pages/PlasmidRecon';
import { SEIRModelling } from './pages/SEIRModelling';
import { Reports } from './pages/Reports';
import { AIEngine } from './pages/AIEngine';
import { OneHealth } from './pages/OneHealth';
import { api } from './services/api';

export const App: React.FC = () => {
  const getTabFromUrl = (): NavTab => {
    const params = new URLSearchParams(window.location.search);
    const tab = params.get('tab') as NavTab;
    const validTabs: NavTab[] = [
      'dashboard', 'surveillance', 'isolates', 'amr', 'typing',
      'comparative', 'ast', 'plasmids', 'modelling', 'ai-engine', 'one-health', 'reports'
    ];
    return validTabs.includes(tab) ? tab : 'dashboard';
  };

  const [activeTab, setActiveTab] = useState<NavTab>(getTabFromUrl());
  const [selectedOrganism, setSelectedOrganism] = useState<string>('Klebsiella pneumoniae');
  const [systemHealth, setSystemHealth] = useState<any>(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleTabChange = (tab: NavTab) => {
    setActiveTab(tab);
    setIsMobileMenuOpen(false);
    const url = new URL(window.location.href);
    url.searchParams.set('tab', tab);
    window.history.pushState({}, '', url.toString());
  };

  useEffect(() => {
    async function checkHealth() {
      try {
        const h = await api.getHealth();
        setSystemHealth(h);
      } catch (err) {
        console.error('API health check error:', err);
      }
    }
    checkHealth();
  }, []);

  const renderActivePage = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard onNavigate={(tab) => handleTabChange(tab)} selectedOrganism={selectedOrganism} />;
      case 'surveillance':
        return <Surveillance selectedOrganism={selectedOrganism} />;
      case 'isolates':
        return <Isolates selectedOrganism={selectedOrganism} />;
      case 'amr':
        return <AMRExplorer selectedOrganism={selectedOrganism} />;
      case 'typing':
        return <AMRExplorer selectedOrganism={selectedOrganism} />;
      case 'comparative':
        return <ComparativeGenomics />;
      case 'ast':
        return <ASTValidation selectedOrganism={selectedOrganism} />;
      case 'plasmids':
        return <PlasmidRecon />;
      case 'ai-engine':
        return <AIEngine selectedOrganism={selectedOrganism} />;
      case 'one-health':
        return <OneHealth />;
      case 'modelling':
        return <SEIRModelling />;
      case 'reports':
        return <Reports />;
      default:
        return <Dashboard onNavigate={(tab) => handleTabChange(tab)} selectedOrganism={selectedOrganism} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header
        systemHealth={systemHealth}
        selectedOrganism={selectedOrganism}
        onSelectOrganism={setSelectedOrganism}
        isMobileMenuOpen={isMobileMenuOpen}
        onToggleMobileMenu={() => setIsMobileMenuOpen((prev) => !prev)}
      />
      <div className="flex flex-1 overflow-hidden relative">
        <Sidebar
          activeTab={activeTab}
          onTabChange={handleTabChange}
          alertCount={1}
          isMobileOpen={isMobileMenuOpen}
          onCloseMobile={() => setIsMobileMenuOpen(false)}
          selectedOrganism={selectedOrganism}
        />
        <main className="flex-1 overflow-y-auto p-3 sm:p-5 lg:p-6 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 w-full">
          <div className="max-w-7xl mx-auto w-full">{renderActivePage()}</div>
        </main>
      </div>
    </div>
  );

};


export default App;
