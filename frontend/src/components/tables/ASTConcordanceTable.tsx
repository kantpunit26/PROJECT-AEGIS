import React from 'react';
import { ASTConcordanceMetrics } from '../../types';
import { CheckCircle2, AlertTriangle } from 'lucide-react';

interface ASTConcordanceTableProps {
  metrics: ASTConcordanceMetrics[];
}

export const ASTConcordanceTable: React.FC<ASTConcordanceTableProps> = ({ metrics }) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div>
        <h3 className="text-sm font-semibold text-white">Genotype vs. Phenotype Concordance Validation</h3>
        <p className="text-xs text-slate-400">
          CLSI M100 / EUCAST breakpoint concordance and diagnostic error rates across clinical MIC determinations
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[680px] text-xs font-mono border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-slate-500 text-[11px] uppercase">
              <th className="text-left py-2 px-3">Antimicrobial</th>
              <th className="text-center py-2 px-3">Tested (N)</th>
              <th className="text-center py-2 px-3">TP (Resistant)</th>
              <th className="text-center py-2 px-3">TN (Susceptible)</th>
              <th className="text-center py-2 px-3">Major Error (ME)</th>
              <th className="text-center py-2 px-3">Very Major Error (VME)</th>
              <th className="text-center py-2 px-3">Sensitivity</th>
              <th className="text-center py-2 px-3">Specificity</th>
              <th className="text-right py-2 px-3">Concordance</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {metrics.map((m) => (
              <tr key={m.antibiotic} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-2.5 px-3 font-semibold text-slate-200">{m.antibiotic}</td>
                <td className="py-2.5 px-3 text-center text-slate-400">{m.total_tested}</td>
                <td className="py-2.5 px-3 text-center text-emerald-400 font-bold">{m.true_positive_resistant}</td>
                <td className="py-2.5 px-3 text-center text-slate-300 font-bold">{m.true_negative_susceptible}</td>
                <td className="py-2.5 px-3 text-center">
                  <span className={m.major_error_false_resistant > 0 ? 'text-amber-400 font-bold' : 'text-slate-500'}>
                    {m.major_error_false_resistant}
                  </span>
                </td>
                <td className="py-2.5 px-3 text-center">
                  <span className={m.very_major_error_false_susceptible > 0 ? 'text-crimson-400 font-bold' : 'text-slate-500'}>
                    {m.very_major_error_false_susceptible}
                  </span>
                </td>
                <td className="py-2.5 px-3 text-center font-bold text-slate-200">{m.sensitivity}%</td>
                <td className="py-2.5 px-3 text-center font-bold text-slate-200">{m.specificity}%</td>
                <td className="py-2.5 px-3 text-right">
                  <span className="px-2 py-0.5 rounded bg-emerald-950 border border-emerald-800 text-emerald-400 font-bold">
                    {m.concordance_rate}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

