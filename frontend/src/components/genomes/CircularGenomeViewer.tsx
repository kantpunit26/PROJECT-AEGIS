import React, { useState } from 'react';
import { CircularAtlasData, CircularAtlasBin, CircularAtlasHotspot } from '../../types';
import { Dna, Eye, Layers, ShieldAlert, Sparkles, Sliders } from 'lucide-react';

interface CircularGenomeViewerProps {
  atlasData?: CircularAtlasData | null;
  coordinates?: any[];
  genomeSize?: number;
}

export const CircularGenomeViewer: React.FC<CircularGenomeViewerProps> = ({
  atlasData,
  coordinates,
  genomeSize = 5333942,
}) => {
  const [selectedHotspot, setSelectedHotspot] = useState<CircularAtlasHotspot | null>(null);
  const [hoveredBin, setHoveredBin] = useState<CircularAtlasBin | null>(null);
  const [showBlastRings, setShowBlastRings] = useState<boolean>(true);
  const [showVirulence, setShowVirulence] = useState<boolean>(true);
  const [showMGE, setShowMGE] = useState<boolean>(true);

  // Fallback synthetic bins if API data is still loading
  const bins: CircularAtlasBin[] = atlasData?.bins || [];
  const totalBins = bins.length || 100;

  // ViewBox & Radii configuration
  const size = 680;
  const center = size / 2;

  // Concentric track radii from outside to center
  const rContig = 310;
  const rCdsFwd = 292;
  const rCdsRev = 278;
  const rAmr = 260;
  const rVir = 244;
  const rMge = 228;
  // BLAST Clade rings (5 rings)
  const rBlast1 = 212; // Clade 1
  const rBlast2 = 200; // Clade 2
  const rBlast3 = 188; // Clade 3
  const rBlast4 = 176; // Clade 4
  const rBlast5 = 164; // Clade 5
  // GC Skew & Content center
  const rGcContent = 142;
  const rGcSkew = 112;
  const rInnerHole = 76;

  // Helper to get cartesian point from angle & radius
  const getPoint = (binIndex: number, radius: number) => {
    const angle = (binIndex / totalBins) * 2 * Math.PI - Math.PI / 2;
    return {
      x: center + radius * Math.cos(angle),
      y: center + radius * Math.sin(angle),
      angle
    };
  };

  const getAmrColor = (mechanism?: string) => {
    switch (mechanism) {
      case 'Inactivation':
        return '#e11d48'; // crimson
      case 'Target Protection':
        return '#0284c7'; // sky
      case 'Target Alteration':
        return '#f59e0b'; // amber
      case 'Efflux':
        return '#06b6d4'; // cyan
      default:
        return '#ef4444';
    }
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-3 sm:p-5 space-y-4 flex flex-col items-center w-full shadow-2xl">
      {/* Header and Controls */}
      <div className="w-full flex flex-col md:flex-row justify-between items-start md:items-center gap-3 border-b border-slate-800/80 pb-3.5">
        <div>
          <div className="flex items-center space-x-2">
            <Dna className="w-4 h-4 text-crimson-400" />
            <h3 className="text-sm sm:text-base font-bold text-white tracking-wide">
              Multi-Track Circular Genome Atlas (BRIG / Circos)
            </h3>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            {atlasData?.strain || 'K. pneumoniae HS11286 / ST11 (MDR-CRKP)'} • {(genomeSize / 1e6).toFixed(2)} Mbp • GC Mean: 57.3%
          </p>
        </div>

        {/* Track Visibility Toggles */}
        <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
          <button
            onClick={() => setShowBlastRings(!showBlastRings)}
            className={`px-2.5 py-1 rounded-md border text-[11px] transition-all flex items-center space-x-1.5 ${
              showBlastRings
                ? 'bg-blue-950/70 border-blue-700 text-blue-300 font-semibold'
                : 'bg-slate-950 border-slate-800 text-slate-500'
            }`}
          >
            <span>BLAST Rings (5 Clades)</span>
          </button>
          <button
            onClick={() => setShowVirulence(!showVirulence)}
            className={`px-2.5 py-1 rounded-md border text-[11px] transition-all flex items-center space-x-1.5 ${
              showVirulence
                ? 'bg-emerald-950/70 border-emerald-700 text-emerald-300 font-semibold'
                : 'bg-slate-950 border-slate-800 text-slate-500'
            }`}
          >
            <span>Virulence (VF)</span>
          </button>
          <button
            onClick={() => setShowMGE(!showMGE)}
            className={`px-2.5 py-1 rounded-md border text-[11px] transition-all flex items-center space-x-1.5 ${
              showMGE
                ? 'bg-amber-950/70 border-amber-700 text-amber-300 font-semibold'
                : 'bg-slate-950 border-slate-800 text-slate-500'
            }`}
          >
            <span>MGE / Islands</span>
          </button>
        </div>
      </div>

      {/* Main Circular SVG Canvas */}
      <div className="relative w-full flex justify-center max-w-[680px]">
        <svg viewBox={`0 0 ${size} ${size}`} className="w-full h-auto overflow-visible select-none">
          {/* Background Ambient Glow */}
          <circle cx={center} cy={center} r={rContig + 12} fill="#020617" opacity="0.6" />

          {/* 1. Track Outermost: Contig / Chromosome Backbone */}
          <circle cx={center} cy={center} r={rContig} fill="none" stroke="#1e293b" strokeWidth="6" />

          {/* Genomic coordinate tick marks (1 Mbp intervals) */}
          {[0, 1, 2, 3, 4, 5].map((mbp) => {
            const binIdx = Math.floor((mbp / 5.333942) * totalBins);
            const ptOuter = getPoint(binIdx, rContig + 10);
            const ptLabel = getPoint(binIdx, rContig + 22);
            return (
              <g key={mbp}>
                <line
                  x1={getPoint(binIdx, rContig - 4).x}
                  y1={getPoint(binIdx, rContig - 4).y}
                  x2={ptOuter.x}
                  y2={ptOuter.y}
                  stroke="#64748b"
                  strokeWidth="1.5"
                />
                <text
                  x={ptLabel.x}
                  y={ptLabel.y + 3}
                  textAnchor="middle"
                  fill="#94a3b8"
                  fontSize="9"
                  fontFamily="monospace"
                  fontWeight="bold"
                >
                  {mbp} Mb
                </text>
              </g>
            );
          })}

          {/* 2 & 3. Forward & Reverse CDS Strands */}
          {bins.map((bin, i) => {
            const ptFwd = getPoint(i, rCdsFwd);
            const ptRev = getPoint(i, rCdsRev);
            return (
              <g key={i}>
                {bin.cds_fwd && (
                  <circle
                    cx={ptFwd.x}
                    cy={ptFwd.y}
                    r="2.2"
                    fill="#10b981"
                    opacity="0.85"
                  />
                )}
                {bin.cds_rev && (
                  <circle
                    cx={ptRev.x}
                    cy={ptRev.y}
                    r="2.2"
                    fill="#8b5cf6"
                    opacity="0.85"
                  />
                )}
              </g>
            );
          })}

          {/* 4. AMR Determinants Track */}
          {bins.map((bin, i) => {
            if (!bin.amr) return null;
            const pt = getPoint(i, rAmr);
            const color = getAmrColor(bin.amr.mechanism);
            return (
              <g
                key={`amr-${i}`}
                className="cursor-pointer transition-transform hover:scale-125"
                onMouseEnter={() => setHoveredBin(bin)}
                onMouseLeave={() => setHoveredBin(null)}
              >
                <circle cx={pt.x} cy={pt.y} r="5.5" fill={color} stroke="#0f172a" strokeWidth="1.5" />
                <circle cx={pt.x} cy={pt.y} r="8" fill="none" stroke={color} strokeWidth="1" strokeDasharray="2,2" opacity="0.7" />
              </g>
            );
          })}

          {/* 5. Virulence Factors Track */}
          {showVirulence &&
            bins.map((bin, i) => {
              if (!bin.virulence) return null;
              const pt = getPoint(i, rVir);
              return (
                <g
                  key={`vir-${i}`}
                  className="cursor-pointer"
                  onMouseEnter={() => setHoveredBin(bin)}
                  onMouseLeave={() => setHoveredBin(null)}
                >
                  <rect
                    x={pt.x - 4}
                    y={pt.y - 4}
                    width="8"
                    height="8"
                    fill="#eab308"
                    stroke="#0f172a"
                    strokeWidth="1.2"
                    transform={`rotate(${45}, ${pt.x}, ${pt.y})`}
                  />
                </g>
              );
            })}

          {/* 6. Mobile Genetic Elements (MGE) Track */}
          {showMGE &&
            bins.map((bin, i) => {
              if (!bin.mge) return null;
              const pt = getPoint(i, rMge);
              return (
                <g
                  key={`mge-${i}`}
                  className="cursor-pointer"
                  onMouseEnter={() => setHoveredBin(bin)}
                  onMouseLeave={() => setHoveredBin(null)}
                >
                  <circle cx={pt.x} cy={pt.y} r="4.2" fill="#f97316" stroke="#0f172a" strokeWidth="1" />
                </g>
              );
            })}

          {/* 7. BLAST Clade Comparison Rings (Concentric circular alignments) */}
          {showBlastRings && (
            <g>
              {[
                { r: rBlast1, cladeKey: 'clade_1_st258', color: '#10b981', label: 'Clade 1 (ST258)' },
                { r: rBlast2, cladeKey: 'clade_2_st11', color: '#f97316', label: 'Clade 2 (ST11 Ref)' },
                { r: rBlast3, cladeKey: 'clade_3_st147', color: '#ec4899', label: 'Clade 3 (ST147)' },
                { r: rBlast4, cladeKey: 'clade_4_st15', color: '#38bdf8', label: 'Clade 4 (ST15)' },
                { r: rBlast5, cladeKey: 'clade_5_st307', color: '#a855f7', label: 'Clade 5 (ST307)' },
              ].map((ring) => (
                <g key={ring.cladeKey}>
                  {/* Base Ring Guide */}
                  <circle cx={center} cy={center} r={ring.r} fill="none" stroke="#1e293b" strokeWidth="4.5" opacity="0.3" />
                  {/* Segment arcs showing BLAST identity matches */}
                  {bins.map((bin, i) => {
                    const idScore = (bin.blast_clades as any)?.[ring.cladeKey] || 100;
                    if (idScore < 75) return null; // Gap / deletion
                    const pt = getPoint(i, ring.r);
                    return (
                      <circle
                        key={i}
                        cx={pt.x}
                        cy={pt.y}
                        r="2.4"
                        fill={ring.color}
                        opacity={idScore > 95 ? 0.9 : 0.4}
                      />
                    );
                  })}
                </g>
              ))}
            </g>
          )}

          {/* 8. GC Content Baseline & Arc waveform */}
          <circle cx={center} cy={center} r={rGcContent} fill="none" stroke="#334155" strokeWidth="1" strokeDasharray="3,3" />
          {bins.map((bin, i) => {
            const dev = (bin.gc_content - 57.3) * 3.5;
            const ptBase = getPoint(i, rGcContent);
            const ptDev = getPoint(i, rGcContent + dev);
            return (
              <line
                key={`gc-${i}`}
                x1={ptBase.x}
                y1={ptBase.y}
                x2={ptDev.x}
                y2={ptDev.y}
                stroke="#64748b"
                strokeWidth="1.2"
                opacity="0.8"
              />
            );
          })}

          {/* 9. GC Skew (+ / -) Centerline & Spikes */}
          <circle cx={center} cy={center} r={rGcSkew} fill="none" stroke="#1e293b" strokeWidth="1.5" />
          {bins.map((bin, i) => {
            const skewOffset = bin.gc_skew * 130;
            const ptBase = getPoint(i, rGcSkew);
            const ptSkew = getPoint(i, rGcSkew + skewOffset);
            const isPos = bin.gc_skew >= 0;
            return (
              <line
                key={`skew-${i}`}
                x1={ptBase.x}
                y1={ptBase.y}
                x2={ptSkew.x}
                y2={ptSkew.y}
                stroke={isPos ? '#10b981' : '#e11d48'}
                strokeWidth="1.4"
                opacity="0.9"
              />
            );
          })}

          {/* Inner Core Label */}
          <circle cx={center} cy={center} r={rInnerHole} fill="#090d16" stroke="#1e293b" strokeWidth="2" />
          <text x={center} y={center - 14} textAnchor="middle" fill="#f8fafc" fontSize="13" fontFamily="sans-serif" fontWeight="bold">
            K. pneumoniae
          </text>
          <text x={center} y={center + 3} textAnchor="middle" fill="#94a3b8" fontSize="10" fontFamily="monospace">
            HS11286 / ST11
          </text>
          <text x={center} y={center + 18} textAnchor="middle" fill="#e11d48" fontSize="9" fontFamily="monospace" fontWeight="bold">
            MDR / CRKP
          </text>

          {/* 10. Callout pins with leader lines to Key Hotspots */}
          {(atlasData?.hotspots || []).map((hotspot) => {
            const binPt = getPoint(hotspot.bin_index, rContig);
            // Push callout pin further outward
            const calloutPt = getPoint(hotspot.bin_index, rContig + 45);
            const isSelected = selectedHotspot?.id === hotspot.id;

            return (
              <g
                key={hotspot.id}
                className="cursor-pointer"
                onClick={() => setSelectedHotspot(isSelected ? null : hotspot)}
              >
                {/* Leader line */}
                <line
                  x1={binPt.x}
                  y1={binPt.y}
                  x2={calloutPt.x}
                  y2={calloutPt.y}
                  stroke={isSelected ? '#e11d48' : '#f59e0b'}
                  strokeWidth={isSelected ? '2' : '1.2'}
                  strokeDasharray="2,2"
                />
                {/* Target hotspot node */}
                <circle
                  cx={calloutPt.x}
                  cy={calloutPt.y}
                  r={isSelected ? '6' : '4.5'}
                  fill={isSelected ? '#e11d48' : '#f59e0b'}
                  stroke="#020617"
                  strokeWidth="1.5"
                />
              </g>
            );
          })}
        </svg>

        {/* Hover / Active Isolate or Hotspot Overlay Card */}
        {(selectedHotspot || hoveredBin?.amr || hoveredBin?.virulence || hoveredBin?.mge) && (
          <div className="absolute bottom-2 left-2 right-2 sm:right-auto sm:max-w-xs bg-slate-950/95 backdrop-blur-md border border-slate-700/80 p-3 rounded-xl shadow-2xl text-xs font-mono space-y-1.5 pointer-events-auto">
            {selectedHotspot ? (
              <>
                <div className="flex justify-between items-center text-slate-200 font-bold border-b border-slate-800 pb-1">
                  <span className="text-crimson-400">{selectedHotspot.label}</span>
                  <span className="text-[10px] text-slate-400">{(selectedHotspot.position_bp / 1e6).toFixed(3)} Mb</span>
                </div>
                <div className="text-[11px] text-amber-300 font-semibold">{selectedHotspot.category}</div>
                <p className="text-[11px] text-slate-300 leading-relaxed font-sans">{selectedHotspot.description}</p>
                <button
                  onClick={() => setSelectedHotspot(null)}
                  className="text-[10px] text-slate-400 hover:text-white underline mt-1"
                >
                  Close Pin
                </button>
              </>
            ) : hoveredBin?.amr ? (
              <>
                <div className="text-crimson-400 font-bold flex justify-between">
                  <span>{hoveredBin.amr.name}</span>
                  <span className="text-slate-400 text-[10px]">{(hoveredBin.position / 1e6).toFixed(3)} Mb</span>
                </div>
                <div className="text-slate-300 text-[11px]">Mechanism: <strong className="text-amber-400">{hoveredBin.amr.mechanism}</strong></div>
                <div className="text-slate-400 text-[11px]">Class: {hoveredBin.amr.drug_class} ({hoveredBin.amr.type})</div>
              </>
            ) : hoveredBin?.virulence ? (
              <>
                <div className="text-emerald-400 font-bold flex justify-between">
                  <span>{hoveredBin.virulence.name}</span>
                  <span className="text-slate-400 text-[10px]">{(hoveredBin.position / 1e6).toFixed(3)} Mb</span>
                </div>
                <div className="text-slate-300 text-[11px]">Function: {hoveredBin.virulence.function}</div>
                <div className="text-slate-400 text-[11px]">Locus: {hoveredBin.virulence.locus}</div>
              </>
            ) : hoveredBin?.mge ? (
              <>
                <div className="text-amber-400 font-bold flex justify-between">
                  <span>{hoveredBin.mge.name}</span>
                  <span className="text-slate-400 text-[10px]">{(hoveredBin.position / 1e6).toFixed(3)} Mb</span>
                </div>
                <div className="text-slate-300 text-[11px]">Type: {hoveredBin.mge.type}</div>
              </>
            ) : null}
          </div>
        )}
      </div>

      {/* Legend Grid */}
      <div className="w-full bg-slate-950/80 border border-slate-800/80 rounded-xl p-3 text-xs font-mono grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shrink-0"></span>
          <span className="text-slate-300 truncate">CDS Forward (+)</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-purple-500 shrink-0"></span>
          <span className="text-slate-300 truncate">CDS Reverse (-)</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-crimson-500 shrink-0"></span>
          <span className="text-slate-300 truncate">AMR Determinants</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded bg-amber-500 shrink-0"></span>
          <span className="text-slate-300 truncate">Virulence (VF)</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-orange-500 shrink-0"></span>
          <span className="text-slate-300 truncate">MGE / Islands</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-sky-400 shrink-0"></span>
          <span className="text-slate-300 truncate">5 Clade BLAST</span>
        </div>
      </div>
    </div>
  );
};
