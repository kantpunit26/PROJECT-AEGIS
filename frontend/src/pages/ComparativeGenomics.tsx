import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import {
  SNPMatrixData,
  PhylogeneticTreeData,
  CircularAtlasData,
  MSTData,
  TimeScaledTreeData,
  BayesianSkylineData,
  PanGenomeMatrixData,
  LinearSyntenyData
} from '../types';
import { SNPHeatmap } from '../components/charts/SNPHeatmap';
import { PhylogeneticTreeViewer } from '../components/trees/PhylogeneticTreeViewer';
import { CircularGenomeViewer } from '../components/genomes/CircularGenomeViewer';
import { TransmissionNetworkMST } from '../components/trees/TransmissionNetworkMST';
import { TimeScaledPhyloViewer } from '../components/trees/TimeScaledPhyloViewer';
import { BayesianSkylinePlot } from '../components/charts/BayesianSkylinePlot';
import { PanGenomeTreeMatrix } from '../components/trees/PanGenomeTreeMatrix';
import { LinearSyntenyViewer } from '../components/genomes/LinearSyntenyViewer';
import { FolderGit2, GitBranch, Sliders, Dna, Network, Clock, Layers, TrendingUp } from 'lucide-react';

export const ComparativeGenomics: React.FC = () => {
  const [snpData, setSnpData] = useState<SNPMatrixData | null>(null);
  const [treeData, setTreeData] = useState<PhylogeneticTreeData | null>(null);
  const [circularAtlas, setCircularAtlas] = useState<CircularAtlasData | null>(null);
  const [mstData, setMstData] = useState<MSTData | null>(null);
  const [timeTreeData, setTimeTreeData] = useState<TimeScaledTreeData | null>(null);
  const [skylineData, setSkylineData] = useState<BayesianSkylineData | null>(null);
  const [panMatrixData, setPanMatrixData] = useState<PanGenomeMatrixData | null>(null);
  const [syntenyData, setSyntenyData] = useState<LinearSyntenyData | null>(null);

  const [threshold, setThreshold] = useState<number>(15);

  type SubTab = 'snp' | 'mst' | 'time_tree' | 'pan_matrix' | 'circular' | 'synteny';
  const getInitialSubTab = (): SubTab => {
    const sub = new URLSearchParams(window.location.search).get('sub') as SubTab;
    const valid: SubTab[] = ['snp', 'mst', 'time_tree', 'pan_matrix', 'circular', 'synteny'];
    return valid.includes(sub) ? sub : 'snp';
  };
  const [activeSubTab, setActiveSubTab] = useState<SubTab>(getInitialSubTab());

  useEffect(() => {
    async function loadComparative() {
      try {
        const [snp, tree, atlas, mst, timeTree, skyline, panMat, synteny] = await Promise.all([
          api.getSNPMatrix('HS11286'),
          api.getPhylogeneticTree('Klebsiella pneumoniae'),
          api.getCircularAtlas(),
          api.getMinimumSpanningTree(),
          api.getTimeScaledTree(),
          api.getBayesianSkyline(),
          api.getPanGenomeMatrix(),
          api.getLinearSynteny(),
        ]);
        setSnpData(snp);
        setTreeData(tree);
        setCircularAtlas(atlas);
        setMstData(mst);
        setTimeTreeData(timeTree);
        setSkylineData(skyline);
        setPanMatrixData(panMat);
        setSyntenyData(synteny);
      } catch (err) {
        console.error('Failed to load comparative genomics data:', err);
      }
    }
    loadComparative();
  }, []);

  const handleSubTabChange = (tab: SubTab) => {
    setActiveSubTab(tab);
    const url = new URL(window.location.href);
    url.searchParams.set('sub', tab);
    window.history.pushState({}, '', url.toString());
  };

  return (
    <div className="space-y-4 sm:space-y-6 w-full">
      {/* Title & Navigation */}
      <div className="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-3">
        <div>
          <h1 className="text-lg sm:text-xl font-bold text-white tracking-wide">Comparative Genomics & Phylogenetics</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Core-genome alignment, transmission networks, Bayesian molecular clocks, pan-genome matrices, and circular chromosome atlases
          </p>
        </div>

        {/* 6 Sub-Tab Navigation Bar */}
        <div className="flex bg-slate-900 border border-slate-800 p-1 rounded-lg text-xs font-mono overflow-x-auto w-full xl:w-auto scrollbar-none shrink-0 gap-1">
          <button
            onClick={() => handleSubTabChange('snp')}
            className={`px-3 py-1.5 rounded-md transition-all whitespace-nowrap text-center ${
              activeSubTab === 'snp' ? 'bg-crimson-800 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Core SNP Matrix
          </button>
          <button
            onClick={() => handleSubTabChange('mst')}
            className={`px-3 py-1.5 rounded-md transition-all whitespace-nowrap text-center ${
              activeSubTab === 'mst' ? 'bg-crimson-800 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Transmission MST
          </button>
          <button
            onClick={() => handleSubTabChange('time_tree')}
            className={`px-3 py-1.5 rounded-md transition-all whitespace-nowrap text-center ${
              activeSubTab === 'time_tree' ? 'bg-crimson-800 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Time-Scaled & BSP
          </button>
          <button
            onClick={() => handleSubTabChange('pan_matrix')}
            className={`px-3 py-1.5 rounded-md transition-all whitespace-nowrap text-center ${
              activeSubTab === 'pan_matrix' ? 'bg-crimson-800 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Pan-Resistome Matrix
          </button>
          <button
            onClick={() => handleSubTabChange('circular')}
            className={`px-3 py-1.5 rounded-md transition-all whitespace-nowrap text-center ${
              activeSubTab === 'circular' ? 'bg-crimson-800 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Circular Atlas (BRIG)
          </button>
          <button
            onClick={() => handleSubTabChange('synteny')}
            className={`px-3 py-1.5 rounded-md transition-all whitespace-nowrap text-center ${
              activeSubTab === 'synteny' ? 'bg-crimson-800 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Linear Synteny (Easyfig)
          </button>
        </div>
      </div>

      {/* 1. Core SNP Matrix Tab */}
      {activeSubTab === 'snp' && (
        <div className="space-y-4">
          <div className="bg-slate-900/60 border border-slate-800 p-3.5 sm:p-4 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs font-mono">
            <div className="flex items-center space-x-2.5">
              <Sliders className="w-4 h-4 text-crimson-400 shrink-0" />
              <span className="text-slate-300">Outbreak Threshold:</span>
              <span className="text-crimson-400 font-bold">&le; {threshold} SNPs</span>
            </div>
            <div className="flex items-center space-x-3 w-full sm:w-auto">
              <input
                type="range"
                min="5"
                max="50"
                step="1"
                value={threshold}
                onChange={(e) => setThreshold(Number(e.target.value))}
                className="w-full sm:w-48 accent-crimson-600 cursor-pointer"
              />
              <span className="text-slate-400 shrink-0 font-bold text-xs">{threshold} bp</span>
            </div>
          </div>

          {snpData && <SNPHeatmap data={snpData} outbreakThreshold={threshold} />}
        </div>
      )}

      {/* 2. Minimum Spanning Tree (MST) Tab */}
      {activeSubTab === 'mst' && mstData && <TransmissionNetworkMST data={mstData} />}

      {/* 3. Time-Scaled Phylodynamic Tree & Bayesian Skyline Demography Tab */}
      {activeSubTab === 'time_tree' && (
        <div className="space-y-6">
          {timeTreeData && <TimeScaledPhyloViewer data={timeTreeData} />}
          {skylineData && <BayesianSkylinePlot data={skylineData} />}
        </div>
      )}

      {/* 4. Pan-Genome Tree Aligned with Matrix Tab */}
      {activeSubTab === 'pan_matrix' && panMatrixData && (
        <PanGenomeTreeMatrix data={panMatrixData} />
      )}

      {/* 5. Circular Chromosome Atlas Tab */}
      {activeSubTab === 'circular' && (
        <div className="flex justify-center w-full">
          <div className="w-full max-w-4xl">
            <CircularGenomeViewer atlasData={circularAtlas} />
          </div>
        </div>
      )}

      {/* 6. Linear Synteny & MGE Resistance Islands Tab */}
      {activeSubTab === 'synteny' && syntenyData && (
        <LinearSyntenyViewer data={syntenyData} />
      )}
    </div>
  );
};
