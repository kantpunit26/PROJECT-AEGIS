# PROJECT AEGIS 2.0 — ARCHITECTURE SPECIFICATION

## 1. System Overview

PROJECT AEGIS 2.0 is structured as a decoupled, microservices-ready modular monolith. It provides high scientific reproducibility, complete audit trails, spatial indexing, and automated pipeline dispatch.

```
+-------------------------------------------------------------------------+
|                               UI LAYER                                  |
|   React 18 / Vite / TypeScript / Tailwind CSS / Deck.gl / Three.js      |
+-------------------------------------------------------------------------+
                                     |
                          HTTPS / REST API (OpenAPI)
                                     v
+-------------------------------------------------------------------------+
|                              API LAYER                                  |
|   FastAPI / Pydantic v2 / OAuth2 JWT / Structured Validation / CORS    |
+-------------------------------------------------------------------------+
          |                                            |
          v                                            v
+-----------------------+                    +----------------------------+
|    SERVICE LAYER      |                    |     ASYNC DISPATCHER       |
| - NCBI Ingestion      |                    | Celery Task Queue (Redis)  |
| - AMRFinder & Rules   |                    +----------------------------+
| - AST Concordance     |                                  |
| - SNP Matrix Engine   |                                  v
| - SEIR ODE Solver     |                    +----------------------------+
| - PostGIS Queries     |                    |   BIOINFORMATICS ENGINE    |
+-----------------------+                    | - Nextflow Orchestration   |
          |                                  | - FastQC / QUAST / CheckM2 |
          v                                  | - AMRFinderPlus / MLST     |
+-----------------------+                    | - Snippy / IQ-TREE / MOB   |
|  PERSISTENCE LAYER    |                    +----------------------------+
| SQLAlchemy 2.0 ORM    |                                  |
| PostgreSQL 16+PostGIS |<---------------------------------+
+-----------------------+
```

## 2. Core Architectural Pillars

### 2.1 Scientific Integrity & Data Provenance
- Every isolate ingested preserves its raw accession identifier, download URL, MD5/SHA256 checksum, collection date, geographic coordinates, and submission metadata.
- Missing values are explicitly flagged as `UNAVAILABLE` or `NULL`—never manufactured or interpolated.
- Genetic predictions (e.g. *bla*KPC-2 presence) are explicitly kept distinct from phenotypic susceptibility outcomes (e.g. Meropenem MIC $\ge 16$ mg/L).

### 2.2 Storage & Persistence
- Relational entities with spatial attributes (isolates, sampling sites, hospital centers) use PostGIS geometry (`Point`, SRID 4326 WGS84).
- High-volume genomic matrices (pairwise SNP distances) are stored using efficient relational and columnar BLOB/JSON formats.
- File storage uses a structured local hierarchy (`./data/raw`, `./data/processed`, `./data/reference`), with mountable volume mapping in Docker for portability.

### 2.3 Modular Ingestion Architecture
- Ingestion supports direct NCBI Entrez / Datasets REST endpoints, BioSample metadata parsing, and fallback ingestion from pre-curated reference packages for offline/air-gapped deployments.

