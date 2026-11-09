# PROJECT AEGIS — DATA DICTIONARY

This document defines the core relational database schema, entities, fields, data types, and constraints in the AEGIS platform.

---

## 1. Entity: `isolates`
Primary registry of biological isolates, samples, and high-level surveillance records.

| Field | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID / String | No | Primary Key |
| `accession` | String(64) | No | NCBI or internal unique accession (e.g., GCA_000000000.1) |
| `sample_id` | String(128) | Yes | BioSample or clinical lab identifier |
| `organism` | String(128) | No | Taxon name (e.g., *Klebsiella pneumoniae*) |
| `taxon_id` | Integer | Yes | NCBI Taxonomy ID (e.g., 573) |
| `strain` | String(128) | Yes | Strain or isolate name |
| `collection_date`| Date | Yes | Exact collection date (YYYY-MM-DD) |
| `collection_year`| Integer | Yes | Extracted collection year |
| `isolation_source`| String(128) | Yes | Clinical anatomical site (e.g., Blood, Sputum, Urine, Rectal Swab) |
| `host` | String(64) | Yes | Host organism (e.g., *Homo sapiens*) |
| `country` | String(64) | Yes | Country of origin (ISO-3166 or name) |
| `state_province` | String(64) | Yes | Sub-national administrative region |
| `city` | String(64) | Yes | City or district |
| `latitude` | Float | Yes | Decimal latitude (-90.0 to +90.0) |
| `longitude` | Float | Yes | Decimal longitude (-180.0 to +180.0) |
| `assembly_level` | String(32) | Yes | Complete Genome, Chromosome, Scaffold, Contig |
| `genome_size` | BigInteger | Yes | Total base pairs in assembly |
| `gc_percent` | Float | Yes | GC content percentage (0.0 to 100.0) |
| `n50` | Integer | Yes | Assembly N50 metric |
| `contig_count` | Integer | Yes | Number of contigs |
| `qc_status` | String(16) | No | PASS, WARNING, FAIL |
| `checksum_sha256`| String(64) | Yes | Cryptographic hash of input FASTA/FASTQ |
| `provenance_source`| String(64) | Yes | NCBI_DATASETS, NCBI_PATHOGEN_DETECTION, SRA, LOCAL_UPLOAD |
| `created_at` | DateTime | No | Record creation timestamp |
| `updated_at` | DateTime | No | Last update timestamp |

---

## 2. Entity: `amr_determinants`
Resistance genes, gene variants, and resistance-conferring point mutations identified by AMRFinderPlus.

