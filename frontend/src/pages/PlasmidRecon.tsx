import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { SlidersHorizontal, Layers, Share2, ShieldAlert } from 'lucide-react';

export const PlasmidRecon: React.FC = () => {
  const [summary, setSummary] = useState<any | null>(null);
  const [matrixData, setMatrixData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadPlasmids() {
      try {
        const [sum, mat] = await Promise.all([
          api.getPlasmidSummary(),
          api.getPlasmidMatrix(),
        ]);
        setSummary(sum);
        setMatrixData(mat);
      } catch (err) {
        console.error('Failed to load plasmid data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadPlasmids();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div>
          <h1 className="text-xl font-bold text-white tracking-wide">Plasmid Characterization & MOB-Suite</h1>
          <p className="text-xs text-slate-400">
            Reconstructed extrachromosomal replicon incompatibility typing and chromosome-vs-plasmid AMR partitioning
          </p>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Reconstructed Plasmids</div>
          <div className="text-2xl font-bold font-mono text-white">{summary?.total_plasmids || 0}</div>
          <div className="text-[11px] text-slate-400">MOB-recon circularized and clustered contigs</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Conjugative Mobility</div>
          <div className="text-2xl font-bold font-mono text-crimson-400">
            {summary?.mobility_distribution?.CONJUGATIVE || 0} Plasmids
          </div>
          <div className="text-[11px] text-slate-400">Autonomous horizontal gene transfer machinery</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
          <div className="text-xs font-mono uppercase text-slate-400">Dominant Incompatibility Groups</div>
          <div className="text-xl font-bold font-mono text-blue-400">IncFII, IncX3, IncA/C</div>
          <div className="text-[11px] text-slate-400">Major epidemic vehicles for carbapenemases</div>
        </div>
      </div>

      {/* Chromosome vs. Plasmid Matrix */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
        <div>
          <h3 className="text-sm font-semibold text-white">Chromosome vs. Plasmid Genetic Context Partitioning</h3>
          <p className="text-xs text-slate-400">Physical localization of resistance determinant classes</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs font-mono border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-slate-500 text-[11px] uppercase">
                <th className="py-2.5 px-4 text-left">Antimicrobial Class</th>
                <th className="py-2.5 px-4 text-center">Total Detections</th>
                <th className="py-2.5 px-4 text-center">Chromosomal</th>
                <th className="py-2.5 px-4 text-center">Plasmid-Borne</th>
                <th className="py-2.5 px-4 text-right">Plasmid Localization (%)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {matrixData?.data?.map((row: any) => (
                <tr key={row.drug_class} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-2.5 px-4 font-semibold text-slate-200">{row.drug_class}</td>
                  <td className="py-2.5 px-4 text-center text-slate-400">{row.total}</td>
                  <td className="py-2.5 px-4 text-center text-slate-300 font-bold">{row.chromosome_count}</td>
                  <td className="py-2.5 px-4 text-center text-crimson-400 font-bold">{row.plasmid_count}</td>
                  <td className="py-2.5 px-4 text-right">
                    <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-200 font-bold">
                      {row.plasmid_percentage}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

