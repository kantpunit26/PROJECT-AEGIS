import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { PrevalenceChart } from '../components/charts/PrevalenceChart';
import { CoOccurrenceHeatmap } from '../components/charts/CoOccurrenceHeatmap';
import { Binary, ShieldAlert, Cpu, AlertTriangle } from 'lucide-react';

interface AMRExplorerProps {
  selectedOrganism?: string;
}

export const AMRExplorer: React.FC<AMRExplorerProps> = ({
  selectedOrganism = 'Klebsiella pneumoniae'
}) => {
  const [prevalenceData, setPrevalenceData] = useState<any>({ total_isolates: 0, determinants: [] });
  const [coOccurrenceData, setCoOccurrenceData] = useState<any>({ genes: [], matrix: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAMR() {
      setLoading(true);
      try {
        const [prev, coOcc] = await Promise.all([
          api.getAMRPrevalence(selectedOrganism),
          api.getAMRCoOccurrence(8, selectedOrganism),
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
  }, [selectedOrganism]);

  const topBetaLactam = prevalenceData.determinants
    ?.filter((d: any) => d.drug_class?.toLowerCase().includes('beta') || d.subclass?.toLowerCase().includes('carbapenem'))
    .slice(0, 3)
    .map((d: any) => d.gene_symbol)
    .join(', ') || 'None detected';

  const topAminoglycoside = prevalenceData.determinants
    ?.filter((d: any) => d.drug_class?.toLowerCase().includes('amino'))
    .slice(0, 3)
    .map((d: any) => d.gene_symbol)
    .join(', ') || 'Wild-type';

  const topOther = prevalenceData.determinants
    ?.filter((d: any) => !d.drug_class?.toLowerCase().includes('beta') && !d.drug_class?.toLowerCase().includes('amino'))
    .slice(0, 3)
    .map((d: any) => d.gene_symbol)
    .join(', ') || 'None detected';

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-xl font-bold text-white tracking-wide">Antimicrobial Resistance Determinants</h1>
            <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800 italic">
              {selectedOrganism}
            </span>
          </div>
          <p className="text-xs text-slate-400">
            NCBI AMRFinderPlus acquired resistance genes, point mutations, and co-selection patterns ({prevalenceData.total_isolates || 0} genomes)
          </p>
        </div>
      </div>

      {/* AMR Mechanism Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Primary Beta-Lactamases / Carbapenemases</div>
          <div className="text-xl font-bold font-mono text-crimson-400 truncate">{topBetaLactam}</div>
          <div className="text-[11px] text-slate-400">High-risk target hydrolyzing determinants</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Aminoglycoside Resistance</div>
          <div className="text-xl font-bold font-mono text-blue-400 truncate">{topAminoglycoside}</div>
          <div className="text-[11px] text-slate-400">Enzymatic modifiers & 16S methyltransferases</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Target Alterations / Other Classes</div>
          <div className="text-xl font-bold font-mono text-purple-400 truncate">{topOther}</div>
          <div className="text-[11px] text-slate-400">Quinolone, polymyxin, glycopeptide, and rifamycin markers</div>
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

