# PROJECT AEGIS 2.0 — API DOCUMENTATION

The AEGIS 2.0 backend exposes an OpenAPI 3.1 compliant REST API under `/api/v1`.

Interactive Swagger UI: `http://localhost:8000/docs`  
ReDoc UI: `http://localhost:8000/redoc`

---

## 1. Authentication Endpoints

- `POST /api/v1/auth/login`: Authenticate with username and password, returns JWT bearer token.
- `GET /api/v1/auth/me`: Retrieve currently authenticated researcher identity and roles.

---

## 2. Health & System Status

- `GET /api/v1/health`: Returns overall system health, database connection state, Redis status, and version.

---

## 3. Isolates Registry

- `GET /api/v1/isolates`: Query isolates with filtering (`organism`, `country`, `year`, `qc_status`, `sequence_type`, `amr_gene`). Supports pagination (`skip`, `limit`).
- `GET /api/v1/isolates/{id}`: Detailed isolate record with linked AMR determinants, sequence types, plasmids, and AST values.
- `POST /api/v1/isolates`: Register a new isolate record with validation.
- `POST /api/v1/isolates/ingest/ncbi`: Trigger automated NCBI acquisition job for an organism or accession list.

---

## 4. AMR Analytics

- `GET /api/v1/amr/determinants`: Search resistance determinants across isolates.
- `GET /api/v1/amr/prevalence`: Gene prevalence summary aggregated by drug class and organism.
- `GET /api/v1/amr/co-occurrence`: Matrix of co-occurring resistance genes (e.g. *bla*KPC with *bla*CTX-M-15).

---

## 5. Molecular Typing

- `GET /api/v1/typing/mlst-distribution`: Sequence type frequency counts for phylogenetic and epidemiological mapping.
- `GET /api/v1/typing/kleborate-summary`: Virulence score vs. resistance score 2D distribution.

---

## 6. AST & Concordance Validation

- `GET /api/v1/ast/records`: Retrieve experimental MIC data.
- `GET /api/v1/ast/concordance`: Calculate genotype-phenotype concordance metrics (Sensitivity, Specificity, PPV, NPV, Major Error, Very Major Error rates).

---

## 7. Comparative Genomics & Phylogenetics

- `POST /api/v1/comparative/snp-matrix`: Compute or retrieve pairwise core-genome SNP distance matrix.
- `GET /api/v1/comparative/trees`: Retrieve maximum-likelihood Newick trees with linked isolate metadata tracks.
- `GET /api/v1/comparative/circular-genome`: Coordinates for circular genome map rendering (GC skew, GC content, CDS, mobile elements).

---

## 8. Plasmid Characterization

- `GET /api/v1/plasmids`: Plasmid reconstructions, incompatibility replicon distribution, and AMR localization.
- `GET /api/v1/plasmids/matrix`: Chromosome vs. plasmid genetic context matrix.

---

## 9. Geospatial Surveillance

- `GET /api/v1/surveillance/spatial-clusters`: PostGIS spatial clustering of isolates and resistance phenotypes.
- `POST /api/v1/surveillance/nl-query`: Safe parameterized natural language query translation (e.g., *"Show all K. pneumoniae isolates with blaNDM within 50 km of Vadodara"*).

---

## 10. Epidemiological Modelling

- `POST /api/v1/modelling/seir/simulate`: Run deterministic Runge-Kutta SEIR simulation with colonization, treatment, and hospital parameters.
- `GET /api/v1/modelling/scenarios`: List historical saved simulation runs and scenarios.

---

## 11. Alerts & Reports Export

- `GET /api/v1/alerts`: Active surveillance alerts and threshold breaches.
- `POST /api/v1/reports/export`: Export surveillance datasets in CSV, GeoJSON, Newick, JSON, or WHO GLASS format.
