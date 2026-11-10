import React, { useState } from 'react';
import { BayesianSkylineData, SkylineClade } from '../../types';
import { TrendingUp, Activity, Layers, Info } from 'lucide-react';

interface BayesianSkylinePlotProps {
  data: BayesianSkylineData;
}

export const BayesianSkylinePlot: React.FC<BayesianSkylinePlotProps> = ({ data }) => {
  const [selectedClade, setSelectedClade] = useState<string | null>(null);

  const { clades, y_axis_label, x_axis_label } = data;

  // Render individual clade plot
  const renderCladeCard = (clade: SkylineClade) => {
    const width = 360;
    const height = 180;
    const padX = 45;
    const padY = 25;
    const plotW = width - padX - 15;
    const plotH = height - padY - 25;

    // Log10 scale for Ne (min: 0.1, max: 1000)
    const minLog = -1; // 10^-1 = 0.1
    const maxLog = 3;  // 10^3 = 1000

    const minYear = Math.min(...clade.years);
    const maxYear = Math.max(...clade.years);

    const getX = (year: number) => {
      const ratio = (year - minYear) / Math.max(1, maxYear - minYear);
      return padX + ratio * plotW;
    };

    const getY = (val: number) => {
      const logVal = Math.log10(Math.max(0.05, val));
      const ratio = (logVal - minLog) / (maxLog - minLog);
      return height - padY - ratio * plotH;
    };

    // Construct polygon for 95% HPD envelope
    const upperPoints = clade.years.map((y, i) => `${getX(y)},${getY(clade.upper_hpd[i])}`).join(' ');
    const lowerPoints = clade.years
      .slice()
      .reverse()
      .map((y, i) => {
        const origIdx = clade.years.length - 1 - i;
        return `${getX(y)},${getY(clade.lower_hpd[origIdx])}`;
      })
      .join(' ');
    const polygonPoints = `${upperPoints} ${lowerPoints}`;

    // Median line path
    const medianPath = clade.years
      .map((y, i) => `${i === 0 ? 'M' : 'L'} ${getX(y)} ${getY(clade.median_ne[i])}`)
      .join(' ');

    return (
      <div
        key={clade.clade_id}
        className="bg-slate-950/80 border border-slate-800 rounded-xl p-3.5 space-y-2 hover:border-slate-700 transition-all flex flex-col justify-between"
      >
        <div className="flex justify-between items-center border-b border-slate-800/80 pb-1.5">
          <span className="font-bold text-xs text-white" style={{ color: clade.color }}>
            {clade.name}
          </span>
          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-900 border border-slate-700 text-slate-300">
            Peak: {clade.peak_year}
          </span>
        </div>

        {/* Clade Mini Chart SVG */}
        <div className="w-full flex justify-center">
          <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto select-none">
            {/* Grid Lines */}
            {[-1, 0, 1, 2, 3].map((logExp) => {
              const yVal = Math.pow(10, logExp);
              const yPos = getY(yVal);
              return (
                <g key={logExp}>
                  <line x1={padX} y1={yPos} x2={width - 15} y2={yPos} stroke="#1e293b" strokeWidth="1" strokeDasharray="2,2" />
                  <text x={padX - 6} y={yPos + 3.5} textAnchor="end" fill="#64748b" fontSize="8" fontFamily="monospace">
                    {yVal >= 1 ? yVal : '0.1'}
                  </text>
                </g>
              );
            })}

            {/* X-axis year ticks */}
            {clade.years.filter((_, idx) => idx % 2 === 0).map((year) => (
              <text
                key={year}
                x={getX(year)}
                y={height - 8}
                textAnchor="middle"
                fill="#64748b"
                fontSize="8.5"
                fontFamily="monospace"
              >
                {year}
              </text>
            ))}

            {/* Shaded 95% HPD Demographic Envelope */}
            <polygon points={polygonPoints} fill={clade.color} fillOpacity="0.25" />

            {/* Median Effective Population Size (Ne * tau) trajectory curve */}
            <path d={medianPath} fill="none" stroke={clade.color} strokeWidth="2.5" strokeLinecap="round" />

            {/* Data points */}
            {clade.years.map((y, i) => (
              <circle
                key={y}
                cx={getX(y)}
                cy={getY(clade.median_ne[i])}
                r="3"
                fill="#020617"
                stroke={clade.color}
                strokeWidth="1.8"
              />
            ))}
          </svg>
        </div>

        <p className="text-[10px] text-slate-400 font-sans leading-relaxed pt-1">
          {clade.notes}
        </p>
      </div>
    );
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4 shadow-2xl">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-slate-800 pb-3">
        <div>
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-4 h-4 text-crimson-400" />
            <h3 className="text-sm sm:text-base font-bold text-white tracking-wide">
              {data.title || 'Bayesian Skyline Demographic Plots (BSP)'}
            </h3>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            Log-scale Effective Population Size ($N_e \times \tau$) trajectories reconstruct epidemic clone expansion
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono text-slate-400">
          <Info className="w-3.5 h-3.5 text-blue-400" />
          <span>Shaded bands = 95% Bayesian Credible Envelope</span>
        </div>
      </div>

      {/* Grid of Clade Skyline Plots */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {clades.map((clade) => renderCladeCard(clade))}
      </div>
    </div>
  );
};

