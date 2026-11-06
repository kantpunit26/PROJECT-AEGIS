import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { SEIRSimulationResult } from '../types';
import { TrendingUp, Sliders, Info, Play, RotateCcw } from 'lucide-react';

export const SEIRModelling: React.FC = () => {
  const [params, setParams] = useState({
    total_population: 1000.0,
    initial_susceptible: 990.0,
    initial_colonized: 8.0,
    initial_infected: 2.0,
    initial_recovered: 0.0,
    beta_transmission: 0.28,
    theta_carrier_infectivity: 0.35,
    alpha_progression: 0.08,
    gamma_colonized_clearance: 0.03,
    gamma_infection_clearance: 0.10,
    delta_treatment_exposure: 0.05,
    simulation_days: 120,
    time_step: 0.5,
  });

  const [simResult, setSimResult] = useState<SEIRSimulationResult | null>(null);
  const [loading, setLoading] = useState(false);

  const runSimulation = async () => {
    setLoading(true);
    try {
      const res = await api.simulateSEIR(params);
      setSimResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runSimulation();
  }, [params]);

  // SVG Chart Geometry
  const width = 720;
  const height = 300;
  const padding = 40;

  const getPoints = (arr: number[]) => {
    if (!arr || arr.length === 0) return '';
    const maxVal = params.total_population;
    return arr
      .map((val, idx) => {
        const x = padding + (idx / (arr.length - 1)) * (width - 2 * padding);
        const y = height - padding - (val / maxVal) * (height - 2 * padding);
        return `${x},${y}`;
      })
      .join(' ');
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div>
          <h1 className="text-xl font-bold text-white tracking-wide">Hospital Transmission & Colonization Dynamics</h1>
          <p className="text-xs text-slate-400">
            Deterministic Runge-Kutta numerical differential equation solver for bacterial colonization (C) and infection (I)
          </p>
        </div>

        <button
          onClick={() =>
            setParams({
              total_population: 1000.0,
              initial_susceptible: 990.0,
              initial_colonized: 8.0,
              initial_infected: 2.0,
              initial_recovered: 0.0,
              beta_transmission: 0.28,
              theta_carrier_infectivity: 0.35,
              alpha_progression: 0.08,
              gamma_colonized_clearance: 0.03,
              gamma_infection_clearance: 0.10,
              delta_treatment_exposure: 0.05,
              simulation_days: 120,
              time_step: 0.5,
            })
          }
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-mono transition-all border border-slate-700"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Reset Parameters</span>
        </button>
      </div>

      {/* Model Scientific Disclaimer */}
      <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-lg flex items-start space-x-2 text-xs text-slate-400 font-sans">
        <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
        <p>
          <strong className="text-slate-200">Mathematical Specification:</strong> This compartmental model explicitly partitions subclinical asymptomatic carriage ($C$) from active clinical infection ($I$). Model parameters reflect hospital epidemiological transmission literature, not genomic sequence metrics.
        </p>
      </div>

      {/* Simulation Results Header */}
      {simResult && (
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
            <div className="text-xs font-mono uppercase text-slate-400">Basic Reproduction Number (R0)</div>
            <div className={`text-2xl font-bold font-mono ${simResult.r0 > 1.0 ? 'text-crimson-400' : 'text-emerald-400'}`}>
              {simResult.r0}
            </div>
            <div className="text-[11px] text-slate-400">
              {simResult.r0 > 1.0 ? 'Epidemic expansion potential' : 'Self-limiting subcritical transmission'}
            </div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
            <div className="text-xs font-mono uppercase text-slate-400">Peak Clinical Infection</div>
            <div className="text-2xl font-bold font-mono text-white">{simResult.peak_infected_count} cases</div>
            <div className="text-[11px] text-slate-400">Projected peak on Day {simResult.peak_day}</div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
            <div className="text-xs font-mono uppercase text-slate-400">Cumulative Colonization</div>
            <div className="text-2xl font-bold font-mono text-amber-400">
              {simResult.total_colonization_incidence}
            </div>
            <div className="text-[11px] text-slate-400">Asymptomatically colonized carriers</div>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1">
            <div className="text-xs font-mono uppercase text-slate-400">Effective Re (Day 120)</div>
            <div className="text-2xl font-bold font-mono text-blue-400">
              {simResult.effective_re[simResult.effective_re.length - 1]}
            </div>
            <div className="text-[11px] text-slate-400">Depleted susceptible equilibrium</div>
          </div>
        </div>
      )}

      {/* SVG Time-Series Trajectory Plot */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-sm font-semibold text-white">Transmission Compartment Trajectories</h3>
            <p className="text-xs text-slate-400">Temporal population projection over {params.simulation_days} days</p>
          </div>

          <div className="flex items-center space-x-4 text-xs font-mono">
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-1 bg-slate-400 inline-block"></span>
              <span className="text-slate-300">Susceptible (S)</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-1 bg-amber-500 inline-block"></span>
              <span className="text-amber-400">Colonized (C)</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-1 bg-crimson-500 inline-block"></span>
              <span className="text-crimson-400">Infected (I)</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-3 h-1 bg-emerald-500 inline-block"></span>
              <span className="text-emerald-400">Recovered (R)</span>
            </div>
          </div>
        </div>

        {simResult && (
          <div className="w-full overflow-x-auto flex justify-center">
            <svg width={width} height={height} className="select-none font-mono text-[10px]">
              {/* Axes */}
              <line
                x1={padding}
                y1={height - padding}
                x2={width - padding}
                y2={height - padding}
                stroke="#334155"
                strokeWidth="1.5"
              />
              <line
                x1={padding}
                y1={padding}
                x2={padding}
                y2={height - padding}
                stroke="#334155"
                strokeWidth="1.5"
              />

              {/* Gridlines */}
              {[0.25, 0.5, 0.75].map((pct) => (
                <line
                  key={pct}
                  x1={padding}
                  y1={height - padding - pct * (height - 2 * padding)}
                  x2={width - padding}
                  y2={height - padding - pct * (height - 2 * padding)}
                  stroke="#1E293B"
                  strokeDasharray="3,3"
                />
              ))}

              {/* Trajectory Polylines */}
              <polyline
                fill="none"
                stroke="#94A3B8"
                strokeWidth="2"
                points={getPoints(simResult.susceptible)}
              />
              <polyline
                fill="none"
                stroke="#F59E0B"
                strokeWidth="2.5"
                points={getPoints(simResult.colonized)}
              />
              <polyline
                fill="none"
                stroke="#EF4444"
                strokeWidth="2.5"
                points={getPoints(simResult.infected)}
              />
              <polyline
                fill="none"
                stroke="#10B981"
                strokeWidth="2"
                points={getPoints(simResult.recovered)}
              />

              {/* X and Y labels */}
              <text x={width - padding} y={height - padding + 20} textAnchor="end" fill="#64748B">
                Day {params.simulation_days}
              </text>
              <text x={padding} y={height - padding + 20} textAnchor="start" fill="#64748B">
                Day 0
              </text>
              <text x={padding - 10} y={padding + 5} textAnchor="end" fill="#64748B">
                N={params.total_population}
              </text>
            </svg>
          </div>
        )}
      </div>

      {/* Parameter Sliders Control Panel */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex items-center space-x-2">
          <Sliders className="w-4 h-4 text-crimson-400" />
          <h3 className="text-sm font-semibold text-white">Dynamic Epidemiological Parameters</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono text-xs">
          {/* Transmission beta */}
          <div className="space-y-1.5">
            <div className="flex justify-between">
              <span className="text-slate-400">Transmission Rate (&beta;):</span>
              <span className="text-white font-bold">{params.beta_transmission}</span>
            </div>
            <input
              type="range"
              min="0.05"
              max="0.80"
              step="0.01"
              value={params.beta_transmission}
              onChange={(e) => setParams({ ...params, beta_transmission: Number(e.target.value) })}
              className="w-full accent-crimson-600 cursor-pointer"
            />
          </div>

          {/* Carrier infectivity theta */}
          <div className="space-y-1.5">
            <div className="flex justify-between">
              <span className="text-slate-400">Carrier Relative Infectivity (&theta;):</span>
              <span className="text-white font-bold">{params.theta_carrier_infectivity}</span>
            </div>
            <input
              type="range"
              min="0.10"
              max="1.00"
              step="0.05"
              value={params.theta_carrier_infectivity}
              onChange={(e) => setParams({ ...params, theta_carrier_infectivity: Number(e.target.value) })}
              className="w-full accent-crimson-600 cursor-pointer"
            />
          </div>

          {/* Progression alpha */}
          <div className="space-y-1.5">
            <div className="flex justify-between">
              <span className="text-slate-400">Infection Progression Rate (&alpha;):</span>
              <span className="text-white font-bold">{params.alpha_progression}</span>
            </div>
            <input
              type="range"
              min="0.01"
              max="0.30"
              step="0.01"
              value={params.alpha_progression}
              onChange={(e) => setParams({ ...params, alpha_progression: Number(e.target.value) })}
              className="w-full accent-crimson-600 cursor-pointer"
            />
          </div>

          {/* Clearance gamma_c */}
          <div className="space-y-1.5">
            <div className="flex justify-between">
              <span className="text-slate-400">Decolonization Rate (&gamma;c):</span>
              <span className="text-white font-bold">{params.gamma_colonized_clearance}</span>
            </div>
            <input
              type="range"
              min="0.01"
              max="0.20"
              step="0.01"
              value={params.gamma_colonized_clearance}
              onChange={(e) => setParams({ ...params, gamma_colonized_clearance: Number(e.target.value) })}
              className="w-full accent-crimson-600 cursor-pointer"
            />
          </div>

          {/* Treatment exposure delta */}
          <div className="space-y-1.5">
            <div className="flex justify-between">
              <span className="text-slate-400">Antibiotic De-escalation (&delta;):</span>
              <span className="text-white font-bold">{params.delta_treatment_exposure}</span>
            </div>
            <input
              type="range"
              min="0.01"
              max="0.30"
              step="0.01"
              value={params.delta_treatment_exposure}
              onChange={(e) => setParams({ ...params, delta_treatment_exposure: Number(e.target.value) })}
              className="w-full accent-crimson-600 cursor-pointer"
            />
          </div>

          {/* Simulation duration */}
          <div className="space-y-1.5">
            <div className="flex justify-between">
              <span className="text-slate-400">Simulation Horizon:</span>
              <span className="text-white font-bold">{params.simulation_days} Days</span>
            </div>
            <input
              type="range"
              min="30"
              max="365"
              step="5"
              value={params.simulation_days}
              onChange={(e) => setParams({ ...params, simulation_days: Number(e.target.value) })}
              className="w-full accent-crimson-600 cursor-pointer"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
