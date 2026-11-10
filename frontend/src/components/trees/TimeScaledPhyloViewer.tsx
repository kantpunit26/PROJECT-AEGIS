import React, { useState } from 'react';
import { TimeScaledTreeData, TimeScaledLeaf } from '../../types';
import { Clock, ShieldAlert, GitBranch, Info, UserCheck, AlertCircle } from 'lucide-react';

interface TimeScaledPhyloViewerProps {
  data: TimeScaledTreeData;
}

export const TimeScaledPhyloViewer: React.FC<TimeScaledPhyloViewerProps> = ({ data }) => {
  const [selectedLeaf, setSelectedLeaf] = useState<TimeScaledLeaf | null>(null);

  const { timeline, leaves, internal_nodes, tree_lines, wards_legend } = data;

  const width = 840;
  const height = 580;
  const paddingLeft = 140;
  const paddingRight = 180;
  const treeWidth = width - paddingLeft - paddingRight;

  const wardColorMap: Record<string, string> = {
    'Ward A': '#eab308', // Yellow
    'Ward B': '#e11d48', // Red
    'Ward C': '#06b6d4', // Cyan
    'Ward B/C': '#a855f7', // Purple
    'HCW': '#10b981', // Emerald
  };

  const getXCoord = (ratio: number) => paddingLeft + ratio * treeWidth;

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4 shadow-2xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
        <div>
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-crimson-400" />
            <h3 className="text-sm sm:text-base font-bold text-white tracking-wide">
              {data.title || 'Time-Scaled Bayesian Phylodynamic Tree'}
            </h3>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            Model: {data.model} • Clock rate: {data.mean_clock_rate} • Root TMRCA: {data.tmrca}
          </p>
        </div>

        {/* Clade classification tag */}
        <div className="flex items-center space-x-2 text-xs font-mono">
          <span className="px-2 py-1 rounded bg-slate-800 border border-slate-700 text-slate-300">
            Outbreak Reconstruction: Ward B & A/C Cross-Transmission
          </span>
        </div>
      </div>

      {/* Main SVG Tree Canvas */}
      <div className="relative w-full border border-slate-800/80 bg-slate-950/60 rounded-xl overflow-hidden">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto select-none">
          {/* Outbreak Timeline Grid Lines & Headers */}
          {timeline.map((t, idx) => {
            const x = getXCoord(t.pos);
            return (
              <g key={idx}>
                {/* Vertical grid line */}
                <line x1={x} y1={20} x2={x} y2={height - 40} stroke="#1e293b" strokeWidth="1" strokeDasharray="3,3" />
                {/* Bottom Timeline Date */}
                <text
                  x={x}
                  y={height - 20}
                  textAnchor="middle"
                  fill="#94a3b8"
                  fontSize="10"
                  fontFamily="monospace"
                  fontWeight="600"
                >
                  {t.year}
                </text>
              </g>
            );
          })}

          {/* Timeline axis baseline */}
          <line
            x1={paddingLeft}
            y1={height - 35}
            x2={paddingLeft + treeWidth}
            y2={height - 35}
            stroke="#475569"
            strokeWidth="1.5"
          />

          {/* Shaded Outbreak Expansion Window (Mar 2010 - Oct 2010) */}
          <rect
            x={getXCoord(0.5)}
            y={20}
            width={treeWidth * 0.5}
            height={height - 60}
            fill="#334155"
            fillOpacity="0.12"
          />
          <text
            x={getXCoord(0.75)}
            y={32}
            textAnchor="middle"
            fill="#64748b"
            fontSize="9.5"
            fontFamily="monospace"
            letterSpacing="1"
          >
            ACTIVE NOSOCOMIAL OUTBREAK TRANSMISSION PERIOD
          </text>

          {/* 95% HPD Uncertainty Bars on Internal Nodes */}
          {internal_nodes.map((node) => {
            const x1 = getXCoord(node.hpd_low);
            const x2 = getXCoord(node.hpd_high);
            const y = node.y;
            return (
              <g key={`hpd-${node.id}`}>
                <rect
                  x={x1}
                  y={y - 5}
                  width={Math.max(6, x2 - x1)}
                  height={10}
                  rx="3"
                  fill="#0ea5e9"
                  fillOpacity="0.22"
                  stroke="#38bdf8"
                  strokeWidth="0.8"
                />
                {node.posterior && (
                  <text
                    x={getXCoord(node.x) + 4}
                    y={y - 7}
                    fill="#38bdf8"
                    fontSize="8.5"
                    fontFamily="monospace"
                    fontWeight="bold"
                  >
                    {node.posterior.toFixed(2)}
                  </text>
                )}
                {node.label && (
                  <text
                    x={getXCoord(node.x) - 4}
                    y={y + 16}
                    textAnchor="end"
                    fill="#94a3b8"
                    fontSize="8.5"
                    fontFamily="monospace"
                  >
                    {node.label}
                  </text>
                )}
              </g>
            );
          })}

          {/* Tree Phylogenetic Branch Lines */}
          {tree_lines.map((line, i) => (
            <line
              key={`line-${i}`}
              x1={getXCoord(line.x1)}
              y1={line.y1}
              x2={getXCoord(line.x2)}
              y2={line.y2}
              stroke="#cbd5e1"
              strokeWidth="1.8"
              strokeLinecap="round"
            />
          ))}

          {/* Tip Leaves / Isolates */}
          {leaves.map((leaf) => {
            const x = getXCoord(leaf.x);
            const y = leaf.y;
            const isSelected = selectedLeaf?.id === leaf.id;
            const color = wardColorMap[leaf.ward] || '#64748b';

            return (
              <g
                key={leaf.id}
                className="cursor-pointer transition-transform hover:scale-105"
                onClick={() => setSelectedLeaf(isSelected ? null : leaf)}
              >
                {/* Horizontal branch line from node to tip */}
                <line
                  x1={getXCoord(leaf.hpd_low)}
                  y1={y}
                  x2={x}
                  y2={y}
                  stroke="#64748b"
                  strokeWidth="1.2"
                  strokeDasharray="2,2"
                />

                {/* Tip Circle / HCW Icon */}
                <circle
                  cx={x}
                  cy={y}
                  r={leaf.is_hcw ? '7.5' : '6'}
                  fill={color}
                  stroke={isSelected ? '#ffffff' : '#020617'}
                  strokeWidth={isSelected ? '2.5' : '1.5'}
                />

                {/* Tip Leaf Label */}
                <text
                  x={x + 12}
                  y={y + 3.5}
                  fill={isSelected ? '#ffffff' : leaf.is_hcw ? '#10b981' : '#f1f5f9'}
                  fontSize={leaf.is_hcw ? '11' : '10'}
                  fontFamily={leaf.is_hcw ? 'sans-serif' : 'monospace'}
                  fontWeight={leaf.is_hcw || isSelected ? 'bold' : 'normal'}
                >
                  {leaf.label}
                </text>
              </g>
            );
          })}

          {/* Clade 1 & 2 Bracket Annotations on Right */}
          <g transform={`translate(${width - 40}, 0)`}>
            {/* Clade 1 Bracket */}
            <path d="M 0 25 L 10 25 L 10 205 L 18 205 L 10 205 L 10 395 L 0 395" fill="none" stroke="#94a3b8" strokeWidth="1.5" />
            <text x="22" y="210" fill="#f8fafc" fontSize="11" fontFamily="sans-serif" fontWeight="bold">
              Clade 1
            </text>

            {/* Clade 2 Bracket */}
            <path d="M 0 425 L 10 425 L 10 485 L 18 485 L 10 485 L 10 545 L 0 545" fill="none" stroke="#94a3b8" strokeWidth="1.5" />
            <text x="22" y="490" fill="#f8fafc" fontSize="11" fontFamily="sans-serif" fontWeight="bold">
              Clade 2
            </text>
          </g>
        </svg>

        {/* Selected Leaf Detail Popover */}
        {selectedLeaf && (
          <div className="absolute top-4 left-4 bg-slate-900/95 backdrop-blur-md border border-slate-700/80 p-3.5 rounded-xl shadow-2xl text-xs font-mono space-y-1.5 max-w-xs">
            <div className="flex justify-between items-center border-b border-slate-800 pb-1">
              <span className="font-bold text-white text-sm">{selectedLeaf.label}</span>
              <span
                className="px-2 py-0.5 rounded text-[10px] font-bold text-slate-900"
                style={{ backgroundColor: wardColorMap[selectedLeaf.ward] || '#64748b' }}
              >
                {selectedLeaf.ward}
              </span>
            </div>
            <div className="text-slate-300">
              Isolation Date: <strong className="text-white">{selectedLeaf.date}</strong>
            </div>
            <div className="text-slate-300">
              Phylodynamic Clade: <strong className="text-crimson-400">{selectedLeaf.clade}</strong>
            </div>
            {selectedLeaf.is_hcw && (
              <div className="text-emerald-400 text-[11px] font-bold pt-0.5">
                Identified as Healthcare Worker Nosocomial Carrier / Vector
              </div>
            )}
            <button
              onClick={() => setSelectedLeaf(null)}
              className="text-[10px] text-slate-400 hover:text-white underline pt-1 block"
            >
              Close
            </button>
          </div>
        )}
      </div>

      {/* Ward Legend */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-950/80 border border-slate-800/80 rounded-xl p-3 text-xs font-mono">
        <div className="flex items-center space-x-2">
          <span className="text-slate-400 font-semibold">Epidemiological Wards:</span>
          <div className="flex flex-wrap items-center gap-3">
            {wards_legend.map((w) => (
              <div key={w.ward} className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: w.color }}></span>
                <span className="text-slate-300 text-[11px]">{w.ward}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="flex items-center space-x-2 text-slate-400">
          <span className="w-5 h-2.5 rounded bg-sky-500/25 border border-sky-400 inline-block"></span>
          <span className="text-[11px]">95% HPD Divergence Uncertainty Interval</span>
        </div>
      </div>
    </div>
  );
};

