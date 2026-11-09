import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Isolate } from '../types';
import { Search, Filter, Dna, CheckCircle2, AlertTriangle, XCircle, Eye, X } from 'lucide-react';

export const Isolates: React.FC = () => {
  const [isolates, setIsolates] = useState<Isolate[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [qcFilter, setQcFilter] = useState('ALL');
  const [selectedIsolate, setSelectedIsolate] = useState<any | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    async function fetchIsolates() {
      try {
        const data = await api.getIsolates();
        setIsolates(data);
      } catch (err) {
        console.error('Failed to load isolates:', err);
      }
    }
    fetchIsolates();
  }, []);

  const handleOpenDetail = async (id: string) => {
    setDetailLoading(true);
    try {
      const data = await api.getIsolateDetail(id);
      setSelectedIsolate(data);
    } catch (err) {
      console.error(err);
    } finally {
      setDetailLoading(false);
    }
  };

  const filtered = isolates.filter((iso) => {
    const matchesSearch =
      iso.accession.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (iso.strain && iso.strain.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (iso.country && iso.country.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (iso.sequence_type && iso.sequence_type.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesQc = qcFilter === 'ALL' || iso.qc_status === qcFilter;
    return matchesSearch && matchesQc;
  });

  const getQcBadge = (status: string) => {
    if (status === 'PASS') {
      return (
        <span className="flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-emerald-950 border border-emerald-800 text-emerald-400 font-bold">
          <CheckCircle2 className="w-3 h-3" />
          <span>PASS</span>
        </span>
      );
    }
    if (status === 'WARNING') {
      return (
        <span className="flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-amber-950 border border-amber-800 text-amber-400 font-bold">
          <AlertTriangle className="w-3 h-3" />
          <span>WARNING</span>
        </span>
      );
    }
    return (
      <span className="flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-crimson-950 border border-crimson-800 text-crimson-400 font-bold">
        <XCircle className="w-3 h-3" />
        <span>FAIL</span>
      </span>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div>
          <h1 className="text-xl font-bold text-white tracking-wide">Genomic Isolates Registry</h1>
          <p className="text-xs text-slate-400">
            Validated genome assemblies, provenance metadata, and sequence metrics
          </p>
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl flex flex-col sm:flex-row gap-3 justify-between items-center">
        <div className="relative w-full sm:w-96">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by accession, strain, country, ST..."
            className="w-full bg-slate-950 border border-slate-700/80 rounded-lg pl-9 pr-4 py-2 text-xs font-mono text-slate-100 placeholder-slate-500 focus:outline-none focus:border-crimson-500"
          />
        </div>

        <div className="flex items-center space-x-3 w-full sm:w-auto text-xs font-mono">
          <span className="text-slate-400">QC Status:</span>
          <select
            value={qcFilter}
            onChange={(e) => setQcFilter(e.target.value)}
            className="bg-slate-950 border border-slate-700/80 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-crimson-500"
          >
            <option value="ALL">All Statuses</option>
            <option value="PASS">PASS</option>
            <option value="WARNING">WARNING</option>
            <option value="FAIL">FAIL</option>
          </select>
        </div>
      </div>

      {/* Main Isolates Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-xs font-mono border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-slate-500 text-[11px] uppercase bg-slate-950/40">
                <th className="text-left py-3 px-4">Accession</th>
                <th className="text-left py-3 px-4">Organism & Strain</th>
                <th className="text-left py-3 px-4">ST</th>
                <th className="text-left py-3 px-4">Origin</th>
                <th className="text-left py-3 px-4">Source</th>
                <th className="text-center py-3 px-4">Genome Size</th>
                <th className="text-center py-3 px-4">GC %</th>
                <th className="text-center py-3 px-4">QC</th>
                <th className="text-right py-3 px-4">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {filtered.map((iso) => (
                <tr key={iso.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 px-4 font-bold text-slate-200">{iso.accession}</td>
                  <td className="py-3 px-4">
                    <span className="italic text-slate-300">{iso.organism}</span>
                    {iso.strain && <span className="text-slate-500 ml-1.5 font-sans">({iso.strain})</span>}
                  </td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-emerald-400 font-semibold">
                      {iso.sequence_type || 'ST?'}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-300">
                    {iso.city ? `${iso.city}, ${iso.country}` : iso.country || 'Unknown'}
                  </td>
                  <td className="py-3 px-4 text-slate-400">{iso.isolation_source || 'Clinical'}</td>
                  <td className="py-3 px-4 text-center text-slate-300">
                    {iso.genome_size ? `${(iso.genome_size / 1e6).toFixed(2)} Mb` : '-'}
                  </td>
                  <td className="py-3 px-4 text-center text-slate-300">
                    {iso.gc_percent ? `${iso.gc_percent}%` : '-'}
                  </td>
                  <td className="py-3 px-4 flex justify-center">{getQcBadge(iso.qc_status)}</td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => handleOpenDetail(iso.id)}
                      className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700 hover:border-crimson-600 transition-all flex items-center space-x-1 ml-auto"
                    >
                      <Eye className="w-3.5 h-3.5 text-slate-400" />
                      <span>Inspect</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Isolate Detail Modal Drawer */}
      {selectedIsolate && (
        <div className="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto p-6 space-y-6 shadow-2xl">
            <div className="flex justify-between items-start border-b border-slate-800 pb-4">
              <div>
                <div className="flex items-center space-x-3">
                  <span className="text-xl font-bold font-mono text-white">{selectedIsolate.accession}</span>
                  {getQcBadge(selectedIsolate.qc_status)}
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  {selectedIsolate.organism} • Strain {selectedIsolate.strain} ({selectedIsolate.country})
                </p>
              </div>
              <button
                onClick={() => setSelectedIsolate(null)}
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* AMR Determinants Grid */}
            <div className="space-y-2">
              <h3 className="text-sm font-semibold text-white">AMRFinderPlus Resistance Determinants</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                {selectedIsolate.amr_determinants?.map((d: any) => (
                  <div
                    key={d.id}
                    className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 font-mono text-xs space-y-1"
                  >
                    <div className="font-bold text-crimson-400">{d.gene_symbol}</div>
                    <div className="text-[11px] text-slate-400">{d.subclass || d.drug_class}</div>
                    <div className="text-[10px] text-slate-500 flex justify-between">
                      <span>Context: {d.predicted_context}</span>
                      <span>{d.confidence}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Experimental AST Records */}
            <div className="space-y-2">
              <h3 className="text-sm font-semibold text-white">Experimental Antimicrobial Susceptibility (AST)</h3>
              <div className="border border-slate-800 rounded-lg overflow-x-auto">
                <table className="w-full text-xs font-mono">
                  <thead>
                    <tr className="border-b border-slate-800 text-slate-500 bg-slate-950/60">
                      <th className="py-2 px-3 text-left">Antibiotic</th>
                      <th className="py-2 px-3 text-center">MIC Value</th>
                      <th className="py-2 px-3 text-center">Phenotype</th>
                      <th className="py-2 px-3 text-center">Genotypic Pred</th>
                      <th className="py-2 px-3 text-right">Concordance</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {selectedIsolate.ast_records?.map((ast: any) => (
                      <tr key={ast.antibiotic}>
                        <td className="py-2 px-3 text-slate-200">{ast.antibiotic}</td>
                        <td className="py-2 px-3 text-center text-slate-300">
                          {ast.mic_value} {ast.mic_unit}
                        </td>
                        <td className="py-2 px-3 text-center font-bold text-crimson-400">{ast.phenotype}</td>
                        <td className="py-2 px-3 text-center text-slate-300">{ast.genotypic_prediction}</td>
                        <td className="py-2 px-3 text-right text-emerald-400 font-semibold">{ast.concordance_status}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Plasmids */}
            {selectedIsolate.plasmids && selectedIsolate.plasmids.length > 0 && (
              <div className="space-y-2">
                <h3 className="text-sm font-semibold text-white">MOB-Suite Reconstructed Plasmids</h3>
                <div className="space-y-2">
                  {selectedIsolate.plasmids.map((p: any) => (
                    <div key={p.plasmid_id} className="p-3 bg-slate-950 border border-slate-800 rounded-lg font-mono text-xs flex justify-between items-center">
                      <div>
                        <div className="font-bold text-slate-200">{p.plasmid_id} ({p.mobility})</div>
                        <div className="text-[11px] text-slate-400">Replicons: {p.replicon_types?.join(', ') || 'Unknown'}</div>
                      </div>
                      <div className="text-right">
                        <span className="text-slate-400">{p.predicted_length?.toLocaleString()} bp</span>
                        {p.associated_amr_genes && (
                          <div className="text-[11px] text-crimson-400">{p.associated_amr_genes.join(', ')}</div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

