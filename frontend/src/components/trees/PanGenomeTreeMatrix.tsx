import React, { useState } from 'react';
import { PanGenomeMatrixData } from '../../types';
import { GitBranch, Layers, ShieldCheck, Binary, SlidersHorizontal, CheckSquare } from 'lucide-react';

interface PanGenomeTreeMatrixProps {
  data: PanGenomeMatrixData;
}

export const PanGenomeTreeMatrix: React.FC<PanGenomeTreeMatrixProps> = ({ data }) => {
  const [hoveredRowIndex, setHoveredRowIndex] = useState<number | null>(null);

  const { taxa, arg_headers, arg_matrix, inc_headers, inc_matrix, vir_headers, vir_matrix } = data;

  const cladeColors: Record<string, string> = {
    'Clade 1': '#10b981', // Emerald
    'Clade 2': '#f97316', // Orange
    'Clade 3': '#ec4899', // Pink
    'Clade 4': '#38bdf8', // Sky
    'Clade 5': '#a855f7', // Purple
    'hvKP': '#eab308', // Yellow
    'Basal': '#64748b', // Slate
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4 shadow-2xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
        <div>
          <div className="flex items-center space-x-2">
            <GitBranch className="w-4 h-4 text-crimson-400" />
            <h3 className="text-sm sm:text-base font-bold text-white tracking-wide">
              {data.title || 'Pan-Genome Phylogeny Aligned Matrix (iTOL / ggtree)'}
            </h3>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            Synchronized multi-panel analysis aligning core-genome phylogeny with resistance determinants, plasmid replicons, and virulence profiles
          </p>
        </div>

        {/* Legend pills */}
        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded bg-crimson-600 inline-block"></span>
            <span className="text-slate-300">AMR Gene</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded bg-blue-600 inline-block"></span>
            <span className="text-slate-300">Plasmid Inc</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2.5 h-2.5 rounded bg-emerald-600 inline-block"></span>
            <span className="text-slate-300">Virulence</span>
          </div>
        </div>
      </div>

      {/* Synchronized Multi-Panel Scroll Container */}
      <div className="overflow-x-auto border border-slate-800/80 rounded-xl bg-slate-950/60 p-2 sm:p-4">
        <div className="min-w-[960px] space-y-1">
          {/* Header Row */}
          <div className="flex items-end text-[11px] font-mono uppercase text-slate-400 border-b border-slate-800 pb-3">
            {/* Tree Branch Stub & Taxa Info */}
            <div className="w-64 shrink-0 font-bold text-slate-300 px-2">Phylogenetic Clade & Taxon</div>
            <div className="w-16 shrink-0 text-center">Year</div>
            <div className="w-24 shrink-0 text-left">Origin</div>
            <div className="w-20 shrink-0 text-center">MLST</div>
            <div className="w-12 shrink-0 text-center">Clade</div>

            {/* Separator */}
            <div className="w-4 shrink-0"></div>

            {/* Panel 1: AMR Genes (Red) */}
            <div className="flex-1 flex justify-start space-x-1 px-1 border-l border-slate-800">
              {arg_headers.map((gene) => (
                <div
                  key={gene}
                  className="w-7 text-center rotate-[-45deg] origin-bottom-left h-24 truncate text-crimson-300 font-semibold text-[10px]"
                  title={gene}
                >
                  {gene}
                </div>
              ))}
            </div>

            {/* Separator */}
            <div className="w-4 shrink-0"></div>

            {/* Panel 2: Plasmid Incompatibility Types (Blue) */}
            <div className="w-48 shrink-0 flex justify-start space-x-1 px-1 border-l border-slate-800">
              {inc_headers.map((inc) => (
                <div
                  key={inc}
                  className="w-6 text-center rotate-[-45deg] origin-bottom-left h-24 truncate text-blue-300 font-semibold text-[10px]"
                  title={inc}
                >
                  {inc}
                </div>
              ))}
            </div>

            {/* Separator */}
            <div className="w-4 shrink-0"></div>

            {/* Panel 3: Virulence Factors (Green) */}
            <div className="w-48 shrink-0 flex justify-start space-x-1 px-1 border-l border-slate-800">
              {vir_headers.map((vir) => (
                <div
                  key={vir}
                  className="w-6 text-center rotate-[-45deg] origin-bottom-left h-24 truncate text-emerald-300 font-semibold text-[10px]"
                  title={vir}
                >
                  {vir}
                </div>
              ))}
            </div>
          </div>

          {/* Data Rows */}
          {taxa.map((taxon, rIdx) => {
            const isHovered = hoveredRowIndex === rIdx;
            const cladeCol = cladeColors[taxon.clade] || '#64748b';

            return (
              <div
                key={taxon.id}
                onMouseEnter={() => setHoveredRowIndex(rIdx)}
                onMouseLeave={() => setHoveredRowIndex(null)}
                className={`flex items-center text-xs font-mono py-1 px-2 rounded-lg transition-colors cursor-pointer ${
                  isHovered ? 'bg-slate-800/80' : rIdx % 2 === 0 ? 'bg-slate-900/40' : 'bg-transparent'
                }`}
              >
                {/* Dendrogram Branch Stub + Taxon Name */}
                <div className="w-64 shrink-0 flex items-center space-x-2 truncate">
                  <span className="text-slate-600 font-mono select-none">
                    {rIdx === 0 ? '┌──' : rIdx === taxa.length - 1 ? '└──' : '├──'}
                  </span>
                  <span className="w-3 h-0.5 bg-slate-700 inline-block"></span>
                  <span className="font-bold text-slate-100 truncate">{taxon.strain}</span>
                  <span className="text-slate-500 text-[10px]">({taxon.id.slice(0, 10)})</span>
                </div>

                <div className="w-16 shrink-0 text-center text-slate-400 text-[11px]">{taxon.year}</div>
                <div className="w-24 shrink-0 text-left text-slate-300 text-[11px] truncate">{taxon.city}</div>
                <div className="w-20 shrink-0 text-center">
                  <span className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-emerald-400 font-bold text-[10px]">
                    {taxon.mlst}
                  </span>
                </div>
                <div className="w-12 shrink-0 flex justify-center">
                  <span
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: cladeCol }}
                    title={taxon.clade}
                  ></span>
                </div>

                {/* Separator */}
                <div className="w-4 shrink-0"></div>

                {/* Panel 1: AMR Matrix Cells (Red) */}
                <div className="flex-1 flex justify-start space-x-1 px-1 border-l border-slate-800">
                  {arg_headers.map((_, cIdx) => {
                    const present = arg_matrix[rIdx]?.[cIdx];
                    return (
                      <div
                        key={cIdx}
                        className={`w-7 h-5 rounded flex items-center justify-center transition-all ${
                          present
                            ? 'bg-crimson-600 border border-crimson-500 text-white shadow-sm shadow-crimson-900'
                            : 'bg-slate-950/60 border border-slate-800/80 text-transparent'
                        }`}
                        title={`${taxon.strain} - ${arg_headers[cIdx]}: ${present ? 'PRESENT' : 'ABSENT'}`}
                      >
                        {present && <span className="w-2 h-2 bg-white rounded-sm"></span>}
                      </div>
                    );
                  })}
                </div>

                {/* Separator */}
                <div className="w-4 shrink-0"></div>

                {/* Panel 2: Plasmid Inc Cells (Blue) */}
                <div className="w-48 shrink-0 flex justify-start space-x-1 px-1 border-l border-slate-800">
                  {inc_headers.map((_, cIdx) => {
                    const present = inc_matrix[rIdx]?.[cIdx];
                    return (
                      <div
                        key={cIdx}
                        className={`w-6 h-5 rounded flex items-center justify-center transition-all ${
                          present
                            ? 'bg-blue-600 border border-blue-500 text-white shadow-sm shadow-blue-900'
                            : 'bg-slate-950/60 border border-slate-800/80 text-transparent'
                        }`}
                        title={`${taxon.strain} - ${inc_headers[cIdx]}: ${present ? 'PRESENT' : 'ABSENT'}`}
                      >
                        {present && <span className="w-1.5 h-1.5 bg-white rounded-sm"></span>}
                      </div>
                    );
                  })}
                </div>

                {/* Separator */}
                <div className="w-4 shrink-0"></div>

                {/* Panel 3: Virulence Cells (Green) */}
                <div className="w-48 shrink-0 flex justify-start space-x-1 px-1 border-l border-slate-800">
                  {vir_headers.map((_, cIdx) => {
                    const present = vir_matrix[rIdx]?.[cIdx];
                    return (
                      <div
                        key={cIdx}
                        className={`w-6 h-5 rounded flex items-center justify-center transition-all ${
                          present
                            ? 'bg-emerald-600 border border-emerald-500 text-white shadow-sm shadow-emerald-900'
                            : 'bg-slate-950/60 border border-slate-800/80 text-transparent'
                        }`}
                        title={`${taxon.strain} - ${vir_headers[cIdx]}: ${present ? 'PRESENT' : 'ABSENT'}`}
                      >
                        {present && <span className="w-1.5 h-1.5 bg-white rounded-sm"></span>}
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

