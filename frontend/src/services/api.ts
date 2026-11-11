import {
  Isolate,
  ASTConcordanceMetrics,
  SNPMatrixData,
  PhylogeneticTreeData,
  SpatialCluster,
  SurveillanceAlert,
  SEIRSimulationResult,
  MICPredictionResponse,
  AICopilotBrief,
  WastewaterSite,
  WBELeadTimeResponse,
  OneHealthMatrix,
  AlertSimulationResult
} from '../types';

const metaEnv = (import.meta as any).env;
const API_BASE = (metaEnv?.VITE_API_URL ? String(metaEnv.VITE_API_URL).replace(/\/$/, '') : '') + '/api/v1';

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

  async getAMRCoOccurrence(topN: number = 10, organism?: string) {
    const url = organism
      ? `${API_BASE}/amr/co-occurrence?top_n=${topN}&organism=${encodeURIComponent(organism)}`
      : `${API_BASE}/amr/co-occurrence?top_n=${topN}`;
    const res = await fetch(url);
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
  async getASTConcordance(antibiotic?: string, organism?: string) {
    const params = new URLSearchParams();
    if (antibiotic) params.append('antibiotic', antibiotic);
    if (organism) params.append('organism', organism);
    const queryStr = params.toString() ? `?${params.toString()}` : '';
    const res = await fetch(`${API_BASE}/ast/concordance${queryStr}`);
    return (await res.json()) as ASTConcordanceMetrics[];
  },

  async getASTRecords(antibiotic?: string, organism?: string) {
    const params = new URLSearchParams();
    if (antibiotic) params.append('antibiotic', antibiotic);
    if (organism) params.append('organism', organism);
    const queryStr = params.toString() ? `?${params.toString()}` : '';
    const res = await fetch(`${API_BASE}/ast/records${queryStr}`);
    return res.json();
  },


  // Comparative & Phylogeny
  async getSNPMatrix(referenceGenome: string = 'HS11286', organism?: string) {
    const res = await fetch(`${API_BASE}/comparative/snp-matrix`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reference_genome: referenceGenome, organism: organism || 'Klebsiella pneumoniae' })
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

  async getCircularAtlas(organism?: string) {
    const url = organism ? `${API_BASE}/comparative/circular-atlas?organism=${encodeURIComponent(organism)}` : `${API_BASE}/comparative/circular-atlas`;
    const res = await fetch(url);
    return res.json();
  },

  async getMinimumSpanningTree(organism?: string) {
    const url = organism ? `${API_BASE}/comparative/minimum-spanning-tree?organism=${encodeURIComponent(organism)}` : `${API_BASE}/comparative/minimum-spanning-tree`;
    const res = await fetch(url);
    return res.json();
  },

  async getTimeScaledTree(organism?: string) {
    const url = organism ? `${API_BASE}/comparative/time-scaled-tree?organism=${encodeURIComponent(organism)}` : `${API_BASE}/comparative/time-scaled-tree`;
    const res = await fetch(url);
    return res.json();
  },

  async getBayesianSkyline(organism?: string) {
    const url = organism ? `${API_BASE}/comparative/bayesian-skyline?organism=${encodeURIComponent(organism)}` : `${API_BASE}/comparative/bayesian-skyline`;
    const res = await fetch(url);
    return res.json();
  },

  async getPanGenomeMatrix(organism?: string) {
    const url = organism ? `${API_BASE}/comparative/pan-genome-matrix?organism=${encodeURIComponent(organism)}` : `${API_BASE}/comparative/pan-genome-matrix`;
    const res = await fetch(url);
    return res.json();
  },

  async getLinearSynteny(organism?: string) {
    const url = organism ? `${API_BASE}/comparative/linear-synteny?organism=${encodeURIComponent(organism)}` : `${API_BASE}/comparative/linear-synteny`;
    const res = await fetch(url);
    return res.json();
  },

  // Plasmids
  async getPlasmidSummary(organism?: string) {
    const url = organism ? `${API_BASE}/plasmids/summary?organism=${encodeURIComponent(organism)}` : `${API_BASE}/plasmids/summary`;
    const res = await fetch(url);
    return res.json();
  },

  async getPlasmidMatrix(organism?: string) {
    const url = organism ? `${API_BASE}/plasmids/matrix?organism=${encodeURIComponent(organism)}` : `${API_BASE}/plasmids/matrix`;
    const res = await fetch(url);
    return res.json();
  },

  async getMobilizationSankey(organism?: string) {
    const url = organism ? `${API_BASE}/plasmids/sankey?organism=${encodeURIComponent(organism)}` : `${API_BASE}/plasmids/sankey`;
    const res = await fetch(url);
    return res.json();
  },

  async getPartitionedHeatmaps(organism?: string) {
    const url = organism ? `${API_BASE}/plasmids/heatmaps?organism=${encodeURIComponent(organism)}` : `${API_BASE}/plasmids/heatmaps`;
    const res = await fetch(url);
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

  async getAlerts(organism?: string) {
    const url = organism ? `${API_BASE}/surveillance/alerts?organism=${encodeURIComponent(organism)}` : `${API_BASE}/surveillance/alerts`;
    const res = await fetch(url);
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
  },

  // AI & Machine Learning Continuous MIC Engine
  async predictMIC(params: { organism: string; isolate_accession?: string; genes?: string[] }) {
    const res = await fetch(`${API_BASE}/ai/predict-mic`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    return (await res.json()) as MICPredictionResponse;
  },

  async copilotChat(query: string, organism: string = 'Klebsiella pneumoniae') {
    const res = await fetch(`${API_BASE}/ai/copilot-chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, organism })
    });
    return (await res.json()) as AICopilotBrief;
  },

  // One Health & Wastewater-Based Epidemiology (WBE)
  async getWastewaterSites() {
    const res = await fetch(`${API_BASE}/one-health/sites`);
    return (await res.json()) as WastewaterSite[];
  },

  async getWBELeadTime(days: number = 45) {
    const res = await fetch(`${API_BASE}/one-health/lead-time?days=${days}`);
    return (await res.json()) as WBELeadTimeResponse;
  },

  async getOneHealthNexus() {
    const res = await fetch(`${API_BASE}/one-health/nexus`);
    return (await res.json()) as OneHealthMatrix;
  },

  async simulateAlert(payload: { site_id: string; pathogen: string; resistance_gene: string; log10_load: number }) {
    const res = await fetch(`${API_BASE}/one-health/simulate-alert`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return (await res.json()) as AlertSimulationResult;
  }
};


