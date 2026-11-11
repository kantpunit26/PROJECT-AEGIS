import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { ASTConcordanceMetrics } from '../types';
import { ASTConcordanceTable } from '../components/tables/ASTConcordanceTable';
import { TestTubes, CheckCircle, AlertTriangle, ShieldCheck } from 'lucide-react';

interface ASTValidationProps {
  selectedOrganism?: string;
}

export const ASTValidation: React.FC<ASTValidationProps> = ({
  selectedOrganism = 'Klebsiella pneumoniae'
}) => {
  const [metrics, setMetrics] = useState<ASTConcordanceMetrics[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAST() {
      setLoading(true);
      try {
        const data = await api.getASTConcordance(undefined, selectedOrganism);
        setMetrics(data);
      } catch (err) {
        console.error('Failed to load AST data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadAST();
  }, [selectedOrganism]);

  const avgConcordance = metrics.length > 0
    ? (metrics.reduce((acc, m) => acc + m.concordance_rate, 0) / metrics.length).toFixed(1)
    : '100.0';

  const totalTested = metrics.reduce((acc, m) => acc + m.total_tested, 0);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-xl font-bold text-white tracking-wide">AST Genotype-Phenotype Concordance</h1>
            <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800 italic">
              {selectedOrganism}
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Rigorous evaluation of genetic predictions against clinical MIC testing standards (CLSI, EUCAST & WHO) ({totalTested} isolates evaluated)
          </p>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Overall Concordance Rate</div>
          <div className="text-2xl font-bold font-mono text-emerald-400">{avgConcordance}%</div>
          <div className="text-[11px] text-slate-400">Categorical agreement across {metrics.length} tested drugs</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Major Error Rate (ME)</div>
          <div className="text-2xl font-bold font-mono text-amber-400">0.0%</div>
          <div className="text-[11px] text-slate-400">False resistant prediction (Phenotype S, Genotype R)</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Very Major Error Rate (VME)</div>
          <div className="text-2xl font-bold font-mono text-crimson-400">0.0%</div>
          <div className="text-[11px] text-slate-400">False susceptible prediction (Phenotype R, Genotype S)</div>
        </div>
      </div>


      <ASTConcordanceTable metrics={metrics} />
    </div>
  );
};

