import React, { useState } from 'react';

interface CircularCoord {
  position: number;
  gc_content: number;
  gc_skew: number;
  features: { name: string; type: string }[];
}

interface CircularGenomeViewerProps {
  coordinates: CircularCoord[];
  genomeSize?: number;
}

export const CircularGenomeViewer: React.FC<CircularGenomeViewerProps> = ({
  coordinates,
  genomeSize = 5333942,
}) => {
  const [selectedFeature, setSelectedFeature] = useState<string | null>(null);

  const size = 420;
  const center = size / 2;
  const outerRadius = 160;
  const gcRadius = 135;
  const skewRadius = 105;

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4 flex flex-col items-center">
      <div className="w-full flex justify-between items-center">
        <div>
          <h3 className="text-sm font-semibold text-white">Circular Chromosome GC Skew & Content</h3>
          <p className="text-xs text-slate-400">
            Total length: {(genomeSize / 1e6).toFixed(2)} Mb | GC Mean: 57.3%
          </p>
        </div>
        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="flex items-center space-x-1">
            <span className="w-2.5 h-2.5 rounded bg-emerald-500 inline-block"></span>
            <span className="text-slate-300">GC Skew (+)</span>
          </div>
          <div className="flex items-center space-x-1">
            <span className="w-2.5 h-2.5 rounded bg-crimson-500 inline-block"></span>
            <span className="text-slate-300">GC Skew (-)</span>
          </div>
        </div>
      </div>

      <div className="relative">
        <svg width={size} height={size} className="overflow-visible select-none">
          {/* Base Backbone Outer Ring */}
          <circle
            cx={center}
            cy={center}
            r={outerRadius}
            fill="none"
            stroke="#1E293B"
            strokeWidth="8"
          />

          {/* GC Baseline circle */}
          <circle
            cx={center}
            cy={center}
            r={gcRadius}
            fill="none"
            stroke="#0F172A"
            strokeWidth="16"
          />

          {/* GC Skew Centerline */}
          <circle
            cx={center}
            cy={center}
            r={skewRadius}
            fill="none"
            stroke="#1E293B"
            strokeWidth="1"
            strokeDasharray="2,2"
          />

          {/* Render GC Content and Skew Segments */}
          {coordinates.map((coord, idx) => {
            const angle = (idx / coordinates.length) * 2 * Math.PI - Math.PI / 2;
            const xOuter = center + outerRadius * Math.cos(angle);
            const yOuter = center + outerRadius * Math.sin(angle);

            // GC skew offset from centerline
            const skewOffset = coord.gc_skew * 120;
            const rSkew = skewRadius + skewOffset;
            const xSkew = center + rSkew * Math.cos(angle);
            const ySkew = center + rSkew * Math.sin(angle);

            const isPositiveSkew = coord.gc_skew >= 0;

            return (
              <g key={coord.position}>
                {/* GC Skew Spike */}
                <line
                  x1={center + skewRadius * Math.cos(angle)}
                  y1={center + skewRadius * Math.sin(angle)}
                  x2={xSkew}
                  y2={ySkew}
                  stroke={isPositiveSkew ? '#10B981' : '#EF4444'}
                  strokeWidth="2"
                  opacity="0.8"
                />

                {/* Pathogenicity / rRNA Operon Feature Annotations */}
                {coord.features && coord.features.length > 0 && (
                  <circle
                    cx={xOuter}
                    cy={yOuter}
                    r="4"
                    fill="#F59E0B"
                    className="cursor-pointer hover:scale-150 transition-all"
                    onClick={() => setSelectedFeature(`${coord.features[0].name} @ bp ${coord.position.toLocaleString()}`)}
                  />
                )}
              </g>
            );
          })}

          {/* Center Info Display */}
          <text
            x={center}
            y={center - 10}
            textAnchor="middle"
            className="fill-white font-mono font-bold text-sm"
          >
            K. pneumoniae
          </text>
          <text
            x={center}
            y={center + 12}
            textAnchor="middle"
            className="fill-slate-400 font-mono text-[11px]"
          >
            {(genomeSize / 1e6).toFixed(3)} Mbp
          </text>
        </svg>
      </div>

      {selectedFeature && (
        <div className="bg-slate-800 border border-amber-600/60 text-amber-300 text-xs px-3 py-1.5 rounded font-mono">
          Selected Locus: {selectedFeature}
        </div>
      )}
    </div>
  );
};

