import React, { useState, useEffect } from 'react';
import {
  Radio,
  Activity,
  AlertTriangle,
  Clock,
  ShieldAlert,
  Send,
  CheckCircle2,
  TrendingUp,
  MapPin,
  Waves,
  RefreshCw,
  Share2
} from 'lucide-react';
import { api } from '../services/api';
import {
  WastewaterSite,
  WBELeadTimeResponse,
  OneHealthMatrix,
  AlertSimulationResult
} from '../types';

export const OneHealth: React.FC = () => {
  const [sites, setSites] = useState<WastewaterSite[]>([]);
  const [leadTimeData, setLeadTimeData] = useState<WBELeadTimeResponse | null>(null);
  const [nexusMatrix, setNexusMatrix] = useState<OneHealthMatrix | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Simulation State
  const [simSite, setSimSite] = useState('WWTP-METRO-01');
  const [simPathogen, setSimPathogen] = useState('Klebsiella pneumoniae');
  const [simGene, setSimGene] = useState('blaNDM-5');
  const [simLoad, setSimLoad] = useState(7.4);
  const [simResult, setSimResult] = useState<AlertSimulationResult | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [s, lt, nx] = await Promise.all([
        api.getWastewaterSites(),
        api.getWBELeadTime(45),
        api.getOneHealthNexus()
      ]);
      setSites(s);
      setLeadTimeData(lt);
      setNexusMatrix(nx);
    } catch (err) {
      console.error('Failed to load One Health data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSimulateAlert = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSimulating(true);
    try {
      const res = await api.simulateAlert({
        site_id: simSite,
        pathogen: simPathogen,
        resistance_gene: simGene,
        log10_load: Number(simLoad)
      });
      setSimResult(res);
    } catch (err) {
      console.error('Failed to simulate alert dispatch:', err);
    } finally {
      setIsSimulating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="p-6 rounded-xl bg-gradient-to-r from-slate-900 via-slate-900/95 to-slate-950 border border-slate-800 shadow-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-cyan-950 text-cyan-400 border border-cyan-800/60 uppercase">
                One Health Environmental Nexus
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800/60">
                12-Day Clinical Lead Time
              </span>
            </div>
            <h1 className="text-2xl font-bold text-white mt-2 flex items-center space-x-2">
              <Waves className="w-6 h-6 text-cyan-400" />
              <span>Wastewater Metagenomics & Early Warning Lead-Time Engine</span>
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-3xl">
              Track sewage catchment AMR gene load to preempt clinical ICU surges 10–14 days in advance, mapping cross-compartment plasmid diffusion across environmental, animal, and clinical reservoirs.
            </p>
          </div>

          <button
            onClick={loadData}
            disabled={isLoading}
            className="flex items-center space-x-2 px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold border border-slate-700 transition-all"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Sync WBE Feeds</span>
          </button>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow-md">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
            <span>Forecast Lead Time</span>
            <Clock className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">12 Days</div>
          <p className="text-[10px] text-emerald-400 mt-1 font-mono">Mean early detection window</p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow-md">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
            <span>Catchment Population</span>
            <MapPin className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">2.68M</div>
          <p className="text-[10px] text-slate-400 mt-1 font-mono">Covered across 4 WWTP zones</p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow-md">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
            <span>Correlation (Pearson r)</span>
            <TrendingUp className="w-4 h-4 text-crimson-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">r = 0.89</div>
          <p className="text-[10px] text-emerald-400 mt-1 font-mono">p &lt; 0.0001 (High Significance)</p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 shadow-md">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
            <span>One Health Reservoirs</span>
            <Share2 className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">3 Nexus</div>
          <p className="text-[10px] text-purple-300 mt-1 font-mono">Clinical • Agri • Wastewater</p>
        </div>
      </div>

      {/* Paired Lead-Time Timeseries Visualization */}
      <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-md space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-2">
          <div>
            <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              <span>Paired Lead-Time Wave: Wastewater AMR Copies vs. Clinical Hospital Admissions</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Notice how the sewage metagenomic peak (cyan bars) surges ~12 days before the clinical inpatient admission wave (crimson line).
            </p>
          </div>
          <div className="flex items-center space-x-4 text-xs font-mono">
            <span className="flex items-center space-x-1.5 text-cyan-400">
              <span className="w-3 h-3 bg-cyan-500 rounded-sm"></span>
              <span>Wastewater (log10 copies/L)</span>
            </span>
            <span className="flex items-center space-x-1.5 text-crimson-400">
              <span className="w-3 h-1 bg-crimson-500 rounded"></span>
              <span>Clinical Admissions</span>
            </span>
          </div>
        </div>

        {/* Custom Interactive SVG Graph */}
        {leadTimeData?.data ? (
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80 overflow-x-auto">
            <div className="min-w-[700px] h-56 flex items-end space-x-2 relative pt-6 pb-2">
              {/* Threshold indicator line */}
              <div className="absolute top-12 left-0 right-0 border-b border-dashed border-amber-500/60 z-0">
                <span className="absolute -top-4 right-2 text-[10px] font-mono text-amber-400">
                  Early Warning Trigger Threshold (6.0 log10)
                </span>
              </div>

              {leadTimeData.data.map((point, idx) => {
                const barHeight = Math.max(10, ((point.wastewater_amr_log10 - 3.5) / 5.0) * 160);
                const clinHeight = Math.max(4, (point.clinical_admissions / 35.0) * 160);
                const isSurge = point.surge_predicted;

                return (
                  <div key={idx} className="flex-1 flex flex-col items-center group relative h-full justify-end">
                    {/* Hover tooltip */}
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity absolute -top-16 z-20 bg-slate-900 border border-slate-700 px-2 py-1 rounded text-[10px] font-mono text-white pointer-events-none whitespace-nowrap shadow-xl">
                      <div>Date: {point.date}</div>
                      <div className="text-cyan-300">Sewage: {point.wastewater_amr_log10} log10</div>
                      <div className="text-crimson-300">Clinical: {point.clinical_admissions} pts</div>
                    </div>

                    {/* Clinical line point */}
                    <div
                      className="absolute z-10 w-2 h-2 rounded-full bg-crimson-500 border border-crimson-200"
                      style={{ bottom: `${clinHeight}px` }}
                    />

                    {/* Wastewater Bar */}
                    <div
                      className={`w-full rounded-t transition-all ${
                        isSurge
                          ? 'bg-gradient-to-t from-cyan-900/60 to-cyan-400'
                          : 'bg-gradient-to-t from-slate-800 to-slate-700'
                      }`}
                      style={{ height: `${barHeight}px` }}
                    />

                    {/* Day index every 5 days */}
                    {idx % 5 === 0 && (
                      <span className="text-[9px] font-mono text-slate-500 mt-1 truncate">
                        d{idx}
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
            <div className="text-center text-[11px] font-mono text-slate-400 mt-2">
              Timeline: 45 Days Continuous Genomic Catchment Sampling (Daily Automated Metagenomics)
            </div>
          </div>
        ) : null}
      </div>

      {/* Grid: Wastewater Sites & Outbreak Dispatch Simulator */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Monitoring Sites Table (7 Cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-md">
            <h2 className="text-sm font-semibold text-white mb-3 flex items-center space-x-2">
              <Radio className="w-4 h-4 text-cyan-400" />
              <span>Active Wastewater & Environmental Surveillance Catchments</span>
            </h2>

            <div className="space-y-3">
              {sites.map((site) => {
                const isCritical = site.alert_level === 'CRITICAL';
                const isWarning = site.alert_level === 'WARNING';
                return (
                  <div
                    key={site.site_id}
                    className="p-3.5 rounded-lg bg-slate-950 border border-slate-800/90 hover:border-slate-700 transition-all"
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold text-xs text-white">{site.name}</span>
                        <span className="text-[10px] font-mono text-slate-500">[{site.site_id}]</span>
                      </div>
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase ${
                          isCritical
                            ? 'bg-crimson-950 text-crimson-400 border border-crimson-800'
                            : isWarning
                            ? 'bg-amber-950 text-amber-400 border border-amber-800'
                            : 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                        }`}
                      >
                        {site.alert_level}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px] font-mono text-slate-400 my-2">
                      <div>
                        <span className="text-slate-500 block text-[10px]">Population:</span>
                        <span className="text-slate-200">{site.population_served.toLocaleString()}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px]">Daily Flow:</span>
                        <span className="text-slate-200">{site.flow_rate_m3_day.toLocaleString()} m³/d</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px]">AMR Load:</span>
                        <span className="text-cyan-300 font-bold">{site.log10_amr_copies_per_liter} log10</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px]">Advance Window:</span>
                        <span className="text-emerald-400 font-bold">+{site.lead_time_days} days</span>
                      </div>
                    </div>

                    <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px]">
                      <span className="text-slate-400">
                        Marker: <span className="text-crimson-300 font-mono">{site.dominant_determinant}</span>
                      </span>
                      <span className="text-slate-500 italic text-[10px]">
                        Target: {site.target_organism}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* One Health Nexus Matrix */}
          {nexusMatrix && (
            <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-md">
              <h2 className="text-sm font-semibold text-white mb-3 flex items-center space-x-2">
                <Share2 className="w-4 h-4 text-purple-400" />
                <span>One Health Cross-Compartment Plasmid & Determinant Sharing</span>
              </h2>

              <div className="space-y-2">
                {nexusMatrix.shared_mge_interchanges.map((inter, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-lg bg-slate-950 border border-slate-800/80 text-xs flex items-center justify-between"
                  >
                    <div className="space-y-0.5">
                      <div className="flex items-center space-x-2">
                        <span className="text-purple-300 font-mono font-semibold">{inter.element}</span>
                        <span className="text-[10px] text-slate-500">
                          ({inter.shared_snp_distance} core SNPs diff)
                        </span>
                      </div>
                      <div className="text-[11px] text-slate-400">
                        <span>{inter.source}</span>
                        <span className="text-slate-500 mx-1.5">➔</span>
                        <span>{inter.target}</span>
                      </div>
                    </div>

                    <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-800/50 px-2 py-0.5 rounded">
                      {inter.confidence}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right: Outbreak Alert Dispatch Simulator (5 Cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-md">
            <div className="flex items-center space-x-2 mb-3">
              <ShieldAlert className="w-5 h-5 text-crimson-500" />
              <div>
                <h2 className="text-sm font-semibold text-white">Outbreak Alert Dispatch Simulator</h2>
                <p className="text-[11px] text-slate-400">
                  Simulate multi-channel early warning broadcast to hospital IPC & public health command
                </p>
              </div>
            </div>

            <form onSubmit={handleSimulateAlert} className="space-y-3">
              <div>
                <label className="text-[11px] font-mono text-slate-400 block mb-1">Catchment Site:</label>
                <select
                  value={simSite}
                  onChange={(e) => setSimSite(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-crimson-600"
                >
                  {sites.map((s) => (
                    <option key={s.site_id} value={s.site_id}>
                      {s.name} ({s.site_id})
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[11px] font-mono text-slate-400 block mb-1">Pathogen:</label>
                  <input
                    type="text"
                    value={simPathogen}
                    onChange={(e) => setSimPathogen(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 font-mono"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-mono text-slate-400 block mb-1">Emergent Gene:</label>
                  <input
                    type="text"
                    value={simGene}
                    onChange={(e) => setSimGene(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 font-mono"
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-[11px] font-mono text-slate-400 mb-1">
                  <span>Detected Load:</span>
                  <span className="text-cyan-300 font-bold">{simLoad} log10 copies/L</span>
                </div>
                <input
                  type="range"
                  min="4.0"
                  max="9.0"
                  step="0.1"
                  value={simLoad}
                  onChange={(e) => setSimLoad(parseFloat(e.target.value))}
                  className="w-full accent-crimson-500"
                />
              </div>

              <button
                type="submit"
                disabled={isSimulating}
                className="w-full flex items-center justify-center space-x-2 py-2.5 bg-crimson-600 hover:bg-crimson-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-crimson-950 transition-all disabled:opacity-50"
              >
                {isSimulating ? (
                  <RefreshCw className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
                <span>Dispatch Outbreak Broadcast</span>
              </button>
            </form>

            {/* Simulation Result */}
            {simResult && (
              <div className="mt-4 p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
                <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                  <span className="text-xs font-mono font-bold text-emerald-400 flex items-center space-x-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>BROADCAST DELIVERED</span>
                  </span>
                  <span className="text-[10px] font-mono text-slate-500">{simResult.dispatch_id}</span>
                </div>

                <div className="space-y-1 text-xs">
                  <p className="text-slate-300">
                    <span className="text-slate-500 font-mono">Forecasted Lead Time:</span>{' '}
                    <span className="text-emerald-400 font-bold font-mono">
                      {simResult.alert.forecasted_lead_time_days} Days Advance Warning
                    </span>
                  </p>
                  <p className="text-slate-300">
                    <span className="text-slate-500 font-mono">Action:</span>{' '}
                    {simResult.alert.recommended_action}
                  </p>
                </div>

                {/* Channels Latency */}
                <div className="pt-2 border-t border-slate-800/80">
                  <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider block mb-1.5">
                    Broadcast Delivery Gateways:
                  </span>
                  <div className="space-y-1">
                    {simResult.channels.map((ch, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between text-[11px] font-mono text-slate-300 bg-slate-900/60 px-2 py-1 rounded"
                      >
                        <span>{ch.channel}</span>
                        <span className="text-emerald-400">{ch.latency_ms} ms</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
