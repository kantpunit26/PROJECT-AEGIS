import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Isolate, SpatialCluster, SurveillanceAlert } from '../types';
import { SurveillanceGlobe } from '../components/globe/SurveillanceGlobe';
import { ShieldAlert, Dna, Activity, AlertTriangle, Layers, ArrowUpRight } from 'lucide-react';

interface DashboardProps {
  onNavigate: (tab: any) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ onNavigate }) => {
  const [isolates, setIsolates] = useState<Isolate[]>([]);
  const [clusters, setClusters] = useState<SpatialCluster[]>([]);
  const [alerts, setAlerts] = useState<SurveillanceAlert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [isoData, clusterData, alertData] = await Promise.all([
          api.getIsolates(),
          api.getSpatialClusters(),
          api.getAlerts(),
        ]);
        setIsolates(isoData);
        setClusters(clusterData);
        setAlerts(alertData);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const totalCarbapenemases = isolates.reduce((acc, curr) => acc + (curr.amr_count || 0), 0);
  const activeAlerts = alerts.filter((a) => !a.acknowledged);

  return (
    <div className="space-y-4 sm:space-y-6 w-full">
      {/* Top Banner Alert if active outbreak exists */}
      {activeAlerts.length > 0 && (
        <div className="bg-crimson-950/80 border border-crimson-700/80 p-3.5 sm:p-4 rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-lg shadow-crimson-950/30">
          <div className="flex items-start space-x-3 w-full">
            <div className="p-2 bg-crimson-900/60 rounded-lg text-crimson-400 mt-0.5 shrink-0">
              <ShieldAlert className="w-5 h-5 animate-pulse" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
                <span className="font-bold text-white text-xs sm:text-sm">{activeAlerts[0].title}</span>
                <span className="px-2 py-0.5 rounded text-[9px] sm:text-[10px] font-mono bg-crimson-900 text-crimson-300 font-bold uppercase">
                  {activeAlerts[0].severity}
                </span>
              </div>
              <p className="text-[11px] sm:text-xs text-slate-300 mt-1 max-w-3xl leading-relaxed">
                {activeAlerts[0].message}
              </p>
            </div>
          </div>
          <button
            onClick={() => onNavigate('comparative')}
            className="w-full sm:w-auto flex items-center justify-center space-x-1.5 bg-crimson-800 hover:bg-crimson-700 text-white text-xs px-3.5 py-2 rounded-lg font-mono transition-all shrink-0 sm:ml-4"
          >
            <span>Inspect SNPs</span>
            <ArrowUpRight className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Key Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1.5">
          <div className="flex justify-between items-center text-slate-400">
            <span className="text-xs font-mono uppercase tracking-wider">Surveillance Registry</span>
            <Dna className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">{isolates.length}</div>
          <div className="text-[11px] text-slate-400">Genomes fully QC verified (N50 &ge; 30kb)</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1.5">
          <div className="flex justify-between items-center text-slate-400">
            <span className="text-xs font-mono uppercase tracking-wider">Carbapenem Resistance</span>
            <Activity className="w-4 h-4 text-crimson-500" />
          </div>
          <div className="text-2xl font-bold font-mono text-crimson-400">75.0%</div>
          <div className="text-[11px] text-slate-400">blaNDM, blaKPC, and blaOXA-48-like</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1.5">
          <div className="flex justify-between items-center text-slate-400">
            <span className="text-xs font-mono uppercase tracking-wider">High-Risk Lineages</span>
            <Layers className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-xl sm:text-2xl font-bold font-mono text-white">ST11 / ST147</div>
          <div className="text-[11px] text-slate-400">Predominant global pandemic clones</div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl space-y-1.5">
          <div className="flex justify-between items-center text-slate-400">
            <span className="text-xs font-mono uppercase tracking-wider">Active Outbreak Clusters</span>
            <AlertTriangle className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold font-mono text-amber-400">1 Cluster</div>
          <div className="text-[11px] text-slate-400">6 SNPs distance in Vadodara, Gujarat</div>
        </div>
      </div>

      {/* 3D Global Surveillance Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        <div className="lg:col-span-2 space-y-3">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-1 sm:gap-0">
            <div>
              <h2 className="text-sm sm:text-base font-bold text-white">Global Pathogen Distribution & Provenance</h2>
              <p className="text-[11px] sm:text-xs text-slate-400">Interactive 3D Three.js surveillance sphere</p>
            </div>
            <button
              onClick={() => onNavigate('surveillance')}
              className="text-xs font-mono text-crimson-400 hover:text-crimson-300 flex items-center space-x-1 self-end sm:self-auto"
            >
              <span>Open Spatial Explorer</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>
          <div className="h-[320px] sm:h-[420px] lg:h-[480px] w-full rounded-xl overflow-hidden border border-slate-800 bg-slate-950/60">
            <SurveillanceGlobe isolates={clusters} />
          </div>
        </div>

        {/* Quick Isolate Roster */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 flex flex-col justify-between space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-white">Recent Clinical Genomes</h3>
            <p className="text-xs text-slate-400">Verified K. pneumoniae assemblies</p>
          </div>

          <div className="space-y-2.5 overflow-y-auto max-h-[300px] sm:max-h-[380px] pr-1">
            {isolates.slice(0, 6).map((iso) => (
              <div
                key={iso.accession}
                className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/80 hover:border-slate-700 transition-all font-mono text-xs flex justify-between items-center"
              >
                <div className="min-w-0 pr-2">
                  <div className="font-bold text-slate-200 truncate">{iso.accession}</div>
                  <div className="text-[11px] text-slate-400 truncate">
                    {iso.city || iso.country} • {iso.isolation_source || 'Clinical'}
                  </div>
                </div>
                <div className="text-right shrink-0">
                  <span className="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-emerald-400 border border-slate-700">
                    {iso.sequence_type || 'ST?'}
                  </span>
                  <div className="text-[10px] text-slate-500 mt-1">{iso.collection_year}</div>
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={() => onNavigate('isolates')}
            className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono rounded-lg transition-all border border-slate-700"
          >
            View All Genomes &rarr;
          </button>
        </div>
      </div>
    </div>
  );
};
