import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { SurveillanceAlert } from '../types';
import { FileSpreadsheet, Download, Bell, ShieldAlert, CheckCircle, Radio } from 'lucide-react';

interface ReportsProps {
  selectedOrganism?: string;
}

export const Reports: React.FC<ReportsProps> = ({
  selectedOrganism = 'Klebsiella pneumoniae'
}) => {
  const [alerts, setAlerts] = useState<SurveillanceAlert[]>([]);
  const [downloading, setDownloading] = useState<string | null>(null);

  useEffect(() => {
    async function loadAlerts() {
      try {
        const data = await api.getAlerts(selectedOrganism);
        setAlerts(data);
      } catch (err) {
        console.error('Failed to load alerts:', err);
      }
    }
    loadAlerts();
  }, [selectedOrganism]);

  const handleDownload = async (format: 'csv' | 'geojson' | 'who-glass' | 'newick') => {
    setDownloading(format);
    const orgQuery = `?organism=${encodeURIComponent(selectedOrganism)}`;
    try {
      if (format === 'csv') {
        window.open(`/api/v1/reports/export/csv${orgQuery}`, '_blank');
      } else if (format === 'newick') {
        window.open('/api/v1/reports/export/newick', '_blank');
      } else if (format === 'geojson') {
        const res = await fetch(`/api/v1/reports/export/geojson${orgQuery}`);
        const data = await res.json();
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/geo+json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `aegis_${selectedOrganism.toLowerCase().replace(/[^a-z0-9]/g, '_')}_surveillance.geojson`;
        a.click();
      } else if (format === 'who-glass') {
        const res = await fetch('/api/v1/reports/export/who-glass');
        const data = await res.json();
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'aegis_who_glass_submission.json';
        a.click();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setDownloading(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-xl font-bold text-white tracking-wide">Surveillance Alerts & Export Center</h1>
            <span className="px-2.5 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800 italic">
              {selectedOrganism}
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Generate and export WHO GLASS standardized epidemiological reports, core phylogenies, and spatial GeoJSON datasets
          </p>
        </div>
      </div>

      {/* Standardized Export Formats */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
        <div>
          <h3 className="text-sm font-semibold text-white">Standardized Scientific Data Packages</h3>
          <p className="text-xs text-slate-400">Download analyzed surveillance datasets for external bioinformatics pipelines and WHO reporting</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono text-xs">
          {/* CSV Export */}
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3 flex flex-col justify-between">
            <div>
              <div className="font-bold text-slate-200">Isolates & AMR Table</div>
              <p className="text-[11px] text-slate-400 font-sans mt-1">Complete metadata, ST, K/O locus, carbapenemases, and QC flags in CSV format.</p>
            </div>
            <button
              onClick={() => handleDownload('csv')}
              disabled={downloading === 'csv'}
              className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700 hover:border-crimson-600 transition-all flex items-center justify-center space-x-1.5"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export CSV</span>
            </button>
          </div>

          {/* GeoJSON Export */}
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3 flex flex-col justify-between">
            <div>
              <div className="font-bold text-slate-200">RFC 7946 GeoJSON</div>
              <p className="text-[11px] text-slate-400 font-sans mt-1">Geospatial feature collection compatible with QGIS, ArcGIS, Deck.gl, and Mapbox.</p>
            </div>
            <button
              onClick={() => handleDownload('geojson')}
              disabled={downloading === 'geojson'}
              className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700 hover:border-crimson-600 transition-all flex items-center justify-center space-x-1.5"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export GeoJSON</span>
            </button>
          </div>

          {/* WHO GLASS Export */}
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3 flex flex-col justify-between">
            <div>
              <div className="font-bold text-slate-200">WHO GLASS Schema</div>
              <p className="text-[11px] text-slate-400 font-sans mt-1">Global Antimicrobial Resistance Surveillance System mapped AST and specimen records.</p>
            </div>
            <button
              onClick={() => handleDownload('who-glass')}
              disabled={downloading === 'who-glass'}
              className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700 hover:border-crimson-600 transition-all flex items-center justify-center space-x-1.5"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export GLASS</span>
            </button>
          </div>

          {/* Newick Export */}
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3 flex flex-col justify-between">
            <div>
              <div className="font-bold text-slate-200">Phylogenetic Newick</div>
              <p className="text-[11px] text-slate-400 font-sans mt-1">IQ-TREE maximum likelihood Newick tree with branch lengths and bootstrap values.</p>
            </div>
            <button
              onClick={() => handleDownload('newick')}
              disabled={downloading === 'newick'}
              className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700 hover:border-crimson-600 transition-all flex items-center justify-center space-x-1.5"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export Newick</span>
            </button>
          </div>
        </div>
      </div>

      {/* Outbreak Alert Feeds */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex items-center space-x-2">
          <Bell className="w-4 h-4 text-crimson-500" />
          <h3 className="text-sm font-semibold text-white">Active Surveillance Alerts</h3>
        </div>

        <div className="space-y-3">
          {alerts.map((al) => (
            <div
              key={al.id}
              className="p-3.5 sm:p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 font-mono text-xs"
            >
              <div className="flex items-start space-x-3 w-full">
                <div className="p-2 bg-crimson-900/40 rounded-lg text-crimson-400 mt-0.5 border border-crimson-800/60 shrink-0">
                  <ShieldAlert className="w-5 h-5 animate-pulse" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
                    <span className="font-bold text-white text-xs sm:text-sm">{al.title}</span>
                    <span className="px-2 py-0.5 rounded text-[9px] sm:text-[10px] bg-crimson-900 text-crimson-300 font-bold uppercase">
                      {al.severity}
                    </span>
                    <span className="text-slate-500 text-[10px] sm:text-[11px]">{new Date(al.created_at).toLocaleDateString()}</span>
                  </div>
                  <p className="text-[11px] sm:text-xs text-slate-300 font-sans mt-1.5 max-w-3xl leading-relaxed">{al.message}</p>
                  {al.isolate_accessions && (
                    <div className="mt-2 text-[10px] sm:text-[11px] text-slate-400">
                      Cluster isolates: <span className="text-slate-200 font-bold">{al.isolate_accessions.join(', ')}</span>
                    </div>
                  )}
                </div>
              </div>

              <div className="flex items-center space-x-2 shrink-0 self-end sm:self-auto">
                <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 text-[10px] sm:text-[11px] border border-slate-700">
                  {al.acknowledged ? 'Acknowledged' : 'Active Warning'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

