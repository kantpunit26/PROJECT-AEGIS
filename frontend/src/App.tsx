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
import { api } from './services/api';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavTab>('dashboard');
  const [systemHealth, setSystemHealth] = useState<any>(null);

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
        return <Dashboard onNavigate={(tab) => setActiveTab(tab)} />;
      case 'surveillance':
        return <Surveillance />;
      case 'isolates':
        return <Isolates />;
      case 'amr':
        return <AMRExplorer />;
      case 'comparative':
        return <ComparativeGenomics />;
      case 'ast':
        return <ASTValidation />;
      case 'plasmids':
        return <PlasmidRecon />;
      case 'modelling':
        return <SEIRModelling />;
      case 'reports':
        return <Reports />;
      default:
        return <Dashboard onNavigate={(tab) => setActiveTab(tab)} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header systemHealth={systemHealth} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} alertCount={1} />
        <main className="flex-1 overflow-y-auto p-6 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
          <div className="max-w-7xl mx-auto">{renderActivePage()}</div>
        </main>
      </div>
    </div>
  );
};

export default App;
