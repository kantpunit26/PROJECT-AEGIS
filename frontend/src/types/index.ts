export interface Isolate {
  id: string;
  accession: string;
  sample_id?: string;
  organism: string;
  taxon_id?: number;
  strain?: string;
  collection_date?: string;
  collection_year?: number;
  isolation_source?: string;
  host?: string;
  country?: string;
  state_province?: string;
  city?: string;
  latitude?: number;
  longitude?: number;
  assembly_level?: string;
  genome_size?: number;
  gc_percent?: number;
  n50?: number;
  contig_count?: number;
  qc_status: 'PASS' | 'WARNING' | 'FAIL';
  qc_notes?: string;
  checksum_sha256?: string;
  provenance_source?: string;
  created_at: string;
  updated_at: string;
  amr_count?: number;
  sequence_type?: string;
}

export interface AMRDeterminant {
  id: string;
  isolate_id: string;
  gene_symbol: string;
  gene_family?: string;
  drug_class: string;
  subclass?: string;
  element_type: string;
  mutation_name?: string;
  confidence: string;
  predicted_context: string;
  contig_id?: string;
}

export interface MLSTDistributionItem {
  sequence_type: string;
  count: number;
  percentage: number;
  predominant_carbapenemase?: string;
}

export interface ASTRecord {
  id: string;
  isolate_id: string;
  antibiotic: string;
  mic_value?: number;
  mic_unit: string;
  phenotype: 'S' | 'I' | 'R';
  standard: string;
  genotypic_prediction?: string;
  concordance_status?: string;
}

export interface ASTConcordanceMetrics {
  antibiotic: string;
  total_tested: number;
  true_positive_resistant: number;
  true_negative_susceptible: number;
  major_error_false_resistant: number;
  very_major_error_false_susceptible: number;
  sensitivity: number;
  specificity: number;
  precision_ppv: number;
  concordance_rate: number;
  confusion_matrix?: {
    predicted_resistant: { actual_resistant: number; actual_susceptible: number };
    predicted_susceptible: { actual_resistant: number; actual_susceptible: number };
  };
}

export interface SNPMatrixData {
  id: string;
  analysis_name: string;
  reference_genome: string;
  isolate_count: number;
  accessions: string[];
  distance_matrix: number[][];
  total_core_positions: number;
  filtered_snp_count: number;
}

export interface PhylogeneticTreeData {
  id: string;
  tree_name: string;
  organism: string;
  newick_string: string;
  substitution_model: string;
  log_likelihood?: number;
  bootstrap_replicates: number;
  metadata_tracks?: Record<string, Record<string, string | number>>;
}

export interface SpatialCluster {
  id: string;
  latitude: number;
  longitude: number;
  accession: string;
  organism: string;
  sequence_type?: string;
  carbapenemases: string[];
  colistin_genes: string[];
  country?: string;
  city?: string;
  collection_year?: number;
  qc_status: string;
  distance_km?: number;
}

export interface SurveillanceAlert {
  id: string;
  alert_type: string;
  severity: 'INFO' | 'WARNING' | 'HIGH' | 'CRITICAL';
  title: string;
  message: string;
  organism: string;
  region?: string;
  cluster_size?: number;
  isolate_accessions?: string[];
  acknowledged: boolean;
  created_at: string;
}

export interface SEIRSimulationResult {
  days: number[];
  susceptible: number[];
  colonized: number[];
  infected: number[];
  recovered: number[];
  r0: number;
  effective_re: number[];
  peak_infected_count: number;
  peak_day: number;
  total_colonization_incidence: number;
}

export interface CircularAtlasBin {
  bin_index: number;
  position: number;
  gc_content: number;
  gc_skew: number;
  cds_fwd: boolean;
  cds_rev: boolean;
  amr?: { name: string; mechanism: string; drug_class: string; type: string };
  virulence?: { name: string; function: string; locus: string };
  mge?: { name: string; type: string };
  blast_clades: {
    clade_1_st258: number;
    clade_2_st11: number;
    clade_3_st147: number;
    clade_4_st15: number;
    clade_5_st307: number;
  };
}

