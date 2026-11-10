import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { SpatialCluster } from '../types';
import { SurveillanceGlobe } from '../components/globe/SurveillanceGlobe';
import { Search, Sparkles, Navigation, Layers, AlertCircle, CheckCircle } from 'lucide-react';

export const Surveillance: React.FC = () => {
  const [clusters, setClusters] = useState<SpatialCluster[]>([]);
  const [queryInput, setQueryInput] = useState(
    'Show all K. pneumoniae isolates with blaNDM within 50 km of Vadodara'
  );
  const [queryResult, setQueryResult] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedCountry, setSelectedCountry] = useState<string>('ALL');

  useEffect(() => {
    async function fetchClusters() {
      try {
        const data = await api.getSpatialClusters();
        setClusters(data);
      } catch (err) {
        console.error('Failed to load clusters:', err);
      }
    }
    fetchClusters();
  }, []);

  const handleExecuteNLQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!queryInput.trim()) return;
    setLoading(true);
    try {
      const res = await api.executeNLQuery(queryInput);
      setQueryResult(res);
      if (res.matched_isolates) {
        setClusters(res.matched_isolates);
      }
    } catch (err) {
      console.error('Query execution error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleResetFilters = async () => {
    setLoading(true);
    try {
      const data = await api.getSpatialClusters();
      setClusters(data);
      setQueryResult(null);
      setSelectedCountry('ALL');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4 sm:space-y-6 w-full">
      {/* Page Title & Mission */}
      <div>
        <h1 className="text-lg sm:text-xl font-bold text-white tracking-wide">Geospatial Surveillance & Intelligence</h1>
        <p className="text-xs text-slate-400 mt-0.5">
          PostGIS spatial index engine with safe parameterized natural language query translation
        </p>
      </div>

      {/* Natural Language Query Box */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-3.5 sm:p-4 shadow-xl shadow-slate-950/50">
        <form onSubmit={handleExecuteNLQuery} className="space-y-3">
          <div className="flex items-center space-x-2 text-xs text-slate-300 font-medium">
            <Sparkles className="w-4 h-4 text-crimson-400 shrink-0" />
            <span className="truncate">Natural-Language Spatial Query Interface (Parameterized & Safe)</span>
          </div>

          <div className="flex flex-col sm:flex-row gap-2">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="text"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                placeholder="e.g. Show all K. pneumoniae isolates with blaNDM within 50 km of Vadodara"
                className="w-full bg-slate-950/80 border border-slate-700/80 rounded-lg pl-9 pr-4 py-2.5 text-xs font-mono text-slate-100 placeholder-slate-500 focus:outline-none focus:border-crimson-500"
              />
            </div>
            <div className="flex gap-2">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 sm:flex-initial px-4 sm:px-5 py-2.5 bg-crimson-700 hover:bg-crimson-600 text-white rounded-lg text-xs font-semibold font-mono transition-all disabled:opacity-50 flex items-center justify-center space-x-2 shrink-0"
              >
                <Navigation className="w-3.5 h-3.5" />
                <span>{loading ? 'Executing...' : 'Run Query'}</span>
              </button>
              <button
                type="button"
                onClick={handleResetFilters}
                className="px-3.5 sm:px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-mono transition-all shrink-0"
              >
                Reset
              </button>
            </div>
          </div>
        </form>

        {/* Interpreted Safe Query Feedback */}
        {queryResult && (
          <div className="mt-3.5 pt-3.5 border-t border-slate-800/80 text-xs font-mono flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-slate-400">
            <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
              <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
              <span>Interpreted: </span>
              <span className="text-white font-semibold">
                {queryResult.interpreted_query.organism}
              </span>
              <span>• Gene: </span>
              <span className="text-crimson-400 font-semibold">
                {queryResult.interpreted_query.target_gene || 'Any'}
              </span>
              {queryResult.interpreted_query.target_location && (
                <>
                  <span>• Proximity: </span>
                  <span className="text-amber-400 font-semibold">
                    &le; {queryResult.interpreted_query.radius_km} km of {queryResult.interpreted_query.target_location}
                  </span>
                </>
              )}
            </div>
            <div className="text-slate-400 shrink-0">
              Matched: <strong className="text-emerald-400">{queryResult.total_matched}</strong> isolates ({queryResult.execution_time_ms} ms)
            </div>
          </div>
        )}
      </div>

      {/* 3D Globe & Spatial Cluster Roster */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        <div className="lg:col-span-2 h-[340px] sm:h-[450px] lg:h-[560px] rounded-xl overflow-hidden border border-slate-800 bg-slate-950/60 w-full">
          <SurveillanceGlobe isolates={clusters} />
        </div>

        {/* Filtered Spatial Isolates Table */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 flex flex-col justify-between space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-white">Spatial Clusters & Proximity</h3>
            <p className="text-xs text-slate-400">Geographic coordinates & resistance phenotypes</p>
          </div>

          <div className="space-y-2 overflow-y-auto max-h-[300px] sm:max-h-[460px] pr-1">
            {clusters.map((c) => (
              <div
                key={c.id}
                className="p-3 rounded-lg bg-slate-950/70 border border-slate-800 font-mono text-xs space-y-1.5 hover:border-crimson-600/50 transition-all"
              >
                <div className="flex justify-between items-center">
                  <span className="font-bold text-slate-200 truncate pr-2">{c.accession}</span>
                  <span className="px-1.5 py-0.5 rounded text-[10px] bg-slate-800 text-emerald-400 border border-slate-700 shrink-0">
                    {c.sequence_type || 'ST?'}
                  </span>
                </div>
                <div className="text-slate-400 text-[11px] flex justify-between">
                  <span className="truncate pr-1">{c.city}, {c.country}</span>
                  {c.distance_km !== undefined && (
                    <span className="text-amber-400 font-semibold shrink-0">{c.distance_km} km away</span>
                  )}
                </div>
                <div className="text-[11px] pt-0.5">
                  <span className="text-slate-500">Coordinates: </span>
                  <span className="text-slate-400">{c.latitude.toFixed(4)}, {c.longitude.toFixed(4)}</span>
                </div>
                {c.carbapenemases.length > 0 && (
                  <div className="text-[11px] text-crimson-400 font-semibold truncate">
                    Carbapenemase: {c.carbapenemases.join(', ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
