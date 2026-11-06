import React from 'react';

interface DeterminantItem {
  gene_symbol: string;
  gene_family?: string;
  drug_class: string;
  subclass?: string;
  count: number;
  prevalence_percent: number;
}

interface PrevalenceChartProps {
  determinants: DeterminantItem[];
  totalIsolates: number;
}

export const PrevalenceChart: React.FC<PrevalenceChartProps> = ({ determinants, totalIsolates }) => {
  const getBarColor = (subclass?: string, drugClass?: string) => {
    if (subclass?.includes('Carbapenem')) return 'bg-crimson-600';
    if (subclass?.includes('Colistin')) return 'bg-purple-600';
    if (subclass?.includes('Cephalosporin') || drugClass?.includes('Beta-lactam')) return 'bg-orange-500';
    if (drugClass?.includes('Aminoglycoside')) return 'bg-blue-600';
    if (drugClass?.includes('Fluoroquinolone')) return 'bg-amber-500';
    return 'bg-slate-600';
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-sm font-semibold text-white">AMR Determinant Population Prevalence</h3>
          <p className="text-xs text-slate-400">AMRFinderPlus gene detections across N = {totalIsolates} isolates</p>
        </div>
      </div>

      <div className="space-y-3 max-h-[380px] overflow-y-auto pr-2">
        {determinants.map((det) => (
          <div key={det.gene_symbol} className="space-y-1">
            <div className="flex justify-between items-center text-xs">
              <div className="flex items-center space-x-2">
                <span className="font-mono font-bold text-slate-200">{det.gene_symbol}</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-400">
                  {det.subclass || det.drug_class}
                </span>
              </div>
              <div className="flex items-center space-x-3 font-mono">
                <span className="text-slate-400 text-[11px]">{det.count} isolates</span>
                <span className="font-bold text-slate-200 w-12 text-right">{det.prevalence_percent}%</span>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-slate-800/80 rounded-full h-2 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-500 ${getBarColor(det.subclass, det.drug_class)}`}
                style={{ width: `${Math.min(det.prevalence_percent, 100)}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
