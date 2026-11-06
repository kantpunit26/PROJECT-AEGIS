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
