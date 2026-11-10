import React, { useState } from 'react';
import { MSTData, MSTNode, MSTEdge } from '../../types';
import { Network, ZoomIn, ZoomOut, AlertTriangle, Layers, Info } from 'lucide-react';

interface TransmissionNetworkMSTProps {
  data: MSTData;
}

export const TransmissionNetworkMST: React.FC<TransmissionNetworkMSTProps> = ({ data }) => {
  const [selectedNode, setSelectedNode] = useState<MSTNode | null>(null);
  const [hoveredEdge, setHoveredEdge] = useState<MSTEdge | null>(null);

  const { nodes, edges, outbreak_halos } = data;

  const sourceColors: Record<string, string> = {
    ICU: '#ef4444', // Red
    Bloodstream: '#3b82f6', // Blue
    Respiratory: '#10b981', // Green
    Surgical: '#eab308', // Yellow
    'Liver Abscess': '#a855f7', // Purple
    Urine: '#f97316', // Orange
    Sputum: '#06b6d4', // Cyan
    Other: '#64748b', // Slate
  };

  // Helper to render pie chart slices for a node
  const renderPieSlices = (node: MSTNode) => {
    const total = Object.values(node.sources).reduce((a, b) => a + b, 0);
    if (total === 0) return null;

    let cumulativeAngle = -Math.PI / 2;
    const slices: JSX.Element[] = [];

    const entries = Object.entries(node.sources);
    if (entries.length === 1) {
      const color = sourceColors[entries[0][0]] || '#64748b';
      return <circle cx={node.x} cy={node.y} r={node.radius} fill={color} stroke="#020617" strokeWidth="2" />;
    }

    entries.forEach(([source, count], idx) => {
      const fraction = count / total;
      const angle = fraction * 2 * Math.PI;
      const startAngle = cumulativeAngle;
      const endAngle = cumulativeAngle + angle;
      cumulativeAngle = endAngle;

      const x1 = node.x + node.radius * Math.cos(startAngle);
      const y1 = node.y + node.radius * Math.sin(startAngle);
      const x2 = node.x + node.radius * Math.cos(endAngle);
      const y2 = node.y + node.radius * Math.sin(endAngle);

      const largeArc = angle > Math.PI ? 1 : 0;
      const d = `M ${node.x} ${node.y} L ${x1} ${y1} A ${node.radius} ${node.radius} 0 ${largeArc} 1 ${x2} ${y2} Z`;

      slices.push(
        <path
          key={idx}
          d={d}
          fill={sourceColors[source] || '#64748b'}
          stroke="#020617"
          strokeWidth="1.2"
        />
      );
    });

    return <g>{slices}</g>;
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4 shadow-2xl">
      {/* Title & Metadata */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
        <div>
          <div className="flex items-center space-x-2">
            <Network className="w-4 h-4 text-crimson-500" />
            <h3 className="text-sm sm:text-base font-bold text-white tracking-wide">
              {data.title || 'Core-Genome Minimum Spanning Tree (MST)'}
            </h3>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            {data.method} • Node sizes reflect isolate frequency; pie slices reflect clinical source breakdown
          </p>
        </div>

        <div className="flex items-center space-x-2 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800 text-xs font-mono">
          <span className="w-2.5 h-2.5 rounded-full bg-crimson-600 animate-pulse"></span>
          <span className="text-slate-300">Outbreak Threshold: &le; 10 SNPs</span>
        </div>
      </div>

      {/* SVG MST Network Canvas */}
      <div className="relative w-full border border-slate-800/80 bg-slate-950/60 rounded-xl overflow-hidden">
        <svg viewBox="0 0 820 540" className="w-full h-auto select-none">
          <defs>
            <radialGradient id="halo-glow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#e11d48" stopOpacity="0.2" />
              <stop offset="100%" stopColor="#e11d48" stopOpacity="0" />
            </radialGradient>
          </defs>

          {/* Outbreak Cluster Halos (Dashed ellipses around <= 10 SNP transmission chains) */}
          {outbreak_halos.map((halo, i) => (
            <g key={i}>
              <ellipse
                cx={halo.center_x}
                cy={halo.center_y}
                rx={halo.radius_x}
                ry={halo.radius_y}
                fill={halo.color}
                fillOpacity="0.12"
                stroke={halo.color}
                strokeWidth="1.8"
                strokeDasharray="5,4"
              />
              <text
                x={halo.center_x}
                y={halo.center_y - halo.radius_y - 6}
                textAnchor="middle"
                fill={halo.color}
                fontSize="10"
                fontFamily="monospace"
                fontWeight="bold"
              >
                {halo.name} ({halo.snp_threshold})
              </text>
            </g>
          ))}

          {/* MST Edges with SNP Distance Labels */}
          {edges.map((edge, i) => {
            const sNode = nodes.find((n) => n.id === edge.source);
            const tNode = nodes.find((n) => n.id === edge.target);
            if (!sNode || !tNode) return null;

            const midX = (sNode.x + tNode.x) / 2;
            const midY = (sNode.y + tNode.y) / 2;

            const isHovered = hoveredEdge === edge;

            return (
              <g
                key={i}
                className="cursor-pointer"
                onMouseEnter={() => setHoveredEdge(edge)}
                onMouseLeave={() => setHoveredEdge(null)}
              >
                {/* Edge line */}
                <line
                  x1={sNode.x}
                  y1={sNode.y}
                  x2={tNode.x}
                  y2={tNode.y}
                  stroke={edge.outbreak_link ? '#e11d48' : isHovered ? '#f59e0b' : '#475569'}
                  strokeWidth={edge.outbreak_link ? '2.5' : isHovered ? '2' : '1.4'}
                  strokeDasharray={edge.outbreak_link ? undefined : '2,2'}
                />

                {/* SNP Distance Badge */}
                <rect
                  x={midX - 16}
                  y={midY - 9}
                  width="32"
                  height="18"
                  rx="4"
                  fill="#020617"
                  stroke={edge.outbreak_link ? '#e11d48' : '#334155'}
                  strokeWidth="1"
                />
                <text
                  x={midX}
                  y={midY + 4}
                  textAnchor="middle"
                  fill={edge.outbreak_link ? '#fb7185' : '#94a3b8'}
                  fontSize="9.5"
                  fontFamily="monospace"
                  fontWeight="bold"
                >
                  {edge.snp_distance}
                </text>
              </g>
            );
          })}

          {/* MST Nodes (Pie charts by clinical origin) */}
          {nodes.map((node) => {
            const isSelected = selectedNode?.id === node.id;
            return (
              <g
                key={node.id}
                className="cursor-pointer transition-transform hover:scale-110"
                onClick={() => setSelectedNode(isSelected ? null : node)}
              >
                {/* Selection outer pulse ring */}
                {isSelected && (
                  <circle
                    cx={node.x}
                    cy={node.y}
                    r={node.radius + 6}
                    fill="none"
                    stroke="#e11d48"
                    strokeWidth="2.5"
                    strokeDasharray="3,2"
                  />
                )}

                {/* Pie Chart node body */}
                {renderPieSlices(node)}

                {/* Node Label */}
                <text
                  x={node.x}
                  y={node.y + node.radius + 14}
                  textAnchor="middle"
                  fill="#f1f5f9"
                  fontSize="11"
                  fontFamily="sans-serif"
                  fontWeight="600"
                >
                  {node.label}
                </text>
                <text
                  x={node.x}
                  y={node.y + node.radius + 26}
                  textAnchor="middle"
                  fill="#94a3b8"
                  fontSize="9"
                  fontFamily="monospace"
                >
                  n={node.isolate_count} ({node.carbapenemase || 'WT'})
                </text>
              </g>
            );
          })}
        </svg>

        {/* Selected Node Details Card */}
        {selectedNode && (
          <div className="absolute top-3 right-3 bg-slate-900/95 backdrop-blur-md border border-slate-700/80 p-3.5 rounded-xl shadow-2xl text-xs font-mono space-y-2 max-w-xs">
            <div className="flex justify-between items-center border-b border-slate-800 pb-1.5">
              <span className="font-bold text-white text-sm">{selectedNode.label}</span>
              <span className="px-2 py-0.5 rounded bg-crimson-950 border border-crimson-800 text-crimson-400 font-bold">
                {selectedNode.sequence_type}
              </span>
            </div>
            <div className="text-slate-300">
              Isolates in Cluster: <strong className="text-white">{selectedNode.isolate_count}</strong>
            </div>
            <div className="text-slate-300">
              Carbapenemase: <strong className="text-amber-400">{selectedNode.carbapenemase || 'None'}</strong>
            </div>
            <div className="text-slate-300">
              Virulence Score: <strong className="text-emerald-400">{selectedNode.virulence_score}/5</strong>
            </div>

            {/* Source breakdown */}
            <div className="pt-1 space-y-1">
              <div className="text-[11px] text-slate-400 font-semibold uppercase">Epidemiological Isolation Sources:</div>
              <div className="grid grid-cols-2 gap-1.5 text-[11px]">
                {Object.entries(selectedNode.sources).map(([src, count]) => (
                  <div key={src} className="flex items-center space-x-1.5">
                    <span
                      className="w-2.5 h-2.5 rounded-full shrink-0"
                      style={{ backgroundColor: sourceColors[src] || '#64748b' }}
                    ></span>
                    <span className="text-slate-300 truncate">
                      {src}: {count}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <button
              onClick={() => setSelectedNode(null)}
              className="text-[11px] text-slate-400 hover:text-white underline pt-1"
            >
              Close
            </button>
          </div>
        )}
      </div>

      {/* Legend */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-950/80 border border-slate-800/80 rounded-xl p-3 text-xs font-mono">
        <div className="flex items-center space-x-2">
          <span className="text-slate-400 font-semibold">Clinical Sources:</span>
          <div className="flex flex-wrap items-center gap-3">
            {Object.entries(sourceColors).map(([src, color]) => (
              <div key={src} className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: color }}></span>
                <span className="text-slate-300 text-[11px]">{src}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="flex items-center space-x-2 text-slate-400">
          <span className="w-4 h-0.5 bg-crimson-500 inline-block"></span>
          <span className="text-[11px]">Solid red branch: &le; 10 SNPs Outbreak link</span>
        </div>
      </div>
    </div>
  );
};