export interface CircularAtlasHotspot {
  id: string;
  label: string;
  position_bp: number;
  bin_index: number;
  category: string;
  description: string;
}

export interface CircularAtlasData {
  organism: string;
  strain: string;
  genome_size: number;
  gc_mean: number;
  total_bins: number;
  bins: CircularAtlasBin[];
  hotspots: CircularAtlasHotspot[];
}

export interface MSTNode {
  id: string;
  label: string;
  sequence_type: string;
  isolate_count: number;
  carbapenemase?: string;
  virulence_score?: number;
  sources: Record<string, number>;
  cluster: string;
  x: number;
  y: number;
  radius: number;
}

export interface MSTEdge {
  source: string;
  target: string;
  snp_distance: number;
  outbreak_link: boolean;
}

export interface MSTData {
  title: string;
  method: string;
  nodes: MSTNode[];
  edges: MSTEdge[];
  outbreak_halos: {
    name: string;
    center_x: number;
    center_y: number;
    radius_x: number;
    radius_y: number;
    snp_threshold: string;
    color: string;
  }[];
}

export interface TimeScaledLeaf {
  id: string;
  label: string;
  ward: string;
  date: string;
  y: number;
  x: number;
  hpd_low: number;
  hpd_high: number;
  clade: string;
  is_hcw?: boolean;
}

export interface TimeScaledTreeData {
  title: string;
  model: string;
  mean_clock_rate: string;
  tmrca: string;
  timeline: { year: string; pos: number }[];
  leaves: TimeScaledLeaf[];
  internal_nodes: {
    id: string;
    x: number;
    y: number;
    hpd_low: number;
    hpd_high: number;
    posterior?: number;
    label?: string;
  }[];
  tree_lines: { x1: number; y1: number; x2: number; y2: number }[];
  wards_legend: { ward: string; color: string }[];
}

export interface SkylineClade {
  clade_id: string;
  name: string;
  color: string;
  years: number[];
  median_ne: number[];
  lower_hpd: number[];
  upper_hpd: number[];
  peak_year: number;
  notes: string;
}

export interface BayesianSkylineData {
  title: string;
  y_axis_label: string;
  x_axis_label: string;
  clades: SkylineClade[];
}

export interface PanGenomeTaxon {
  id: string;
  strain: string;
  year: number;
  city: string;
  mlst: string;
  clade: string;
  carb: string;
}

export interface PanGenomeMatrixData {
  title: string;
  taxa: PanGenomeTaxon[];
  arg_headers: string[];
  arg_matrix: boolean[][];
  inc_headers: string[];
  inc_matrix: boolean[][];
  vir_headers: string[];
  vir_matrix: boolean[][];
}

export interface SyntenyGene {
  name: string;
  label?: string;
  start: number;
  end: number;
  strand: '+' | '-';
  type: 'ARG' | 'MGE' | 'OTHER';
  color: string;
}

export interface SyntenyLocus {
  id: string;
  name: string;
  length_bp: number;
  host_context: string;
  target_site_duplication: string;
  flanking_repeats: { left: string; right: string };
  genes: SyntenyGene[];
}

export interface LinearSyntenyData {
  title: string;
  reference_standard: string;
  loci: SyntenyLocus[];
}

export interface SankeyNode {
  id: string;
  name: string;
  stage: number;
  color: string;
}

export interface SankeyLink {
  source: string;
  target: string;
  value: number;
}

export interface MobilizationSankeyData {
  title: string;
  nodes: SankeyNode[];
  links: SankeyLink[];
}

export interface PartitionedResistomeGene {
  name: string;
  drug_class: string;
  mechanism: string;
  class_color: string;
}

export interface PartitionedResistomeData {
  title: string;
  isolates: string[];
  chromosomal: {
    genes: PartitionedResistomeGene[];
    matrix: number[][];
  };
  plasmid: {
    genes: PartitionedResistomeGene[];
    matrix: number[][];
  };
}

