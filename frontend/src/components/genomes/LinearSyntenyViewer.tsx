import React, { useState } from 'react';
import { LinearSyntenyData, SyntenyLocus, SyntenyGene } from '../../types';
import { Layers, ArrowRight, Dna, Info, Sliders } from 'lucide-react';

interface LinearSyntenyViewerProps {
  data: LinearSyntenyData;
}

export const LinearSyntenyViewer: React.FC<LinearSyntenyViewerProps> = ({ data }) => {
  const [selectedLocusId, setSelectedLocusId] = useState<string>(data.loci[0]?.id || 'locus_tn4401');
  const [hoveredGene, setHoveredGene] = useState<SyntenyGene | null>(null);

  const activeLocus = data.loci.find((l) => l.id === selectedLocusId) || data.loci[0];
  if (!activeLocus) return null;

  const width = 840;
  const height = 220;
  const padX = 50;
  const plotW = width - padX * 2;
  const trackY = 110;

  const getX = (bp: number) => padX + (bp / activeLocus.length_bp) * plotW;

  // Render directional gene arrow path
  const renderGeneArrow = (gene: SyntenyGene) => {
    const x1 = getX(gene.start);
    const x2 = getX(gene.end);
    const geneW = Math.max(14, Math.abs(x2 - x1));
    const arrowHeadW = Math.min(10, geneW * 0.4);
    const h = 26;
    const yTop = trackY - h / 2;
    const yBottom = trackY + h / 2;

    let pathD = '';
    if (gene.strand === '+') {
      const xBodyEnd = Math.max(x1, x2 - arrowHeadW);
      pathD = `M ${x1} ${yTop} L ${xBodyEnd} ${yTop} L ${x2} ${trackY} L ${xBodyEnd} ${yBottom} L ${x1} ${yBottom} Z`;
    } else {
      const xBodyStart = Math.min(x2, x1 + arrowHeadW);
      pathD = `M ${xBodyStart} ${yTop} L ${x2} ${yTop} L ${x2} ${yBottom} L ${xBodyStart} ${yBottom} L ${x1} ${trackY} Z`;
    }

    const isHovered = hoveredGene?.name === gene.name;

    return (
      <g
        key={gene.name}
        className="cursor-pointer transition-transform hover:opacity-90"
        onMouseEnter={() => setHoveredGene(gene)}
        onMouseLeave={() => setHoveredGene(null)}
      >
        <path
          d={pathD}
          fill={gene.color}
          stroke={isHovered ? '#ffffff' : '#0f172a'}
          strokeWidth={isHovered ? '2' : '1.2'}
        />
        {/* Gene name text inside arrow if wide enough */}
        {geneW > 35 && (
          <text
            x={(x1 + x2) / 2}
            y={trackY + 4}
            textAnchor="middle"
            fill="#ffffff"
            fontSize="9"
            fontFamily="monospace"
            fontWeight="bold"
            pointerEvents="none"
          >
            {gene.name}
          </text>
        )}
      </g>
    );
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4 shadow-2xl">
      {/* Title & Locus Selector */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
        <div>
          <div className="flex items-center space-x-2">
            <Layers className="w-4 h-4 text-crimson-400" />
            <h3 className="text-sm sm:text-base font-bold text-white tracking-wide">
              {data.title || 'Linear Genetic Synteny & Resistance Island Maps'}
            </h3>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            Standard: {data.reference_standard} • Oriented gene arrows reveal horizontal transfer boundaries
          </p>
        </div>

        {/* Locus Tabs */}
        <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs font-mono overflow-x-auto w-full sm:w-auto scrollbar-none">
          {data.loci.map((locus) => (
            <button
              key={locus.id}
              onClick={() => setSelectedLocusId(locus.id)}
              className={`px-3 py-1.5 rounded-md transition-all whitespace-nowrap ${
                selectedLocusId === locus.id
                  ? 'bg-crimson-800 text-white font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {locus.name.split(' ')[0]}
            </button>
          ))}
        </div>
      </div>

      {/* Locus Metadata Banner */}
      <div className="bg-slate-950/80 border border-slate-800/80 p-3 rounded-xl flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
        <div>
          <span className="text-slate-400">Active Locus: </span>
          <span className="text-white font-bold">{activeLocus.name}</span>
        </div>
        <div>
          <span className="text-slate-400">Context: </span>
          <span className="text-emerald-400 font-semibold">{activeLocus.host_context}</span>
        </div>
        <div>
          <span className="text-slate-400">Target Site Duplication: </span>
          <span className="text-amber-400 font-bold">{activeLocus.target_site_duplication}</span>
        </div>
        <div>
          <span className="text-slate-400">Length: </span>
          <span className="text-slate-200">{activeLocus.length_bp.toLocaleString()} bp</span>
        </div>
      </div>

      {/* SVG Synteny Canvas */}
      <div className="relative w-full border border-slate-800/80 bg-slate-950/60 rounded-xl overflow-hidden p-2">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto select-none">
          {/* Chromosome / Plasmid Backbone Line */}
          <line
            x1={padX - 20}
            y1={trackY}
            x2={width - padX + 20}
            y2={trackY}
            stroke="#334155"
            strokeWidth="3"
            strokeLinecap="round"
          />

          {/* Coordinate Scale Bar */}
          <g transform={`translate(${padX}, ${height - 35})`}>
            <line x1={0} y1={0} x2={plotW} y2={0} stroke="#475569" strokeWidth="1" />
            {[0, 0.25, 0.5, 0.75, 1.0].map((ratio) => {
              const bp = Math.round(ratio * activeLocus.length_bp);
              const xPos = ratio * plotW;
              return (
                <g key={ratio}>
                  <line x1={xPos} y1={-4} x2={xPos} y2={4} stroke="#64748b" strokeWidth="1.2" />
                  <text
                    x={xPos}
                    y={16}
                    textAnchor="middle"
                    fill="#94a3b8"
                    fontSize="9"
                    fontFamily="monospace"
                  >
                    {(bp / 1000).toFixed(1)} kb
                  </text>
                </g>
              );
            })}
          </g>

          {/* Flanking Inverted Repeat / Target Site Boundary Pins */}
          <g>
            {/* Left Boundary */}
            <line x1={padX} y1={trackY - 30} x2={padX} y2={trackY + 30} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="3,3" />
            <text x={padX} y={trackY - 36} textAnchor="middle" fill="#f59e0b" fontSize="9" fontFamily="monospace" fontWeight="bold">
              {activeLocus.flanking_repeats.left}
            </text>

            {/* Right Boundary */}
            <line x1={width - padX} y1={trackY - 30} x2={width - padX} y2={trackY + 30} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="3,3" />
            <text x={width - padX} y={trackY - 36} textAnchor="middle" fill="#f59e0b" fontSize="9" fontFamily="monospace" fontWeight="bold">
              {activeLocus.flanking_repeats.right}
            </text>
          </g>

          {/* Directional Gene Arrows */}
          {activeLocus.genes.map((gene) => renderGeneArrow(gene))}
        </svg>

        {/* Hovered Gene Tooltip Overlay */}
        {hoveredGene && (
          <div className="absolute top-2 right-2 bg-slate-900/95 backdrop-blur-md border border-slate-700/80 p-2.5 rounded-lg shadow-xl text-xs font-mono max-w-xs space-y-1">
            <div className="flex justify-between items-center text-white font-bold">
              <span style={{ color: hoveredGene.color }}>{hoveredGene.name}</span>
              <span className="text-[10px] text-slate-400">Strand ({hoveredGene.strand})</span>
            </div>
            <div className="text-slate-300 text-[11px]">{hoveredGene.label || hoveredGene.name}</div>
            <div className="text-[10px] text-slate-400">
              Coordinates: {hoveredGene.start} - {hoveredGene.end} bp ({hoveredGene.end - hoveredGene.start} bp)
            </div>
            <div className="text-[10px] font-semibold text-amber-400">Type: {hoveredGene.type}</div>
          </div>
        )}
      </div>

      {/* Color Category Legend */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-950/80 border border-slate-800/80 rounded-xl p-3 text-xs font-mono">
        <div className="flex items-center space-x-2">
          <span className="text-slate-400 font-semibold">Functional Annotation Categories:</span>
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-3 rounded bg-amber-500 inline-block"></span>
              <span className="text-slate-300 text-[11px]">MGE / Transposase / IS</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-3 rounded bg-crimson-600 inline-block"></span>
              <span className="text-slate-300 text-[11px]">Carbapenemase / Beta-Lactamase</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-3 rounded bg-sky-500 inline-block"></span>
              <span className="text-slate-300 text-[11px]">Aminoglycoside / Quinolone</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-3 rounded bg-purple-500 inline-block"></span>
              <span className="text-slate-300 text-[11px]">Colistin (mgrB Disruption)</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-3 rounded bg-slate-500 inline-block"></span>
              <span className="text-slate-300 text-[11px]">Passenger / Metabolic Protein</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

