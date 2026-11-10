import React, { useState } from 'react';
import { PartitionedResistomeData, PartitionedResistomeGene } from '../../types';
import { Layers, Dna, SlidersHorizontal, Info } from 'lucide-react';

interface ChromosomeVsPlasmidHeatmapProps {
  data: PartitionedResistomeData;
}

export const ChromosomeVsPlasmidHeatmap: React.FC<ChromosomeVsPlasmidHeatmapProps> = ({ data }) => {
  const [activeCell, setActiveCell] = useState<{
    panel: 'Chromosome' | 'Plasmid';
    gene: string;
    isolate: string;
    copyNumber: number;
    drugClass: string;
    mechanism: string;
  } | null>(null);

  const { isolates, chromosomal, plasmid } = data;

  const getCopyColor = (val: number, panel: 'chrom' | 'plasmid') => {
    if (val === 0) return 'bg-slate-950/80 text-slate-700';
    if (panel === 'chrom') {
      // Chromosome palette (light green / cyan / blue)
      if (val === 1) return 'bg-emerald-900/80 border border-emerald-600/70 text-emerald-200 font-bold';
      return 'bg-cyan-500 border border-cyan-300 text-slate-950 font-black';
    } else {
      // Plasmid palette (yellow / orange / crimson / purple)
      if (val === 1) return 'bg-amber-500/80 border border-amber-400 text-slate-950 font-bold';
      if (val === 2) return 'bg-crimson-600 border border-crimson-400 text-white font-bold';
      return 'bg-purple-600 border border-purple-400 text-white font-black';
    }
  };

  const renderPanel = (
    title: string,
    panelType: 'chrom' | 'plasmid',
    genes: PartitionedResistomeGene[],
    matrix: number[][]
  ) => {
    return (
      <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3 sm:p-4 flex-1 space-y-3 overflow-hidden">
        <div className="flex justify-between items-center border-b border-slate-800 pb-2">
          <div className="flex items-center space-x-2">
            <span
              className={`w-3 h-3 rounded-full ${
                panelType === 'chrom' ? 'bg-emerald-500' : 'bg-crimson-500'
              }`}
            ></span>
            <h4 className="font-bold text-sm text-white">{title}</h4>
          </div>
          <span className="text-[11px] font-mono text-slate-400">
            {genes.length} Genes &bull; {isolates.length} Isolates
          </span>
        </div>

        {/* Heatmap Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-[11px] font-mono border-collapse select-none">
            <thead>
              <tr>
                <th className="p-1.5 text-left text-slate-500 font-normal w-32 truncate">Gene / Target</th>
                <th className="p-1 text-center text-slate-500 font-normal w-6">Cls</th>
                {isolates.map((iso) => (
                  <th
                    key={iso}
                    className="p-1 text-slate-400 rotate-[-55deg] origin-bottom-left h-24 truncate font-normal text-[9.5px] max-w-[20px]"
                    title={iso}
                  >
                    {iso.split(' ')[0]}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {genes.map((gene, rIdx) => (
                <tr key={gene.name} className="hover:bg-slate-900/50 transition-colors">
                  {/* Gene Name */}
                  <td className="p-1.5 font-bold text-slate-300 whitespace-nowrap text-right pr-2">
                    {gene.name}
                  </td>
                  {/* Drug Class Color Sidebar */}
                  <td className="p-0.5 text-center">
                    <span
                      className="w-2.5 h-4 rounded-sm inline-block"
                      style={{ backgroundColor: gene.class_color }}
                      title={`${gene.drug_class} (${gene.mechanism})`}
                    ></span>
                  </td>
                  {/* Cells */}
                  {isolates.map((iso, cIdx) => {
                    const copyNum = matrix[rIdx]?.[cIdx] ?? 0;
                    return (
                      <td
                        key={iso}
                        onClick={() =>
                          setActiveCell({
                            panel: panelType === 'chrom' ? 'Chromosome' : 'Plasmid',
                            gene: gene.name,
                            isolate: iso,
                            copyNumber: copyNum,
                            drugClass: gene.drug_class,
                            mechanism: gene.mechanism,
                          })
                        }
                        className={`p-0.5 text-center cursor-pointer transition-all ${getCopyColor(
                          copyNum,
                          panelType
                        )}`}
                        title={`${iso} | ${gene.name}: ${copyNum} copy`}
                      >
                        <div className="w-4 h-4 mx-auto flex items-center justify-center text-[9px]">
                          {copyNum > 0 ? copyNum : ''}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4 shadow-2xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
        <div>
          <div className="flex items-center space-x-2">
            <Layers className="w-4 h-4 text-crimson-400" />
            <h3 className="text-sm sm:text-base font-bold text-white tracking-wide">
              {data.title || 'Partitioned Resistome Architecture (Chromosome vs. Plasmid)'}
            </h3>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            Decoupled comparative heatmaps: (A) Core intrinsic chromosomal mechanisms vs. (B) Horizontally acquired plasmid cargo
          </p>
        </div>

        {/* Copy number legend */}
        <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
          <div className="flex items-center space-x-1">
            <span className="w-3 h-3 bg-slate-950 border border-slate-800 rounded-sm"></span>
            <span className="text-slate-400">0 Copy</span>
          </div>
          <div className="flex items-center space-x-1">
            <span className="w-3 h-3 bg-amber-500 rounded-sm"></span>
            <span className="text-slate-300">1 Copy</span>
          </div>
          <div className="flex items-center space-x-1">
            <span className="w-3 h-3 bg-crimson-600 rounded-sm"></span>
            <span className="text-slate-300">2 Copies</span>
          </div>
          <div className="flex items-center space-x-1">
            <span className="w-3 h-3 bg-purple-600 rounded-sm"></span>
            <span className="text-slate-300">3+ Copies</span>
          </div>
        </div>
      </div>

      {/* Side-by-Side Dual Panels */}
      <div className="flex flex-col xl:flex-row gap-4 w-full">
        {renderPanel('(A) Chromosomal Resistome', 'chrom', chromosomal.genes, chromosomal.matrix)}
        {renderPanel('(B) Plasmid-Borne Resistome', 'plasmid', plasmid.genes, plasmid.matrix)}
      </div>

      {/* Interactive Selected Cell Banner */}
      {activeCell && (
        <div className="bg-slate-950 border border-slate-700 p-3 rounded-xl flex justify-between items-center text-xs font-mono">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-slate-400">Selected:</span>
            <span className="font-bold text-white">{activeCell.isolate}</span>
            <span>&bull;</span>
            <span className="text-crimson-400 font-bold">{activeCell.gene}</span>
            <span>&bull;</span>
            <span className="text-amber-400">Context: {activeCell.panel}</span>
            <span>&bull;</span>
            <span className="text-slate-300">Copy Number: {activeCell.copyNumber}</span>
            <span>&bull;</span>
            <span className="text-emerald-400">Class: {activeCell.drugClass} ({activeCell.mechanism})</span>
          </div>
          <button
            onClick={() => setActiveCell(null)}
            className="text-slate-400 hover:text-white underline ml-3 shrink-0"
          >
            Dismiss
          </button>
        </div>
      )}
    </div>
  );
};

