# PROJECT AEGIS 2.0
### Advanced Genomic Epidemiology & Intelligence System

[![Platform](https://img.shields.io/badge/Platform-AEGIS%202.0-8B0000.svg)](https://github.com/aegis-surveillance/aegis-2.0)
[![Target-Organism](https://img.shields.io/badge/Primary%20Organism-Klebsiella%20pneumoniae-2E8B57.svg)]()
[![Stack](https://img.shields.io/badge/Stack-FastAPI%20|%20React%20|%20PostgreSQL%20PostGIS%20|%20Deck.gl-blue.svg)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey.svg)]()

---

## 1. Executive Summary

**PROJECT AEGIS 2.0** is an enterprise research-grade genomic epidemiology and antimicrobial resistance (AMR) intelligence platform. Designed from zero for molecular epidemiologists, computational biologists, and public health agencies, AEGIS 2.0 bridges raw high-throughput pathogen sequencing with spatial-temporal outbreak analytics, comparative genomics, plasmid reconstruction, and deterministic transmission modelling.

Initially focused on high-priority multi-drug resistant (MDR) and extensively drug-resistant (XDR) ***Klebsiella pneumoniae***, the architecture scales across the ESCAPE pathogens (*Enterococcus faecium*, *Staphylococcus aureus*, *Klebsiella pneumoniae*, *Acinetobacter baumannii*, *Pseudomonas aeruginosa*, *Enterobacter* spp.) and *Salmonella enterica*.

---

## 2. Core Capabilities

1. **NCBI Genomic Data Acquisition & SRA Pipelines**
   - Automated accession resolution, checksum verification, FASTQ/FASTA retrieval from NCBI Datasets, Entrez, Pathogen Detection, and SRA.
   - Comprehensive extraction of clinical isolation sources, collection dates, geographic provenance, and AST metadata.
2. **Genome Assembly Quality Control**
   - Read-level QC via `fastp`/`FastQC`, assembly QC via `QUAST` (N50, L50, contig count, genome size), and completeness/contamination heuristics via `CheckM2`.
3. **AMR Determinant Identification**
   - Rigorous NCBI `AMRFinderPlus` integration detecting carbapenemases (*bla*KPC, *bla*NDM, *bla*OXA-48-like, *bla*VIM, *bla*IMP), ESBLs (*bla*CTX-M, *bla*SHV, *bla*TEM), colistin resistance (*mcr-1* through *mcr-10*, *mgrB* mutations), fluoroquinolone mutations (*gyrA*, *parC*), aminoglycoside modifying enzymes, and efflux mechanisms.
4. **Molecular Typing & Lineage Classification**
   - 7-gene Pasteur and Oxford MLST sequence typing.
   - Deep *K. pneumoniae* capsule (K-type/wzi) and lipopolysaccharide (O-type) virulence profiling via *Kleborate*.
5. **Comparative Genomics & Core-Genome SNP Analysis**
   - Reference-guided core-genome alignment, variant calling, and filtered pairwise SNP distance matrix generation.
6. **Maximum-Likelihood Phylogenetics**
   - ModelFinder substitution matrix optimization, high-performance IQ-TREE phylogenetic inference, Ultrafast Bootstrap branch support, and multi-track metadata integration.
7. **Plasmid Reconstruction & Replicon Characterization**
   - MOB-suite (`MOB-recon`, `MOB-typer`) replicon family typing (IncF, IncX, IncA/C, ColRNAI), relaxase MOB typing, mating pair apparatus profiling, and AMR chromosome-vs-plasmid partitioning.
8. **Genotype vs. Phenotype Concordance Validation**
   - Clinical MIC record validation against CLSI and EUCAST interpretive standards, generating true/false positive/negative rates, sensitivity, specificity, and confusion matrices.
9. **Geospatial Genomic Surveillance & 3D Analytics**
   - PostgreSQL/PostGIS spatial index engine with Deck.gl and Three.js 3D interactive globe.
   - Safe parameterized natural language query translation for outbreak proximity queries.
10. **Deterministic Epidemiological Modelling (SEIR-Extended)**
    - Runge-Kutta numerical differential equation solver with hospital colonization, antibiotic pressure, and basic/effective reproduction numbers ($R_0, R_e$).
11. **Surveillance Alerting & WHO GLASS Reporting**
    - Slack/Discord automated outbreak webhooks and standardized export formats (CSV, JSON, GeoJSON, Newick, PDF, WHO GLASS).

---

## 3. Technology Architecture

```
                    +------------------------------------+
                    |        PROJECT AEGIS 2.0           |
                    |   Scientific UI (React + Vite)     |
                    |  Three.js Globe / Deck.gl / D3.js  |
                    +-----------------+------------------+
                                      | HTTP / REST API (OpenAPI 3.1)
                                      v
                    +-----------------+------------------+
                    |       FastAPI REST Service         |
                    |   Pydantic V2 Validation Layer     |
                    +--------+------------------+--------+
                             |                  |
            SQLAlchemy 2.0   |                  | Asynchronous Tasks
            + PostGIS        v                  v (Celery + Redis)
+-------------------------------+   +-------------------------------+
|     PostgreSQL 16 + PostGIS   |   |     Redis 7 Task Broker       |
|  - Spatial Coordinates & GIST |   +---------------+---------------+
|  - Normalized Genomic Schema  |                   |
+-------------------------------+                   v
                                    +-------------------------------+
                                    |     Bioinformatics Worker     |
                                    | Nextflow / AMRFinder / IQ-TREE|
                                    +-------------------------------+
```

---

## 4. Quick Start (Production via Docker)

Ensure Docker Desktop (with WSL2 on Windows or native Docker on Linux) is running:

```bash
# Clone and enter directory
cd AEGIS-2.0

# Copy environment variables
cp .env.example .env

# Launch complete platform
docker compose up --build -d
```

Access the interfaces:
- **Scientific Surveillance UI**: [http://localhost:3000](http://localhost:3000)
- **FastAPI Interactive Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Health Endpoint**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 5. Local Development Mode

If running standalone without Docker:

```bash
# 1. Setup Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 2. Setup Frontend
cd ../frontend
npm install
npm run dev
```

---

## 6. Scientific Documentation Index

- [Architecture Design](docs/ARCHITECTURE.md)
- [Scientific Methodology & Pipeline Reference](docs/SCIENTIFIC_METHODOLOGY.md)
- [Data Dictionary & Genomic Schema](docs/DATA_DICTIONARY.md)
- [REST API Specification](docs/API_DOCUMENTATION.md)
- [Security & Provenance](docs/SECURITY.md)
- [Backup and Disaster Recovery](docs/BACKUP_AND_RESTORE.md)
- [Troubleshooting & Diagnostics](docs/TROUBLESHOOTING.md)
- [Changelog](docs/CHANGELOG.md)

---
*AEGIS 2.0 is developed under scientific reproducibility and open computational epidemiology standards.*

