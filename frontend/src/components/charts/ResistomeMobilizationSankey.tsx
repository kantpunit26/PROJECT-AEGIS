import React, { useState } from 'react';
import { MobilizationSankeyData, SankeyNode, SankeyLink } from '../../types';
import { Share2, Layers, Info } from 'lucide-react';

interface ResistomeMobilizationSankeyProps {
  data: MobilizationSankeyData;
}

export const ResistomeMobilizationSankey: React.FC<ResistomeMobilizationSankeyProps> = ({ data }) => {
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);

  const { nodes, links } = data;

  const width = 840;
  const height = 480;

  // Stages X positions: Stage 0 (Lineages), Stage 1 (ARGs), Stage 2 (Mobility)
  const stageX = [70, 390, 710];
  const nodeWidth = 18;

  // Group nodes by stage
  const stage0Nodes = nodes.filter((n) => n.stage === 0);
  const stage1Nodes = nodes.filter((n) => n.stage === 1);
  const stage2Nodes = nodes.filter((n) => n.stage === 2);

  // Calculate layout Y positions
  const layoutStage = (stageList: SankeyNode[]) => {
    const totalGap = 12 * (stageList.length - 1);
    const availableH = height - 80 - totalGap;
    const hPerNode = availableH / stageList.length;

    return stageList.map((node, idx) => ({
      ...node,
      x: stageX[node.stage],
      y: 40 + idx * (hPerNode + 12),
      height: Math.max(16, hPerNode),
    }));
  };

  const layoutedStage0 = layoutStage(stage0Nodes);
  const layoutedStage1 = layoutStage(stage1Nodes);
  const layoutedStage2 = layoutStage(stage2Nodes);
  const allLayouted = [...layoutedStage0, ...layoutedStage1, ...layoutedStage2];

  // Map node id to layouted node
  const nodeMap = new Map(allLayouted.map((n) => [n.id, n]));

  // Cubic Bezier path generator for links
  const renderFlowRibbon = (link: SankeyLink, idx: number) => {
    const src = nodeMap.get(link.source);
    const tgt = nodeMap.get(link.target);
    if (!src || !tgt) return null;

    const x0 = src.x + nodeWidth;
    const y0 = src.y + src.height / 2;
    const x1 = tgt.x;
    const y1 = tgt.y + tgt.height / 2;
    const dx = (x1 - x0) * 0.5;

    const isConnected =
      hoveredNodeId === link.source || hoveredNodeId === link.target;

    const strokeColor = src.color || '#64748b';
    const strokeWidth = Math.max(1.8, Math.min(10, link.value * 0.28));

    return (
      <path
        key={idx}
        d={`M ${x0} ${y0} C ${x0 + dx} ${y0}, ${x1 - dx} ${y1}, ${x1} ${y1}`}
        fill="none"
        stroke={strokeColor}
        strokeWidth={strokeWidth}
        strokeOpacity={hoveredNodeId ? (isConnected ? 0.85 : 0.08) : 0.4}
        className="transition-all duration-200"
      />
    );
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4 shadow-2xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
        <div>
          <div className="flex items-center space-x-2">
            <Share2 className="w-4 h-4 text-crimson-400" />
            <h3 className="text-sm sm:text-base font-bold text-white tracking-wide">
              {data.title || 'Resistome Mobilization Alluvial Flow (Sankey)'}
            </h3>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            Trace horizontal flow of resistance gene subtypes from bacterial lineages to mobile plasmids vs. chromosomal retention
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono text-slate-400">
          <Info className="w-3.5 h-3.5 text-blue-400" />
          <span>Hover on any node to isolate flow paths</span>
        </div>
      </div>

      {/* SVG Canvas */}
      <div className="relative w-full border border-slate-800/80 bg-slate-950/60 rounded-xl overflow-hidden p-2">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto select-none">
          {/* Column Stage Headers */}
          <text x={stageX[0]} y={24} textAnchor="start" fill="#94a3b8" fontSize="11" fontFamily="monospace" fontWeight="bold">
            STAGE 1: LINEAGE / CLADE
          </text>
          <text x={stageX[1]} y={24} textAnchor="middle" fill="#94a3b8" fontSize="11" fontFamily="monospace" fontWeight="bold">
            STAGE 2: ARG SUBTYPE
          </text>
          <text x={stageX[2]} y={24} textAnchor="end" fill="#94a3b8" fontSize="11" fontFamily="monospace" fontWeight="bold">
            STAGE 3: MOBILITY STATUS
          </text>

          {/* Flow Links */}
          <g>{links.map((link, idx) => renderFlowRibbon(link, idx))}</g>

          {/* Nodes */}
          {allLayouted.map((node) => {
            const isHovered = hoveredNodeId === node.id;
            return (
              <g
                key={node.id}
                className="cursor-pointer"
                onMouseEnter={() => setHoveredNodeId(node.id)}
                onMouseLeave={() => setHoveredNodeId(null)}
              >
                {/* Node Bar */}
                <rect
                  x={node.x}
                  y={node.y}
                  width={nodeWidth}
                  height={node.height}
                  rx="3"
                  fill={node.color}
                  stroke={isHovered ? '#ffffff' : '#0f172a'}
                  strokeWidth={isHovered ? '2' : '1'}
                />

                {/* Node Label */}
                <text
                  x={
                    node.stage === 0
                      ? node.x - 8
                      : node.stage === 1
                      ? node.x + nodeWidth / 2
                      : node.x + nodeWidth + 8
                  }
                  y={node.stage === 1 ? node.y - 4 : node.y + node.height / 2 + 4}
                  textAnchor={node.stage === 0 ? 'end' : node.stage === 1 ? 'middle' : 'start'}
                  fill={isHovered ? '#ffffff' : '#e2e8f0'}
                  fontSize={node.stage === 1 ? '9.5' : '10.5'}
                  fontFamily="monospace"
                  fontWeight={isHovered ? 'bold' : 'normal'}
                >
                  {node.name}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Footer Info */}
      <div className="flex flex-wrap items-center justify-between gap-2 bg-slate-950/80 border border-slate-800/80 rounded-xl p-3 text-xs font-mono text-slate-400">
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded bg-crimson-600 inline-block"></span>
          <span>Red: Highly mobile plasmid cargo (blaNDM-5, blaKPC-2, blaOXA-181)</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded bg-amber-500 inline-block"></span>
          <span>Amber: Transposon-associated (IS26 / composite transposons)</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded bg-blue-500 inline-block"></span>
          <span>Blue: Chromosomally conserved intrinsic core (fosA, oqxAB)</span>
        </div>
      </div>
    </div>
  );
};

