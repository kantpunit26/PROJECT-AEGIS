# PROJECT AEGIS 2.0 — SCIENTIFIC METHODOLOGY

## 1. Scope and Target Organisms

PROJECT AEGIS 2.0 establishes automated surveillance pipelines focused initially on *Klebsiella pneumoniae*, one of the most critical World Health Organization (WHO) and CDC urgent AMR threats. The analytical architecture is designed to generalize to *Escherichia coli*, *Acinetobacter baumannii*, *Salmonella enterica*, *Staphylococcus aureus*, and *Enterococcus faecium*.

---

## 2. Genomic Quality Assessment

Raw read and de novo assembly evaluation follows international standards:
1. **Raw Reads**:
   - `FastQC` and `fastp` adapter trimming, low-quality base filtering ($Q < 20$), and GC distribution analysis.
2. **Assemblies**:
   - `QUAST`: Contig count ($< 500$ contigs for complete draft), total genome length ($5.0 - 5.8$ Mb for *K. pneumoniae*), N50 ($> 50,000$ bp threshold), L50, and GC content ($\sim 57.0 - 57.5\%$).
   - `CheckM2`: Machine learning-based completeness ($> 95\%$) and contamination ($< 5\%$).

---

## 3. Antimicrobial Resistance Determinant Profiling

### 3.1 AMRFinderPlus Integration
AEGIS 2.0 incorporates NCBI AMRFinderPlus to classify:
- **Core AMR Determinants**: Acquired resistance genes (e.g. carbapenemases: *bla*KPC, *bla*NDM, *bla*OXA-48-like, *bla*VIM, *bla*IMP; ESBLs: *bla*CTX-M-15, *bla*SHV-12).
- **Point Mutations**: Chromosomal mutations conferring resistance to fluoroquinolones (GyrA: S83I, S83F; ParC: S80I), colistin (*mgrB* disruptions, *pmrAB*, *phoPQ*), and carbapenems (*ompK35*, *ompK36* porin loss).
- **Stress Response & Virulence Factors**: Heavy metal resistance (copper *pco*, silver *sil*), yersiniabactin (*ybt*), aerobactin (*iuc*), and salmochelin (*iro*).

---

## 4. Molecular Typing & Virulence

1. **Multi-Locus Sequence Typing (MLST)**:
   - 7 housekeeping genes: *gapA*, *infB*, *mdh*, *pgi*, *phoE*, *rpoB*, *tonB*. Sequence types such as ST11, ST14, ST15, ST16, ST23, ST101, ST147, ST258, and ST307 are tracked as high-risk global clones.
2. **Kleborate Virulence Profiling**:
   - Virulence score ($0 - 5$): Presence of yersiniabactin, colibactin, and aerobactin siderophores.
   - Resistance score ($0 - 3$): ESBL, carbapenemase, and colistin resistance presence.
   - Capsule (K-locus, e.g. K1, K2, K64) and LPS (O-locus, e.g. O1, O2, O3b) serotyping.

---

## 5. Comparative Genomics & Core-Genome SNPs

1. **Reference Selection**: Curated reference genomes (e.g., *K. pneumoniae* HS11286 or MGH 78578).
2. **SNP Calling**: Identification of high-confidence biallelic core-genome single nucleotide polymorphisms, masking repetitive elements, mobile elements, and phage regions.
3. **Distance Matrix**: Symmetrical pairwise Hamming/Manhattan distance matrix calculation:
   $$D_{ij} = \sum_{k=1}^{L_{\text{core}}} \mathbb{I}(S_{ik} \ne S_{jk})$$
   Thresholds: $\le 10 - 15$ SNPs frequently indicate epidemiologically linked hospital transmission chains.

---

## 6. Maximum-Likelihood Phylogenetics

1. **Model Selection**: ModelFinder evaluates candidate nucleotide substitution models (GTR+G, GTR+I+G, TVM+F+R4) using Bayesian Information Criterion (BIC).
2. **IQ-TREE Tree Search**: High-performance maximum likelihood optimization with 1,000 Ultrafast Bootstrap replicates (`-B 1000`) and SH-aLRT test (`-alrt 1000`).
3. **Phylogenetic Interpretation**: Trees are exported as standardized Newick strings annotated with lineage and resistance attributes. Proximity in a phylogenetic tree represents evolutionary relatedness, not definitive direct transmission.

---

## 7. Plasmid Reconstruction & MOB-Suite Characterization

1. **MOB-recon**: Disentangles chromosomal vs. extrachromosomal (plasmid) contigs based on replicon signatures, relaxases, and mating pair formation (MPF) genes.
2. **MOB-typer**:
   - Replicon typing (IncFII, IncFIA, IncFIB, IncX3, IncA/C, IncL/M, ColRNAI).
   - Mobility classification: Conjugative, Mobilizable, or Non-mobilizable.
   - Contextual mapping of carbapenemases (e.g., *bla*NDM-5 on IncX3, *bla*KPC-2 on IncFII).

---

## 8. Genotype-to-Phenotype Susceptibility Concordance

AEGIS 2.0 pairs Minimum Inhibitory Concentration (MIC) laboratory testing with genetic resistance predictions using CLSI M100 and EUCAST breakpoints.
Metrics computed:
$$\text{Sensitivity} = \frac{TP}{TP + FN}, \quad \text{Specificity} = \frac{TN}{TN + FP}$$
$$\text{Precision (PPV)} = \frac{TP}{TP + FP}, \quad \text{Concordance Rate} = \frac{TP + TN}{N}$$
Very Major Errors (VME: false susceptibility / false negative) and Major Errors (ME: false resistance / false positive) are tracked independently.

---

## 9. Deterministic SEIR Epidemiological Modelling

An extended compartmental model for hospital-associated bacterial transmission and colonization:
$$\frac{dS}{dt} = \Lambda - \beta \frac{S (I + \theta C)}{N} - \mu S$$
$$\frac{dC}{dt} = \beta \frac{S (I + \theta C)}{N} - (\alpha + \gamma_c + \mu) C + \delta_{treat} I$$
$$\frac{dI}{dt} = \alpha C - (\gamma_i + \delta_{treat} + \mu + d) I$$
$$\frac{dR}{dt} = \gamma_c C + \gamma_i I - \mu R$$

Where:
- $S$: Susceptible population
- $C$: Asymptomatically colonized individuals (subclinical carriers)
- $I$: Clinically infected individuals exhibiting symptoms
- $R$: Cleared / Recovered population
- $\beta$: Transmission coefficient
- $\theta$: Relative infectiousness of colonized vs. infected individuals
- $\alpha$: Rate of progression from colonization to active infection
- $\delta_{treat}$: Antibiotic exposure / treatment response
- $R_0$: Basic reproduction number calculated via next-generation matrix method.

