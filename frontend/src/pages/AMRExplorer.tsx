import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { PrevalenceChart } from '../components/charts/PrevalenceChart';
import { CoOccurrenceHeatmap } from '../components/charts/CoOccurrenceHeatmap';
import { Binary, ShieldAlert, Cpu, AlertTriangle } from 'lucide-react';

export const AMRExplorer: React.FC = () => {
  const [prevalenceData, setPrevalenceData] = useState<any>({ total_isolates: 0, determinants: [] });
  const [coOccurrenceData, setCoOccurrenceData] = useState<any>({ genes: [], matrix: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAMR() {
      try {
        const [prev, coOcc] = await Promise.all([
          api.getAMRPrevalence(),
          api.getAMRCoOccurrence(8),
        ]);
        setPrevalenceData(prev);
        setCoOccurrenceData(coOcc);
      } catch (err) {
        console.error('Failed to load AMR data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadAMR();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div>
          <h1 className="text-xl font-bold text-white tracking-wide">Antimicrobial Resistance Determinants</h1>
          <p className="text-xs text-slate-400">
            NCBI AMRFinderPlus acquired resistance genes, point mutations, and co-selection patterns
          </p>
        </div>
      </div>

      {/* AMR Mechanism Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Carbapenemase Spectrum</div>
          <div className="text-xl font-bold font-mono text-crimson-400">NDM-5, KPC-2, OXA-181</div>
          <div className="text-[11px] text-slate-400">Class A, B, and D active carbapenem resistance</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Polymyxin / Colistin</div>
          <div className="text-xl font-bold font-mono text-purple-400">mcr-1.1 & mgrB disruption</div>
          <div className="text-[11px] text-slate-400">Plasmid transfer and chromosomal regulator loss</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Pan-Aminoglycoside</div>
          <div className="text-xl font-bold font-mono text-blue-400">armA & rmtB</div>
          <div className="text-[11px] text-slate-400">16S rRNA methyltransferase resistance to amikacin</div>
        </div>
      </div>

      {/* Population Prevalence & Co-occurrence Matrix */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PrevalenceChart
          determinants={prevalenceData.determinants || []}
          totalIsolates={prevalenceData.total_isolates || 0}
        />
        <CoOccurrenceHeatmap data={coOccurrenceData} />
      </div>
    </div>
  );
};
