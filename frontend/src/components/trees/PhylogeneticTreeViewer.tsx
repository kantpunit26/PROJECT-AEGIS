import React, { useState } from 'react';
import { PhylogeneticTreeData } from '../../types';
import { GitBranch, Download, Info } from 'lucide-react';

interface PhylogeneticTreeViewerProps {
  treeData: PhylogeneticTreeData;
}

export const PhylogeneticTreeViewer: React.FC<PhylogeneticTreeViewerProps> = ({ treeData }) => {
  const [selectedLeaf, setSelectedLeaf] = useState<string | null>(null);

  // Parse simple taxa names from Newick string
  const taxaMatches = treeData.newick_string.match(/GCA_\d+\.\d+/g) || [];
  const uniqueTaxa = Array.from(new Set(taxaMatches));

  const metadata = treeData.metadata_tracks || {};
  const stTrack = metadata['ST'] || {};
  const countryTrack = metadata['Country'] || {};
  const carbTrack = metadata['Carbapenemase'] || {};

  const downloadNewick = () => {
    const blob = new Blob([treeData.newick_string], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${treeData.tree_name.toLowerCase().replace(/\s+/g, '_')}.nwk`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div>
          <div className="flex items-center space-x-2">
            <GitBranch className="w-4 h-4 text-crimson-500" />
            <h3 className="text-sm font-semibold text-white">{treeData.tree_name}</h3>
          </div>
          <p className="text-xs text-slate-400 font-mono">
            Model: {treeData.substitution_model} | Bootstrap: {treeData.bootstrap_replicates}x UFBoot
          </p>
        </div>

        <button
          onClick={downloadNewick}
          className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg text-xs font-mono transition-all border border-slate-700"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export Newick</span>
        </button>
      </div>

      {/* Scientific Caution Alert */}
      <div className="bg-slate-950/80 border border-slate-800 p-3 rounded-lg flex items-start space-x-2 text-xs text-slate-400">
        <Info className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
        <p>
          <strong className="text-slate-200">Epidemiological Note:</strong> Phylogenetic proximity represents evolutionary relatedness, not definitive proof of direct person-to-person transmission without epidemiological contact tracing.
        </p>
      </div>

      {/* Multi-Track Tree Layout */}
      <div className="border border-slate-800 rounded-lg overflow-x-auto bg-slate-950/40 p-4">
        <table className="w-full text-xs font-mono border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-slate-500 text-[11px] uppercase">
              <th className="text-left py-2 px-3">Phylogenetic Leaf / Accession</th>
              <th className="text-left py-2 px-3">Sequence Type (ST)</th>
              <th className="text-left py-2 px-3">Geographic Provenance</th>
              <th className="text-left py-2 px-3">Carbapenemase Determinants</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {uniqueTaxa.map((acc, index) => {
              const st = stTrack[acc] || 'ST?';
              const country = countryTrack[acc] || 'Unknown';
              const carb = carbTrack[acc] || 'Negative';
              const hasCarb = carb !== 'Negative' && carb !== 'None';

              return (
                <tr
                  key={acc}
                  onClick={() => setSelectedLeaf(acc)}
                  className={`cursor-pointer transition-colors ${
                    selectedLeaf === acc ? 'bg-crimson-950/40' : 'hover:bg-slate-800/40'
                  }`}
                >
                  <td className="py-2.5 px-3 flex items-center space-x-3">
                    {/* Visual Dendrogram Branch Stub */}
                    <div className="flex items-center text-slate-600 font-mono select-none">
                      <span>{index === 0 ? '┌──' : index === uniqueTaxa.length - 1 ? '└──' : '├──'}</span>
                      <span className="w-4 h-px bg-slate-700"></span>
                    </div>
                    <span className="font-bold text-slate-200">{acc}</span>
                  </td>
                  <td className="py-2.5 px-3">
                    <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-emerald-400 font-semibold">
                      {st}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-300">{country}</td>
                  <td className="py-2.5 px-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[11px] font-semibold ${
                        hasCarb
                          ? 'bg-crimson-950 border border-crimson-800 text-crimson-400'
                          : 'text-slate-500'
                      }`}
                    >
                      {carb}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

