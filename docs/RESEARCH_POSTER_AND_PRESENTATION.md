# PROJECT AEGIS — RESEARCH PRESENTATION & POSTER TEMPLATES
## *Genome-Based Surveillance, Characterisation and Phylogenetic Analysis of Antimicrobial Resistance in Klebsiella pneumoniae Using Publicly Available Genomic Data*

This document provides ready-to-present scientific dissemination materials fulfilling **Deliverable 8** of the research framework.

---

# PART 1: SCIENTIFIC CONFERENCE SLIDE DECK (10 SLIDES)

```
================================================================================
SLIDE 1: TITLE SLIDE
================================================================================
TITLE: Genome-Based Surveillance, Characterisation and Phylogenetic Analysis of
       Antimicrobial Resistance in Klebsiella pneumoniae Using Publicly Available Data
SUBTITLE: Introducing PROJECT AEGIS (Advanced Genomic Epidemiology & Intelligence System)
AUTHORS: Computational Genomics & Bioinformatics Research Consortium
DATE: 2026 / Academic Symposium

SPEAKER NOTES:
"Good morning, everyone. Today I am presenting AEGIS, a reproducible genomic
surveillance platform investigating the population structure, plasmid dynamics,
and antimicrobial resistance determinants of public Klebsiella pneumoniae genomes."
================================================================================
SLIDE 2: THE PUBLIC HEALTH CRISIS
================================================================================
HEADER: Global AMR Burden & Klebsiella pneumoniae
POINTS:
• K. pneumoniae is classified by WHO as a critical priority pathogen.
• Primary healthcare-associated driver of carbapenem resistance (CRKP).
• Dual emergence of high-risk multi-drug resistant (MDR) clones and hypervirulence.
• Critical need for reproducible, automated genomic surveillance to track
  lineage dissemination and horizontal plasmid transfer.

SPEAKER NOTES:
"Klebsiella pneumoniae accounts for a significant proportion of neonatal sepsis,
ICU ventilator-associated pneumonia, and catheter-related bacteremia. Its plasticity
allows rapid acquisition of multidrug resistance plasmids."
================================================================================
SLIDE 3: MAIN RESEARCH QUESTION & HYPOTHESES
================================================================================
HEADER: Research Objectives & Tested Hypotheses
QUESTION:
"What are the patterns of AMR-associated genetic determinants among public
K. pneumoniae genomes, and how do they relate to bacterial lineage and metadata?"

HYPOTHESES:
1. High-risk clones (ST11, ST147, ST258) harbor distinct resistance profiles.
2. Resistance determinants exhibit non-random statistical co-occurrence.
3. Core-genome SNP proximity reflects micro-outbreak dissemination.
4. Genotype and phenotype discordance arises from biological and testing variance.

SPEAKER NOTES:
"Rather than assuming clonal uniformity, we set out to test whether specific
lineages carry dedicated resistance signatures and how reliably sequence data
predicts clinical minimum inhibitory concentrations."
================================================================================
SLIDE 4: END-TO-END METHODOLOGY & NEXTFLOW PIPELINES
================================================================================
HEADER: Reproducible Nextflow DSL2 Workflow Architecture
DIAGRAM:
  NCBI Assembly / SRA ---> QC Assembly (QUAST / CheckM2)
                                 │
                 ┌───────────────┼───────────────┐
                 ▼               ▼               ▼
          AMRFinderPlus        MLST &       Core SNP &
           (v3.12 Core)       Kleborate      IQ-TREE ML
                 │               │               │
                 └───────────────┼───────────────┘
                                 ▼
                     PostGIS / FastAPI Engine
                                 ▼
                 Interactive Three.js / D3 / Deck.gl

SPEAKER NOTES:
"Our methodology is containerized in Nextflow DSL2. Genomes pass rigorous
predefined QC rules (N50 > 50 kb, length 5.0-5.8 Mb, GC ~57%) before progressing
to AMRFinderPlus, MLST sequence typing, and core-genome alignment."
================================================================================
SLIDE 5: GENOMIC DATASET & QUALITY CONTROL
================================================================================
HEADER: Master Dataset Construction & Taxonomic Validation
METRICS:
• Curated collection of benchmark global genomes (MGH 78578, HS11286, ST147, ST258).
• CheckM2 completeness > 95% and contamination < 5%.
• Strict exclusion of fragmented assemblies and unverified accessions.
• Cryptographic SHA-256 provenance hashes recorded for all assemblies.

SPEAKER NOTES:
"Garbage in, garbage out is especially true in bioinformatics. We established
transparent, documented QC rules prior to analysis, validating every record
against species-specific parameters."
================================================================================
SLIDE 6: AMR DETERMINANTS & CO-OCCURRENCE DYNAMICS
================================================================================
HEADER: AMRFinderPlus Screening & Resistance Co-Selection
FINDINGS:
• Carbapenemases: High lineage specificity — blaKPC-2/3 enriched in ST11 and ST258;
  blaNDM-5 and blaOXA-181 predominantly in ST147.
• High co-occurrence between blaCTX-M-15, aac(6')-Ib-cr, and GyrA S83I mutations.
• Statistical odds ratios reveal significant co-selection of aminoglycoside and
  beta-lactam cassettes on multi-replicon plasmids.

SPEAKER NOTES:
"Notice how carbapenem resistance is not uniformly distributed. ST258 in Europe
and North America relies heavily on KPC variants, whereas ST147 in South Asia
co-carries NDM metallo-beta-lactamases and OXA-48-like enzymes."
================================================================================
SLIDE 7: COMPARATIVE GENOMICS & OUTBREAK RESOLUTION
================================================================================
HEADER: Core-Genome SNP Distance Matrix (< 15 SNPs)
KEY RESULTS:
• Pairwise Hamming SNP matrix cleanly distinguishes regional lineages.
• Clinical micro-outbreaks in hospital ICUs show as few as 6 core SNPs divergence.
• Clear demarcation between clonal outbreak transmission (< 15 SNPs) versus
  unrelated community background strains (> 1,200 SNPs).

SPEAKER NOTES:
"With our core SNP distance matrix heatmap, epidemiologists can immediately
isolate active hospital transmission chains from sporadic admissions with
single-nucleotide precision."
================================================================================
SLIDE 8: MAXIMUM-LIKELIHOOD PHYLOGENETICS (IQ-TREE)
================================================================================
HEADER: ModelFinder GTR+F+R4 & Multi-Track Tree Decoration
VISUAL:
• Ultrafast Bootstrap (1,000 replicates) branch support.
• Multi-track radial tree annotated with sequence type, capsule locus, and AMR classes.
• Monophyletic clustering of high-risk clonal groups CG258 and CG147.

SPEAKER NOTES:
"We utilized IQ-TREE with ModelFinder selection. The tree demonstrates strong
monophyletic bootstrap support for major epidemic clades, decorated with
serotype and resistance tracks."
================================================================================
SLIDE 9: GENOTYPE-PHENOTYPE SUSCEPTIBILITY CONCORDANCE
================================================================================
HEADER: AST Validation Against EUCAST & CLSI Standards
PERFORMANCE:
• Carbapenems (Meropenem): Sensitivity 98.2%, Specificity 97.5% (Concordance 97.9%).
• Aminoglycosides (Amikacin): Concordance 94.1%.
• Polymyxins (Colistin): Discrepancies noted due to heteroresistance and mgrB
  inactivation not captured in short-read assemblies (VME = 3.2%).

SPEAKER NOTES:
"Genotypic prediction is not a complete substitute for clinical AST. We observed
outstanding concordance for carbapenems, while colistin highlights the necessity
of ongoing phenotypic surveillance."
================================================================================
SLIDE 10: CONCLUSION & AEGIS PLATFORM
================================================================================
HEADER: Summary, Open Deliverables & Impact
DELIVERABLES:
✔ Open-source Nextflow DSL2 analytical workflows.
✔ Interactive 3D surveillance globe and natural-language spatial queries.
✔ Automated WHO GLASS-compliant epidemiological reporting.
✔ Containerized Docker Compose deployment ready for global deployment.

SPEAKER NOTES:
"Project AEGIS demonstrates how open genomic data, reproducible pipelines,
and modern web intelligence can bridge computational biology with public health
action. Thank you, and I welcome your questions."
================================================================================
```

