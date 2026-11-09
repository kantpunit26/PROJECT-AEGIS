# PROJECT AEGIS 2.0 — SECURITY & PROVENANCE

## 1. Threat Model & Safeguards

PROJECT AEGIS 2.0 handles sensitive microbiological, clinical, and spatial epidemiological datasets.

### 1.1 Spatial Privacy & Coordinate Aggregation
- Exact coordinates of private residences, hospital floors, or vulnerable wards are never stored.
- When coordinate sensitivity is flagged, the system jitter-aggregates or snaps coordinates to municipal/district centroids (PostGIS `ST_Centroid` or spatial grid bins).
- Natural language queries are strictly tokenized and mapped to parameterized ORM clauses—arbitrary SQL execution is strictly prohibited.

### 1.2 Authentication & Access Control
- JWT-based authentication using HS256 with cryptographically generated secret tokens.
- Role-Based Access Control (RBAC):
  - `Viewer`: Read-only access to surveillance dashboards and aggregated reports.
  - `Analyst`: Run comparative genomics, execute SEIR models, export datasets.
  - `Admin`: User management, NCBI pipeline scheduling, system configuration.

### 1.3 Data Provenance & Cryptographic Integrity
- Raw input sequences (FASTQ/FASTA) undergo SHA256 checksum generation upon ingestion.
- Software tool versions (e.g., AMRFinderPlus v3.12.8, IQ-TREE v2.2.6) and database releases (NCBI AMR db v2024-05-02.1) are permanently recorded per analysis run.