| Field | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID / String | No | Primary Key |
| `isolate_id` | UUID / String | No | Foreign Key -> `isolates.id` |
| `gene_symbol` | String(64) | No | Standardized symbol (e.g., *bla*KPC-2, *mcr-1.1*, *aac(6')-Ib-cr*) |
| `gene_family` | String(64) | Yes | Functional gene family (e.g., Carbapenemase, ESBL, Colistin) |
| `drug_class` | String(64) | No | Target class (e.g., Beta-lactam, Aminoglycoside, Polymyxin) |
| `subclass` | String(64) | Yes | Carbapenem, Cephalosporin, Fluoroquinolone |
| `element_type` | String(32) | No | `GENE` or `POINT_MUTATION` |
| `mutation_name` | String(64) | Yes | Amino acid change (e.g., GyrA_S83I) |
| `confidence` | String(16) | Yes | EXACT, BLAST_MATCH, PARTIAL |
| `contig_id` | String(128) | Yes | Contig identifier from assembly |
| `start_coord` | Integer | Yes | 1-based start nucleotide position |
| `end_coord` | Integer | Yes | 1-based end nucleotide position |
| `strand` | String(1) | Yes | `+` or `-` |
| `predicted_context`| String(32) | Yes | CHROMOSOME, PLASMID, UNKNOWN |
| `tool_version` | String(32) | Yes | Software version (e.g., AMRFinderPlus v3.12.8) |
| `db_version` | String(32) | Yes | AMRFinder database release version |

---

## 3. Entity: `molecular_types`
MLST and Kleborate virulence/capsule serotype predictions.

| Field | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID / String | No | Primary Key |
| `isolate_id` | UUID / String | No | Foreign Key -> `isolates.id` |
| `scheme` | String(32) | No | PASTEUR, OXFORD, etc. |
| `sequence_type` | String(32) | No | Sequence type designation (e.g., ST11, ST258) |
| `allelic_profile`| JSON | Yes | Dict of housekeeping alleles (*gapA*, *infB*, etc.) |
| `kleborate_virulence_score` | Integer | Yes | Siderophore index (0 to 5) |
| `kleborate_resistance_score` | Integer | Yes | Resistance determinant index (0 to 3) |
| `k_locus` | String(32) | Yes | Predicted capsule locus (e.g., KL64, KL102) |
| `wzi_allele` | String(32) | Yes | Wzi capsular marker allele |
| `o_locus` | String(32) | Yes | Predicted O-antigen serotype (e.g., O1v1, O2v2) |

---

## 4. Entity: `ast_records`
Antimicrobial Susceptibility Testing (AST) experimental measurements.

| Field | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID / String | No | Primary Key |
| `isolate_id` | UUID / String | No | Foreign Key -> `isolates.id` |
| `antibiotic` | String(64) | No | Antimicrobial agent name (e.g., Meropenem) |
| `mic_value` | Float | Yes | Minimum inhibitory concentration numerical value |
| `mic_operator` | String(2) | Yes | `<=`, `>=`, `==`, `<`, `>` |
| `mic_unit` | String(16) | Yes | `mg/L`, `ug/mL` |
| `phenotype` | String(16) | No | `S` (Susceptible), `I` (Intermediate), `R` (Resistant) |
| `standard` | String(16) | No | `CLSI`, `EUCAST` |
| `standard_version`| String(32) | Yes | Guideline publication year/version (e.g., M100-ED34) |
| `testing_method`| String(64) | Yes | Broth microdilution, E-test, Vitek 2, Disk diffusion |
| `genotype_concordance` | String(16) | Yes | `CONCORDANT`, `MAJOR_ERROR`, `VERY_MAJOR_ERROR` |

---

## 5. Entity: `plasmids`
Extrachromosomal element reconstructions and replicon typing results.

| Field | Type | Nullable | Description |
|---|---|---|---|
| `id` | UUID / String | No | Primary Key |
| `isolate_id` | UUID / String | No | Foreign Key -> `isolates.id` |
| `plasmid_id` | String(64) | No | Contig cluster ID or reconstructed plasmid ID |
| `cluster_id` | String(64) | Yes | MOB-suite cluster identifier |
| `replicon_types`| JSON / Array | Yes | Incompatibility groups (e.g., ["IncFII", "IncFIB"]) |
| `relaxase_type` | String(32) | Yes | MOB relaxase family (e.g., MOBF, MOBP, MOBH) |
| `mpf_type` | String(32) | Yes | Mating pair formation type (e.g., MPF_T, MPF_F) |
| `mobility` | String(32) | No | `CONJUGATIVE`, `MOBILIZABLE`, `NON_MOBILIZABLE` |
| `predicted_length`| Integer | Yes | Approximate plasmid length in base pairs |
| `associated_amr_genes` | JSON / Array | Yes | Resistance genes physically situated on plasmid |

---

## 6. Entity: `snp_matrices` & `phylogenetic_trees`
High-dimensional comparative genomics and evolutionary tree records.

| Entity | Key Attributes | Description |
|---|---|---|
| `snp_analyses` | `id`, `reference_genome`, `total_core_positions`, `isolate_count`, `matrix_json` | Pairwise SNP distance matrix and core alignment metadata |
| `phylogenetic_trees` | `id`, `tree_name`, `newick_string`, `model_selected`, `log_likelihood`, `bootstrap_reps` | Maximum-likelihood Newick trees from IQ-TREE |

---

## 7. Entity: `epidemiological_scenarios` & `alerts`
Dynamic surveillance projections and outbreak alerts.

| Entity | Key Attributes | Description |
|---|---|---|
| `modelling_scenarios`| `id`, `model_type`, `parameters_json`, `trajectory_json`, `r0`, `peak_infected` | SEIR numerical integration outputs |
| `surveillance_alerts`| `id`, `alert_type`, `severity`, `title`, `message`, `cluster_isolates`, `acknowledged` | Outbreak warnings and Slack/Discord notifications |