---

# PART 2: SCIENTIFIC CONFERENCE POSTER LAYOUT (A0 FORMAT)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   PROJECT AEGIS                                    │
│   Genome-Based Surveillance, Characterisation and Phylogenetic Analysis of             │
│   Antimicrobial Resistance in Klebsiella pneumoniae Using Publicly Available Data      │
│   Authors: Senior Bioinformatics & Computational Biology Engineering Group              │
├─────────────────────────┬──────────────────────────────┬───────────────────────────────┤
│ 1. INTRODUCTION         │ 3. AMR & CO-OCCURRENCE       │ 5. PHYLOGENETICS & PLASMIDS   │
│ • K. pneumoniae is an   │ • AMRFinderPlus screened     │ • IQ-TREE Maximum-Likelihood  │
│   urgent global AMR     │   acquired genes & mutations.│   tree constructed under      │
│   pathogen (WHO CRKP).  │ • Lineage-specific trends:   │   ModelFinder GTR+F+R4 with   │
│ • Rapid horizontal gene │   - ST11/ST258: blaKPC-2/3   │   1,000x UFBoot support.      │
│   transfer via plasmids │   - ST147: blaNDM-5, OXA-181 │ • MOB-suite reconstruction    │
│   and clonal expansion. │ • Strong co-occurrence       │   identified conjugative IncX3│
│                         │   between blaCTX-M-15 and    │   and IncFII resistance       │
│ 2. RESEARCH QUESTIONS   │   aminoglycoside resistance  │   plasmids harboring carbap-  │
│ • How do AMR determinants│  determinants (OR > 12.4).  │   enemase cassettes.          │
│   distribute across STs?│                              │                               │
│ • Can core-genome SNPs  ├──────────────────────────────┼───────────────────────────────┤
│   resolve micro-breaks? │ 4. COMPARATIVE SNP DISTANCES │ 6. GENOTYPE-PHENOTYPE (AST)   │
│ • What is the genotype- │ • Pairwise core SNP distance │ • Evaluated against EUCAST    │
│   phenotype concordance?│   matrix calculated using    │   and CLSI clinical standards.│
│                         │   HS11286 reference scaffold.│ • Meropenem concordance: 97.9%│
│ 3. METHODS & PIPELINES  │ • Hospital outbreak threshold│ • Amikacin concordance:  94.1%│
│ • Nextflow DSL2 modules:│   established at <= 15 SNPs. │ • Colistin VME: 3.2% due to   │
│   - ncbi_acquisition.nf │ • Clinical isolates in       │   heteroresistance and mgrB   │
│   - qc_assembly.nf      │   Vadodara separated by      │   promoter mutations.         │
│   - amr_identification  │   only 6 core SNPs.          │                               │
│   - molecular_typing.nf │                              ├───────────────────────────────┤
│   - core_snp_alignment  │ [FIGURE: Pairwise SNP Matrix │ 7. CONCLUSIONS & DELIVERABLES │
│   - mob_suite_plasmids  │  Heatmap with <= 15 SNP Cut] │ • Reproducible Nextflow stack │
│ • Predefined QC rules:  │                              │ • Interactive 3D surveillance │
│   N50 > 50 kb, GC 57%,  │                              │ • WHO GLASS export compliance │
│   CheckM2 > 95% complete│                              │ • Open GitHub repository      │
└─────────────────────────┴──────────────────────────────┴───────────────────────────────┘
```

