import React from 'react';

interface CoOccurrenceProps {
  data: {
    genes: string[];
    matrix: number[][];
  };
}

export const CoOccurrenceHeatmap: React.FC<CoOccurrenceProps> = ({ data }) => {
  const { genes, matrix } = data;
  if (!genes || genes.length === 0) return null;

  // Find max value in matrix for normalization
  let maxVal = 1;
  matrix.forEach((row) => row.forEach((val) => { if (val > maxVal) maxVal = val; }));

  const getHeatColor = (val: number, isDiag: boolean) => {
    if (val === 0) return 'bg-slate-900 text-slate-600';
    const intensity = val / maxVal;
    if (isDiag) return 'bg-slate-800 text-slate-300 font-bold';
    if (intensity > 0.7) return 'bg-crimson-600 text-white font-bold';
    if (intensity > 0.4) return 'bg-crimson-800 text-crimson-100';
    if (intensity > 0.2) return 'bg-crimson-950 text-crimson-300';
    return 'bg-slate-800/80 text-slate-400';
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div>
        <h3 className="text-sm font-semibold text-white">AMR Determinant Co-occurrence Matrix</h3>
        <p className="text-xs text-slate-400">Pairwise frequency of co-localized and co-selected resistance mechanisms</p>
      </div>

      <div className="overflow-x-auto">
        <table className="text-xs font-mono border-collapse">
          <thead>
            <tr>
              <th className="p-2 text-left text-slate-500"></th>
              {genes.map((g) => (
                <th key={g} className="p-2 text-slate-300 rotate-[-45deg] origin-bottom-left h-20 text-[11px] font-medium">
                  {g}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {genes.map((geneRow, rIdx) => (
              <tr key={geneRow}>
                <td className="p-2 font-medium text-slate-300 whitespace-nowrap text-right pr-3 text-[11px]">
                  {geneRow}
                </td>
                {matrix[rIdx]?.map((val, cIdx) => (
                  <td
                    key={`${rIdx}-${cIdx}`}
                    title={`${genes[rIdx]} + ${genes[cIdx]}: ${val} isolates`}
                    className={`p-2 text-center border border-slate-800/60 transition-colors cursor-pointer hover:border-crimson-500 ${getHeatColor(
                      val,
                      rIdx === cIdx
                    )}`}
                  >
                    {val}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

