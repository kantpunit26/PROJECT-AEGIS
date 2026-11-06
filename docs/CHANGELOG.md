# PROJECT AEGIS 2.0 — CHANGELOG

## [2.0.0] - Initial Release (Greenfield)

### Added
- **Core Architecture**:
  - Full modular monorepo layout (`backend`, `frontend`, `bioinformatics`, `deploy`, `docs`, `data`).
  - Docker Compose foundation with PostGIS, Redis, Celery, FastAPI, and React frontend.
- **Backend & Database**:
  - FastAPI application structure with OpenAPI 3.1 schema.
  - SQLAlchemy models for Isolates, AMR Determinants, Molecular Types, AST Records, Plasmids, SNP Matrices, and Alerts.
  - PostGIS spatial query support with fallback development SQLite mode.
- **Bioinformatics Engine**:
  - NCBI acquisition pipeline with checksum verification.
  - AMRFinderPlus AMR classification engine.
  - Core-genome SNP distance matrix calculator.
  - IQ-TREE phylogenetic inference orchestration and Newick exporter.
  - MOB-suite plasmid reconstruction and replicon profiling.
  - AST phenotype-genotype concordance engine with CLSI/EUCAST metrics.
- **Surveillance & Modelling**:
  - 3D interactive Deck.gl / Three.js globe.
  - Safe parameterized natural language spatial query engine.
  - Deterministic SEIR transmission & colonization ODE simulator.
  - Alerting webhooks and WHO GLASS multi-format reporting.
- **Documentation**:
  - Comprehensive scientific methodology, data dictionary, installation, API, and disaster recovery manuals.
