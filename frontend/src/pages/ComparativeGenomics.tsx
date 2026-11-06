import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { SNPMatrixData, PhylogeneticTreeData } from '../types';
import { SNPHeatmap } from '../components/charts/SNPHeatmap';
import { PhylogeneticTreeViewer } from '../components/trees/PhylogeneticTreeViewer';
import { CircularGenomeViewer } from '../components/genomes/CircularGenomeViewer';
import { FolderGit2, GitBranch, Sliders, AlertCircle } from 'lucide-react';

export const ComparativeGenomics: React.FC = () => {
  const [snpData, setSnpData] = useState<SNPMatrixData | null>(null);
  const [treeData, setTreeData] = useState<PhylogeneticTreeData | null>(null);
  const [circularData, setCircularData] = useState<any[]>([]);
  const [threshold, setThreshold] = useState<number>(15);
  const [activeSubTab, setActiveSubTab] = useState<'snp' | 'tree' | 'circular'>('snp');

  useEffect(() => {
    async function loadComparative() {
      try {
        const [snp, tree, circular] = await Promise.all([
          api.getSNPMatrix('HS11286'),
          api.getPhylogeneticTree('Klebsiella pneumoniae'),
          api.getCircularGenome(),
        ]);
        setSnpData(snp);
        setTreeData(tree);
        setCircularData(circular);
      } catch (err) {
        console.error('Failed to load comparative genomics data:', err);
      }
    }
    loadComparative();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div>
          <h1 className="text-xl font-bold text-white tracking-wide">Comparative Genomics & Phylogenetics</h1>
          <p className="text-xs text-slate-400">
            Core-genome alignment, pairwise SNP distance matrices, IQ-TREE maximum likelihood, and circular chromosomes
          </p>
        </div>

        {/* Sub-tab selection */}
        <div className="flex bg-slate-900 border border-slate-800 p-1 rounded-lg text-xs font-mono">
          <button
            onClick={() => setActiveSubTab('snp')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeSubTab === 'snp' ? 'bg-crimson-800 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Core SNP Matrix
          </button>
          <button
            onClick={() => setActiveSubTab('tree')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeSubTab === 'tree' ? 'bg-crimson-800 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Phylogenetic Tree
          </button>
          <button
            onClick={() => setActiveSubTab('circular')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeSubTab === 'circular' ? 'bg-crimson-800 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Circular Chromosome
          </button>
        </div>
      </div>

      {activeSubTab === 'snp' && (
        <div className="space-y-4">
          {/* Outbreak Threshold Slider */}
          <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl flex items-center justify-between text-xs font-mono">
            <div className="flex items-center space-x-3">
              <Sliders className="w-4 h-4 text-crimson-400" />
              <span className="text-slate-300">Micro-outbreak SNP Distance Threshold:</span>
              <span className="text-crimson-400 font-bold">&le; {threshold} SNPs</span>
            </div>
            <input
              type="range"
              min="5"
              max="50"
              step="1"
              value={threshold}
              onChange={(e) => setThreshold(Number(e.target.value))}
              className="w-48 accent-crimson-600 cursor-pointer"
            />
          </div>

          {snpData && <SNPHeatmap data={snpData} outbreakThreshold={threshold} />}
        </div>
      )}

      {activeSubTab === 'tree' && treeData && <PhylogeneticTreeViewer treeData={treeData} />}

      {activeSubTab === 'circular' && (
        <div className="flex justify-center">
          <div className="w-full max-w-2xl">
            <CircularGenomeViewer coordinates={circularData} />
          </div>
        </div>
      )}
    </div>
  );
};
