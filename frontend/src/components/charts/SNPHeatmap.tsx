import React, { useState } from 'react';
import { SNPMatrixData } from '../../types';
import { AlertCircle } from 'lucide-react';

interface SNPHeatmapProps {
  data: SNPMatrixData;
  outbreakThreshold?: number;
}

export const SNPHeatmap: React.FC<SNPHeatmapProps> = ({ data, outbreakThreshold = 15 }) => {
  const [hoveredCell, setHoveredCell] = useState<{
    isoA: string;
    isoB: string;
    dist: number;
    isOutbreak: boolean;
  } | null>(null);

  const { accessions, distance_matrix } = data;

  const getCellColor = (dist: number, isDiag: boolean) => {
    if (isDiag) return 'bg-slate-900 border-slate-800 text-slate-500';
    if (dist <= outbreakThreshold) {
      return 'bg-crimson-600 text-white font-bold ring-2 ring-crimson-400 animate-pulse';
    }
    if (dist <= 100) return 'bg-amber-600 text-white font-semibold';
    if (dist <= 1000) return 'bg-orange-800 text-orange-200';
    if (dist <= 15000) return 'bg-slate-800 text-slate-400';
    return 'bg-slate-900 text-slate-500';
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <h3 className="text-sm font-semibold text-white">Core-Genome Pairwise SNP Distance Matrix</h3>
          <p className="text-xs text-slate-400">
            Reference: {data.reference_genome} | Core Alignment: {data.total_core_positions.toLocaleString()} bp
          </p>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="flex items-center space-x-1.5 bg-crimson-950/70 border border-crimson-700/60 px-2.5 py-1 rounded">
            <span className="w-2.5 h-2.5 rounded bg-crimson-600 inline-block animate-pulse"></span>
            <span className="text-crimson-300 font-semibold">&le; {outbreakThreshold} SNPs (Outbreak Link)</span>
          </div>
          <div className="flex items-center space-x-1.5 bg-slate-800 px-2.5 py-1 rounded">
            <span className="w-2.5 h-2.5 rounded bg-slate-700 inline-block"></span>
            <span className="text-slate-300">&gt; 1,000 SNPs</span>
          </div>
        </div>
      </div>

      {/* Heatmap Grid */}
      <div className="overflow-x-auto pb-2">
        <table className="text-xs font-mono border-collapse">
          <thead>
            <tr>
              <th className="p-2 text-left text-slate-500"></th>
              {accessions.map((acc) => (
                <th key={acc} className="p-2 text-slate-300 rotate-[-45deg] origin-bottom-left h-24 text-[11px] font-medium">
                  {acc}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {accessions.map((accRow, rIdx) => (
              <tr key={accRow}>
                <td className="p-2 font-medium text-slate-300 whitespace-nowrap text-right pr-3 text-[11px]">
                  {accRow}
                </td>
                {distance_matrix[rIdx]?.map((dist, cIdx) => {
                  const isDiag = rIdx === cIdx;
                  const isOutbreak = !isDiag && dist <= outbreakThreshold;

                  return (
                    <td
                      key={`${rIdx}-${cIdx}`}
                      onMouseEnter={() =>
                        setHoveredCell({
                          isoA: accessions[rIdx],
                          isoB: accessions[cIdx],
                          dist,
                          isOutbreak,
                        })
                      }
                      onMouseLeave={() => setHoveredCell(null)}
                      className={`p-2.5 text-center border border-slate-800/80 cursor-pointer transition-all ${getCellColor(
                        dist,
                        isDiag
                      )}`}
                    >
                      {dist.toLocaleString()}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Cell Inspect Tooltip */}
      {hoveredCell && (
        <div className="bg-slate-800/90 border border-slate-700 p-3 rounded-lg text-xs font-mono flex items-center justify-between">
          <div>
            <span className="text-slate-400">Pairwise Comparison: </span>
            <span className="text-white font-bold">{hoveredCell.isoA}</span>
            <span className="text-slate-400"> vs </span>
            <span className="text-white font-bold">{hoveredCell.isoB}</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-slate-400">Distance:</span>
            <span className={`font-bold ${hoveredCell.isOutbreak ? 'text-crimson-400' : 'text-slate-200'}`}>
              {hoveredCell.dist} SNPs
            </span>
            {hoveredCell.isOutbreak && (
              <span className="flex items-center space-x-1 text-crimson-400 font-bold bg-crimson-950 px-2 py-0.5 rounded border border-crimson-800">
                <AlertCircle className="w-3.5 h-3.5" />
                <span>EPIDEMIOLOGICAL CLUSTER</span>
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

