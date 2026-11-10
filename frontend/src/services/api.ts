import {
  Isolate,
  ASTConcordanceMetrics,
  SNPMatrixData,
  PhylogeneticTreeData,
  SpatialCluster,
  SurveillanceAlert,
  SEIRSimulationResult
} from '../types';

const API_BASE = '/api/v1';

export const api = {
  // System Health
  async getHealth() {
    const res = await fetch(`${API_BASE}/health`);
    return res.json();
  },

  // Isolates
  async getIsolates(params?: { organism?: string; country?: string; amr_gene?: string }) {
    const searchParams = new URLSearchParams();
    if (params?.organism) searchParams.append('organism', params.organism);
    if (params?.country) searchParams.append('country', params.country);
    if (params?.amr_gene) searchParams.append('amr_gene', params.amr_gene);
    const res = await fetch(`${API_BASE}/isolates?${searchParams.toString()}`);
    return (await res.json()) as Isolate[];
  },

  async getIsolateDetail(id: string) {
    const res = await fetch(`${API_BASE}/isolates/${id}`);
    return res.json();
  },

  // AMR
  async getAMRPrevalence(organism?: string) {
    const url = organism ? `${API_BASE}/amr/prevalence?organism=${encodeURIComponent(organism)}` : `${API_BASE}/amr/prevalence`;
    const res = await fetch(url);
    return res.json();
  },

  async getAMRCoOccurrence(topN: number = 10) {
    const res = await fetch(`${API_BASE}/amr/co-occurrence?top_n=${topN}`);
    return res.json();
  },

  // Typing
  async getMLSTDistribution(organism?: string) {
    const url = organism ? `${API_BASE}/typing/mlst-distribution?organism=${encodeURIComponent(organism)}` : `${API_BASE}/typing/mlst-distribution`;
    const res = await fetch(url);
    return res.json();
  },

  async getKleborateSummary() {
    const res = await fetch(`${API_BASE}/typing/kleborate-summary`);
    return res.json();
  },

  // AST Concordance
  async getASTConcordance(antibiotic?: string) {
    const url = antibiotic ? `${API_BASE}/ast/concordance?antibiotic=${encodeURIComponent(antibiotic)}` : `${API_BASE}/ast/concordance`;
    const res = await fetch(url);
    return (await res.json()) as ASTConcordanceMetrics[];
  },

  // Comparative & Phylogeny
  async getSNPMatrix(referenceGenome: string = 'HS11286') {
    const res = await fetch(`${API_BASE}/comparative/snp-matrix`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reference_genome: referenceGenome })
    });
    return (await res.json()) as SNPMatrixData;
  },

  async getPhylogeneticTree(organism: string = 'Klebsiella pneumoniae') {
    const res = await fetch(`${API_BASE}/comparative/tree?organism=${encodeURIComponent(organism)}`);
    return (await res.json()) as PhylogeneticTreeData;
  },

  async getCircularGenome() {
    const res = await fetch(`${API_BASE}/comparative/circular-genome`);
    return res.json();
  },

  async getCircularAtlas() {
    const res = await fetch(`${API_BASE}/comparative/circular-atlas`);
    return res.json();
  },

  async getMinimumSpanningTree() {
    const res = await fetch(`${API_BASE}/comparative/minimum-spanning-tree`);
    return res.json();
  },

  async getTimeScaledTree() {
    const res = await fetch(`${API_BASE}/comparative/time-scaled-tree`);
    return res.json();
  },

  async getBayesianSkyline() {
    const res = await fetch(`${API_BASE}/comparative/bayesian-skyline`);
    return res.json();
  },

  async getPanGenomeMatrix() {
    const res = await fetch(`${API_BASE}/comparative/pan-genome-matrix`);
    return res.json();
  },

  async getLinearSynteny() {
    const res = await fetch(`${API_BASE}/comparative/linear-synteny`);
    return res.json();
  },

  // Plasmids
  async getPlasmidSummary() {
    const res = await fetch(`${API_BASE}/plasmids/summary`);
    return res.json();
  },

  async getPlasmidMatrix() {
    const res = await fetch(`${API_BASE}/plasmids/matrix`);
    return res.json();
  },

  async getMobilizationSankey() {
    const res = await fetch(`${API_BASE}/plasmids/sankey`);
    return res.json();
  },

  async getPartitionedHeatmaps() {
    const res = await fetch(`${API_BASE}/plasmids/heatmaps`);
    return res.json();
  },

  // Geospatial Surveillance
  async getSpatialClusters(params?: { organism?: string; country?: string; gene?: string }) {
    const searchParams = new URLSearchParams();
    if (params?.organism) searchParams.append('organism', params.organism);
    if (params?.country) searchParams.append('country', params.country);
    if (params?.gene) searchParams.append('gene', params.gene);
    const res = await fetch(`${API_BASE}/surveillance/spatial-clusters?${searchParams.toString()}`);
    return (await res.json()) as SpatialCluster[];
  },

  async executeNLQuery(query: string) {
    const res = await fetch(`${API_BASE}/surveillance/nl-query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    return res.json();
  },

  async getAlerts() {
    const res = await fetch(`${API_BASE}/surveillance/alerts`);
    return (await res.json()) as SurveillanceAlert[];
  },

  // SEIR Modelling
  async simulateSEIR(params: any) {
    const res = await fetch(`${API_BASE}/modelling/seir/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    return (await res.json()) as SEIRSimulationResult;
  }
};

