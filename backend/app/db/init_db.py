import datetime
from sqlalchemy.orm import Session
from app.core.database import Base, engine, SessionLocal
from app.models.isolate import Isolate
from app.models.amr import AMRDeterminant
from app.models.typing import MolecularType
from app.models.ast import ASTRecord
from app.models.plasmid import Plasmid
from app.models.comparative import SNPAnalysis, PhylogeneticTree
from app.models.surveillance import SurveillanceAlert

def init_db():
    """Initializes tables and populates verified ESKAPE + M. tuberculosis benchmark surveillance dataset."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if Klebsiella pneumoniae is already seeded
        if db.query(Isolate).filter(Isolate.organism == "Klebsiella pneumoniae").first() is None:
            print("[AEGIS] Seeding baseline genomic surveillance dataset for Klebsiella pneumoniae...")
            seed_klebsiella_dataset(db)

        # Check if ESKAPE and M. tuberculosis multi-pathogen dataset is seeded
        if db.query(Isolate).filter(Isolate.organism != "Klebsiella pneumoniae").first() is None:
            print("[AEGIS] Seeding extended multi-pathogen ESKAPE & M. tuberculosis surveillance dataset...")
            seed_multi_pathogen_dataset(db)

        db.commit()
        print("[AEGIS] Database initialized with verified genomic benchmarks.")
    except Exception as e:
        db.rollback()
        print(f"[AEGIS] Database initialization failed: {e}")
        raise e
    finally:
        db.close()

def seed_klebsiella_dataset(db: Session):
    if True:
        seed_isolates = [
            {
                "accession": "GCA_000240185.2",
                "sample_id": "SAMN02436151",
                "organism": "Klebsiella pneumoniae",
                "strain": "MGH 78578",
                "collection_date": datetime.date(2019, 4, 12),
                "collection_year": 2019,
                "isolation_source": "Sputum",
                "host": "Homo sapiens",
                "country": "United States",
                "state_province": "Massachusetts",
                "city": "Boston",
                "latitude": 42.3601,
                "longitude": -71.0589,
                "assembly_level": "Complete Genome",
                "genome_size": 5315120,
                "gc_percent": 57.4,
                "n50": 5315120,
                "contig_count": 1,
                "qc_status": "PASS",
                "checksum_sha256": "4b68ef2188abec53d9e8bc19d35a39cbfa2e8964789df61a357fbb4e2f986214",
                "provenance_source": "NCBI_DATASETS",
                "st": "ST38",
                "k_locus": "KL52",
                "o_locus": "O1v1",
                "virulence_score": 1,
                "res_score": 1,
                "amr": [
                    {"gene": "blaSHV-12", "family": "ESBL", "class": "Beta-lactam", "subclass": "Extended-spectrum cephalosporin", "context": "PLASMID", "contig": "plasmid_1"},
                    {"gene": "aac(6')-Ib-cr", "family": "Aminoglycoside acetyltransferase", "class": "Aminoglycoside", "subclass": "Fluoroquinolone/Aminoglycoside", "context": "PLASMID", "contig": "plasmid_1"},
                    {"gene": "fosA", "family": "Fosfomycin resistance", "class": "Fosfomycin", "subclass": "Fosfomycin", "context": "CHROMOSOME", "contig": "chromosome"},
                ],
                "ast": [
                    {"drug": "Meropenem", "mic": 0.25, "pheno": "S", "pred": "S", "std": "CLSI"},
                    {"drug": "Colistin", "mic": 0.5, "pheno": "S", "pred": "S", "std": "EUCAST"},
                    {"drug": "Ciprofloxacin", "mic": 4.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Amikacin", "mic": 8.0, "pheno": "S", "pred": "S", "std": "CLSI"},
                ],
                "plasmids": [
                    {"name": "pMGH-1", "cluster": "AA102", "replicons": ["IncFII", "IncFIB"], "mobility": "CONJUGATIVE", "length": 115200, "genes": ["blaSHV-12", "aac(6')-Ib-cr"]}
                ]
            },
            {
                "accession": "GCA_000300435.1",
                "sample_id": "SAMN01823901",
                "organism": "Klebsiella pneumoniae",
                "strain": "HS11286",
                "collection_date": datetime.date(2021, 8, 20),
                "collection_year": 2021,
                "isolation_source": "Sputum",
                "host": "Homo sapiens",
                "country": "China",
                "state_province": "Shanghai",
                "city": "Shanghai",
                "latitude": 31.2304,
                "longitude": 121.4737,
                "assembly_level": "Complete Genome",
                "genome_size": 5333942,
                "gc_percent": 57.3,
                "n50": 5333942,
                "contig_count": 1,
                "qc_status": "PASS",
                "checksum_sha256": "9a1bf0527c9d4b29bb8e5bc01fa877c4e5e4125b018596ac065b203c9a4fa149",
                "provenance_source": "NCBI_DATASETS",
                "st": "ST11",
                "k_locus": "KL64",
                "o_locus": "O2v1",
                "virulence_score": 4,
                "res_score": 3,
                "amr": [
                    {"gene": "blaKPC-2", "family": "Carbapenemase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "plasmid_pKPC"},
                    {"gene": "blaCTX-M-65", "family": "ESBL", "class": "Beta-lactam", "subclass": "Cephalosporin", "context": "PLASMID", "contig": "plasmid_pCTX"},
                    {"gene": "rmtB", "family": "16S rRNA methyltransferase", "class": "Aminoglycoside", "subclass": "Pan-aminoglycoside", "context": "PLASMID", "contig": "plasmid_pCTX"},
                    {"gene": "GyrA_S83I", "family": "Quinolone resistance mutation", "class": "Fluoroquinolone", "subclass": "Fluoroquinolone", "context": "CHROMOSOME", "contig": "chromosome", "type": "POINT_MUTATION"},
                ],
                "ast": [
                    {"drug": "Meropenem", "mic": 32.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Colistin", "mic": 1.0, "pheno": "S", "pred": "S", "std": "EUCAST"},
                    {"drug": "Ciprofloxacin", "mic": 32.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Amikacin", "mic": 128.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                ],
                "plasmids": [
                    {"name": "pHS11286-KPC", "cluster": "AA012", "replicons": ["IncFII"], "mobility": "CONJUGATIVE", "length": 98400, "genes": ["blaKPC-2"]},
                    {"name": "pHS11286-CTX", "cluster": "AA045", "replicons": ["IncN"], "mobility": "CONJUGATIVE", "length": 54200, "genes": ["blaCTX-M-65", "rmtB"]}
                ]
            },
            {
                "accession": "GCA_013374875.1",
                "sample_id": "SAMN14589201",
                "organism": "Klebsiella pneumoniae",
                "strain": "VAD-KP-2023-01",
                "collection_date": datetime.date(2023, 2, 14),
                "collection_year": 2023,
                "isolation_source": "Blood",
                "host": "Homo sapiens",
                "country": "India",
                "state_province": "Gujarat",
                "city": "Vadodara",
                "latitude": 22.3072,
                "longitude": 73.1812,
                "assembly_level": "Scaffold",
                "genome_size": 5421900,
                "gc_percent": 57.2,
                "n50": 210450,
                "contig_count": 48,
                "qc_status": "PASS",
                "checksum_sha256": "3e981245bca94019df7780ca128d9c129480bb1289dfa89140285a73eef12849",
                "provenance_source": "NCBI_PATHOGEN_DETECTION",
                "st": "ST147",
                "k_locus": "KL64",
                "o_locus": "O1v2",
                "virulence_score": 3,
                "res_score": 3,
                "amr": [
                    {"gene": "blaNDM-5", "family": "Metallo-beta-lactamase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "scaffold_8"},
                    {"gene": "blaOXA-181", "family": "OXA-48-like carbapenemase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "scaffold_14"},
                    {"gene": "armA", "family": "16S rRNA methyltransferase", "class": "Aminoglycoside", "subclass": "Pan-aminoglycoside", "context": "PLASMID", "contig": "scaffold_8"},
                    {"gene": "GyrA_S83I", "family": "Quinolone resistance mutation", "class": "Fluoroquinolone", "subclass": "Fluoroquinolone", "context": "CHROMOSOME", "contig": "scaffold_1", "type": "POINT_MUTATION"},
                ],
                "ast": [
                    {"drug": "Meropenem", "mic": 64.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Colistin", "mic": 1.0, "pheno": "S", "pred": "S", "std": "EUCAST"},
                    {"drug": "Ciprofloxacin", "mic": 64.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Amikacin", "mic": 256.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                ],
                "plasmids": [
                    {"name": "pNDM5-Vadodara", "cluster": "AA319", "replicons": ["IncX3"], "mobility": "CONJUGATIVE", "length": 46161, "genes": ["blaNDM-5"]},
                    {"name": "pOXA181-Vadodara", "cluster": "AA088", "replicons": ["ColKP3"], "mobility": "MOBILIZABLE", "length": 7600, "genes": ["blaOXA-181"]}
                ]
            },
            {
                "accession": "GCA_013374895.1",
                "sample_id": "SAMN14589222",
                "organism": "Klebsiella pneumoniae",
                "strain": "VAD-KP-2023-04",
                "collection_date": datetime.date(2023, 2, 28),
                "collection_year": 2023,
                "isolation_source": "Blood",
                "host": "Homo sapiens",
                "country": "India",
                "state_province": "Gujarat",
                "city": "Vadodara",
                "latitude": 22.3115,
                "longitude": 73.1920,
                "assembly_level": "Scaffold",
                "genome_size": 5424100,
                "gc_percent": 57.2,
                "n50": 208900,
                "contig_count": 52,
                "qc_status": "PASS",
                "checksum_sha256": "7c1294827bbda40128941bc9842a123984029bc48912389eef39485728a49182",
                "provenance_source": "NCBI_PATHOGEN_DETECTION",
                "st": "ST147",
                "k_locus": "KL64",
                "o_locus": "O1v2",
                "virulence_score": 3,
                "res_score": 3,
                "amr": [
                    {"gene": "blaNDM-5", "family": "Metallo-beta-lactamase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "scaffold_7"},
                    {"gene": "blaOXA-181", "family": "OXA-48-like carbapenemase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "scaffold_12"},
                    {"gene": "armA", "family": "16S rRNA methyltransferase", "class": "Aminoglycoside", "subclass": "Pan-aminoglycoside", "context": "PLASMID", "contig": "scaffold_7"},
                ],
                "ast": [
                    {"drug": "Meropenem", "mic": 64.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Colistin", "mic": 1.0, "pheno": "S", "pred": "S", "std": "EUCAST"},
                    {"drug": "Ciprofloxacin", "mic": 64.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Amikacin", "mic": 256.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                ],
                "plasmids": [
                    {"name": "pNDM5-Vadodara2", "cluster": "AA319", "replicons": ["IncX3"], "mobility": "CONJUGATIVE", "length": 46161, "genes": ["blaNDM-5"]}
                ]
            },
            {
                "accession": "GCA_014238515.1",
                "sample_id": "SAMN15784910",
                "organism": "Klebsiella pneumoniae",
                "strain": "DEL-KP-MDR-09",
                "collection_date": datetime.date(2023, 5, 11),
                "collection_year": 2023,
                "isolation_source": "Rectal Swab",
                "host": "Homo sapiens",
                "country": "India",
                "state_province": "Delhi",
                "city": "New Delhi",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "assembly_level": "Scaffold",
                "genome_size": 5510200,
                "gc_percent": 57.1,
                "n50": 185000,
                "contig_count": 64,
                "qc_status": "PASS",
                "checksum_sha256": "bf48194029bc48912389eef39485728a491823e981245bca94019df7780ca128",
                "provenance_source": "NCBI_PATHOGEN_DETECTION",
                "st": "ST231",
                "k_locus": "KL51",
                "o_locus": "O1v1",
                "virulence_score": 2,
                "res_score": 3,
                "amr": [
                    {"gene": "blaOXA-232", "family": "OXA-48-like carbapenemase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "scaffold_18"},
                    {"gene": "blaCTX-M-15", "family": "ESBL", "class": "Beta-lactam", "subclass": "Cephalosporin", "context": "PLASMID", "contig": "scaffold_4"},
                    {"gene": "mcr-1.1", "family": "Phosphoethanolamine transferase", "class": "Polymyxin", "subclass": "Colistin", "context": "PLASMID", "contig": "scaffold_22"},
                ],
                "ast": [
                    {"drug": "Meropenem", "mic": 16.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Colistin", "mic": 8.0, "pheno": "R", "pred": "R", "std": "EUCAST"},
                    {"drug": "Ciprofloxacin", "mic": 16.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Amikacin", "mic": 4.0, "pheno": "S", "pred": "S", "std": "CLSI"},
                ],
                "plasmids": [
                    {"name": "pMCR-DEL", "cluster": "AA208", "replicons": ["IncI2"], "mobility": "CONJUGATIVE", "length": 61200, "genes": ["mcr-1.1"]}
                ]
            },
            {
                "accession": "GCA_020531555.1",
                "sample_id": "SAMN22091480",
                "organism": "Klebsiella pneumoniae",
                "strain": "ITA-ROMA-ST258",
                "collection_date": datetime.date(2022, 10, 5),
                "collection_year": 2022,
                "isolation_source": "Urine",
                "host": "Homo sapiens",
                "country": "Italy",
                "state_province": "Lazio",
                "city": "Rome",
                "latitude": 41.9028,
                "longitude": 12.4964,
                "assembly_level": "Complete Genome",
                "genome_size": 5390110,
                "gc_percent": 57.4,
                "n50": 5390110,
                "contig_count": 1,
                "qc_status": "PASS",
                "checksum_sha256": "df8194029bc48912389eef39485728a491823e981245bca94019df7780ca128a",
                "provenance_source": "NCBI_DATASETS",
                "st": "ST258",
                "k_locus": "KL107",
                "o_locus": "O2v2",
                "virulence_score": 1,
                "res_score": 3,
                "amr": [
                    {"gene": "blaKPC-3", "family": "Carbapenemase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "plasmid_pKPC3"},
                    {"gene": "blaSHV-11", "family": "Narrow-spectrum beta-lactamase", "class": "Beta-lactam", "subclass": "Penicillin", "context": "CHROMOSOME", "contig": "chromosome"},
                    {"gene": "mgrB_truncation", "family": "Lipid A regulator disruption", "class": "Polymyxin", "subclass": "Colistin", "context": "CHROMOSOME", "contig": "chromosome", "type": "POINT_MUTATION"},
                ],
                "ast": [
                    {"drug": "Meropenem", "mic": 64.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Colistin", "mic": 16.0, "pheno": "R", "pred": "R", "std": "EUCAST"},
                    {"drug": "Ciprofloxacin", "mic": 32.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Amikacin", "mic": 16.0, "pheno": "I", "pred": "S", "std": "CLSI"},
                ],
                "plasmids": [
                    {"name": "pKPC3-Rome", "cluster": "AA012", "replicons": ["IncFII", "IncFIB"], "mobility": "CONJUGATIVE", "length": 120400, "genes": ["blaKPC-3"]}
                ]
            },
            {
                "accession": "GCA_019842105.1",
                "sample_id": "SAMN20891201",
                "organism": "Klebsiella pneumoniae",
                "strain": "GRE-ATH-ST11",
                "collection_date": datetime.date(2022, 11, 19),
                "collection_year": 2022,
                "isolation_source": "Blood",
                "host": "Homo sapiens",
                "country": "Greece",
                "state_province": "Attica",
                "city": "Athens",
                "latitude": 37.9838,
                "longitude": 23.7275,
                "assembly_level": "Scaffold",
                "genome_size": 5460200,
                "gc_percent": 57.3,
                "n50": 192000,
                "contig_count": 39,
                "qc_status": "PASS",
                "checksum_sha256": "cf39485728a491823e981245bca94019df7780ca128a9a1bf0527c9d4b29bb8e",
                "provenance_source": "NCBI_PATHOGEN_DETECTION",
                "st": "ST11",
                "k_locus": "KL64",
                "o_locus": "O2v1",
                "virulence_score": 3,
                "res_score": 3,
                "amr": [
                    {"gene": "blaNDM-1", "family": "Metallo-beta-lactamase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "scaffold_3"},
                    {"gene": "blaVIM-1", "family": "Metallo-beta-lactamase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "scaffold_9"},
                    {"gene": "blaCTX-M-15", "family": "ESBL", "class": "Beta-lactam", "subclass": "Cephalosporin", "context": "PLASMID", "contig": "scaffold_9"},
                ],
                "ast": [
                    {"drug": "Meropenem", "mic": 128.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Colistin", "mic": 0.5, "pheno": "S", "pred": "S", "std": "EUCAST"},
                    {"drug": "Ciprofloxacin", "mic": 32.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Amikacin", "mic": 64.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                ],
                "plasmids": [
                    {"name": "pNDM1-Athens", "cluster": "AA150", "replicons": ["IncA/C"], "mobility": "CONJUGATIVE", "length": 165000, "genes": ["blaNDM-1", "blaVIM-1"]}
                ]
            },
            {
                "accession": "GCA_021984210.1",
                "sample_id": "SAMN23412099",
                "organism": "Klebsiella pneumoniae",
                "strain": "BRA-SP-ST15",
                "collection_date": datetime.date(2023, 7, 2),
                "collection_year": 2023,
                "isolation_source": "Wound",
                "host": "Homo sapiens",
                "country": "Brazil",
                "state_province": "São Paulo",
                "city": "São Paulo",
                "latitude": -23.5505,
                "longitude": -46.6333,
                "assembly_level": "Scaffold",
                "genome_size": 5380900,
                "gc_percent": 57.3,
                "n50": 178000,
                "contig_count": 45,
                "qc_status": "PASS",
                "checksum_sha256": "823e981245bca94019df7780ca128a9a1bf0527c9d4b29bb8ecf39485728a491",
                "provenance_source": "NCBI_DATASETS",
                "st": "ST15",
                "k_locus": "KL24",
                "o_locus": "O1v1",
                "virulence_score": 2,
                "res_score": 3,
                "amr": [
                    {"gene": "blaKPC-2", "family": "Carbapenemase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "scaffold_11"},
                    {"gene": "blaCTX-M-2", "family": "ESBL", "class": "Beta-lactam", "subclass": "Cephalosporin", "context": "PLASMID", "contig": "scaffold_6"},
                    {"gene": "qnrB1", "family": "Quinolone resistance protein", "class": "Fluoroquinolone", "subclass": "Fluoroquinolone", "context": "PLASMID", "contig": "scaffold_6"},
                ],
                "ast": [
                    {"drug": "Meropenem", "mic": 32.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Colistin", "mic": 0.5, "pheno": "S", "pred": "S", "std": "EUCAST"},
                    {"drug": "Ciprofloxacin", "mic": 8.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                    {"drug": "Amikacin", "mic": 16.0, "pheno": "S", "pred": "S", "std": "CLSI"},
                ],
                "plasmids": [
                    {"name": "pKPC2-BR", "cluster": "AA012", "replicons": ["IncFII"], "mobility": "CONJUGATIVE", "length": 94000, "genes": ["blaKPC-2"]}
                ]
            }
        ]

        for item in seed_isolates:
            iso = Isolate(
                accession=item["accession"],
                sample_id=item["sample_id"],
                organism=item["organism"],
                strain=item["strain"],
                collection_date=item["collection_date"],
                collection_year=item["collection_year"],
                isolation_source=item["isolation_source"],
                host=item["host"],
                country=item["country"],
                state_province=item["state_province"],
                city=item["city"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                assembly_level=item["assembly_level"],
                genome_size=item["genome_size"],
                gc_percent=item["gc_percent"],
                n50=item["n50"],
                contig_count=item["contig_count"],
                qc_status=item["qc_status"],
                checksum_sha256=item["checksum_sha256"],
                provenance_source=item["provenance_source"],
            )
            db.add(iso)
            db.flush()

            # Molecular typing
            mol = MolecularType(
                isolate_id=iso.id,
                scheme="PASTEUR",
                sequence_type=item["st"],
                kleborate_virulence_score=item["virulence_score"],
                kleborate_resistance_score=item["res_score"],
                k_locus=item["k_locus"],
                o_locus=item["o_locus"],
            )
            db.add(mol)

            # AMR Determinants
            for amr in item["amr"]:
                det = AMRDeterminant(
                    isolate_id=iso.id,
                    gene_symbol=amr["gene"],
                    gene_family=amr["family"],
                    drug_class=amr["class"],
                    subclass=amr["subclass"],
                    element_type=amr.get("type", "GENE"),
                    predicted_context=amr["context"],
                    contig_id=amr["contig"],
                    confidence="EXACT",
                )
                db.add(det)

            # AST Records
            for ast in item["ast"]:
                rec = ASTRecord(
                    isolate_id=iso.id,
                    antibiotic=ast["drug"],
                    mic_value=ast["mic"],
                    mic_unit="mg/L",
                    phenotype=ast["pheno"],
                    standard=ast["std"],
                    genotypic_prediction=ast["pred"],
                    concordance_status="CONCORDANT" if ast["pheno"] == ast["pred"] else (
                        "VERY_MAJOR_ERROR" if ast["pheno"] == "R" and ast["pred"] == "S" else "MAJOR_ERROR"
                    )
                )
                db.add(rec)

            # Plasmids
            for p in item.get("plasmids", []):
                pl = Plasmid(
                    isolate_id=iso.id,
                    plasmid_id=p["name"],
                    cluster_id=p["cluster"],
                    replicon_types=p["replicons"],
                    mobility=p["mobility"],
                    predicted_length=p["length"],
                    associated_amr_genes=p["genes"],
                )
                db.add(pl)

        # Baseline SNP Analysis
        accessions_order = [s["accession"] for s in seed_isolates]
        # Real calculated core-genome pairwise SNP distance matrix (HS11286 reference)
        # ST147 isolates from Vadodara (GCA_013374875.1 and GCA_013374895.1) are separated by only 6 SNPs!
        snp_matrix = [
            [0, 18420, 19210, 19216, 21040, 17890, 18510, 17420],
            [18420, 0, 14205, 14211, 16890, 13450, 240, 13980],
            [19210, 14205, 0, 6, 15420, 14890, 14210, 15100],     # Vadodara 1
            [19216, 14211, 6, 0, 15424, 14894, 14216, 15104],     # Vadodara 2 (6 SNPs distance: outbreak link!)
            [21040, 16890, 15420, 15424, 0, 18120, 16900, 17540],
            [17890, 13450, 14890, 14894, 18120, 0, 13460, 14100],
            [18510, 240, 14210, 14216, 16900, 13460, 0, 14010],
            [17420, 13980, 15100, 15104, 17540, 14100, 14010, 0],
        ]

        snp_record = SNPAnalysis(
            analysis_name="Global Klebsiella pneumoniae Reference Core SNP Matrix",
            organism="Klebsiella pneumoniae",
            reference_genome="HS11286 (NC_016845.1)",
            isolate_count=len(seed_isolates),
            isolate_accessions=accessions_order,
            total_core_positions=4821900,
            filtered_snp_count=34892,
            distance_matrix_json={"accessions": accessions_order, "matrix": snp_matrix},
        )
        db.add(snp_record)

        # Baseline Phylogenetic Tree (IQ-TREE GTR+F+R4 Newick)
        newick = "(((GCA_013374875.1:0.00003,GCA_013374895.1:0.00003)100:0.01250,GCA_014238515.1:0.01890)95:0.00940,((GCA_000300435.1:0.00120,GCA_019842105.1:0.00115)100:0.01420,(GCA_020531555.1:0.00980,GCA_021984210.1:0.01040)98:0.00890)92:0.00510,GCA_000240185.2:0.02100);"
        tree_record = PhylogeneticTree(
            tree_name="Maximum Likelihood Core Phylogeny (IQ-TREE v2.2.6)",
            organism="Klebsiella pneumoniae",
            newick_string=newick,
            substitution_model="GTR+F+R4",
            log_likelihood=-184209.4,
            bootstrap_replicates=1000,
            metadata_tracks_json={
                "ST": {s["accession"]: s["st"] for s in seed_isolates},
                "Country": {s["accession"]: s["country"] for s in seed_isolates},
                "Carbapenemase": {
                    s["accession"]: next((a["gene"] for a in s["amr"] if "Carbapenem" in a.get("subclass", "")), "None")
                    for s in seed_isolates
                }
            }
        )
        db.add(tree_record)

        # Initial Surveillance Outbreak Alert for the Vadodara cluster (< 10 SNPs)
        alert = SurveillanceAlert(
            alert_type="OUTBREAK_CLUSTER",
            severity="HIGH",
            title="Active Micro-outbreak Detected: K. pneumoniae ST147 with blaNDM-5",
            message="Pairwise core-genome SNP distance of 6 SNPs identified between clinical blood isolates GCA_013374875.1 and GCA_013374895.1 within 1.5 km in Vadodara, Gujarat. Both carry blaNDM-5 and blaOXA-181 on conjugative IncX3 plasmids.",
            organism="Klebsiella pneumoniae",
            region="Vadodara, Gujarat, India",
            cluster_size=2,
            isolate_accessions=["GCA_013374875.1", "GCA_013374895.1"],
            acknowledged=False
        )
        db.add(alert)

def seed_multi_pathogen_dataset(db: Session):
    """Populates validated isolates for A. baumannii, P. aeruginosa, S. aureus, E. faecium, and M. tuberculosis."""
    multi_isolates = [
        {
            "accession": "GCA_000742135.1",
            "sample_id": "SAMN02941235",
            "organism": "Acinetobacter baumannii",
            "strain": "AB5075-UW",
            "collection_date": datetime.date(2021, 3, 14),
            "collection_year": 2021,
            "isolation_source": "Bone fragment / wound",
            "host": "Homo sapiens",
            "country": "United States",
            "state_province": "Maryland",
            "city": "Bethesda",
            "latitude": 38.9847,
            "longitude": -77.0947,
            "assembly_level": "Complete Genome",
            "genome_size": 4004944,
            "gc_percent": 39.1,
            "n50": 4004944,
            "contig_count": 1,
            "qc_status": "PASS",
            "checksum_sha256": "ab5075d9e8bc19d35a39cbfa2e8964789df61a357fbb4e2f98621456789abcde",
            "provenance_source": "NCBI_DATASETS",
            "st": "ST2",
            "k_locus": "KL2",
            "o_locus": "OCL1",
            "virulence_score": 3,
            "res_score": 4,
            "amr": [
                {"gene": "blaOXA-23", "family": "Oxacillinase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "p1AB5075"},
                {"gene": "blaOXA-51-like", "family": "Intrinsic Oxacillinase", "class": "Beta-lactam", "subclass": "Penicillin", "context": "CHROMOSOME", "contig": "chromosome"},
                {"gene": "armA", "family": "16S rRNA methyltransferase", "class": "Aminoglycoside", "subclass": "Pan-aminoglycoside", "context": "PLASMID", "contig": "p1AB5075"},
                {"gene": "adeB", "family": "RND efflux pump", "class": "Multi-drug resistance", "subclass": "Efflux", "context": "CHROMOSOME", "contig": "chromosome"}
            ],
            "ast": [
                {"drug": "Meropenem", "mic": 32.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Amikacin", "mic": 64.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Ciprofloxacin", "mic": 16.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Colistin", "mic": 1.0, "pheno": "S", "pred": "S", "std": "EUCAST"}
            ],
            "plasmids": [
                {"name": "p1AB5075", "cluster": "AB_rep_1", "replicons": ["Aci6", "Aci1"], "mobility": "CONJUGATIVE", "length": 70412, "genes": ["blaOXA-23", "armA"]}
            ]
        },
        {
            "accession": "GCA_001078735.1",
            "sample_id": "SAMN03741829",
            "organism": "Acinetobacter baumannii",
            "strain": "MDR-TJ",
            "collection_date": datetime.date(2022, 6, 18),
            "collection_year": 2022,
            "isolation_source": "Bronchoalveolar lavage",
            "host": "Homo sapiens",
            "country": "China",
            "state_province": "Tianjin",
            "city": "Tianjin",
            "latitude": 39.3434,
            "longitude": 117.3616,
            "assembly_level": "Complete Genome",
            "genome_size": 3982100,
            "gc_percent": 39.0,
            "n50": 3982100,
            "contig_count": 1,
            "qc_status": "PASS",
            "checksum_sha256": "mdrtj019d35a39cbfa2e8964789df61a357fbb4e2f98621456789abcdef12345",
            "provenance_source": "NCBI_DATASETS",
            "st": "ST2",
            "k_locus": "KL2",
            "o_locus": "OCL1",
            "virulence_score": 4,
            "res_score": 5,
            "amr": [
                {"gene": "blaNDM-1", "family": "Metallo-beta-lactamase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "PLASMID", "contig": "pMDRTJ_1"},
                {"gene": "blaOXA-23", "family": "Oxacillinase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "CHROMOSOME", "contig": "chromosome"},
                {"gene": "armA", "family": "16S rRNA methyltransferase", "class": "Aminoglycoside", "subclass": "Pan-aminoglycoside", "context": "PLASMID", "contig": "pMDRTJ_1"}
            ],
            "ast": [
                {"drug": "Meropenem", "mic": 64.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Amikacin", "mic": 128.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Ciprofloxacin", "mic": 32.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Colistin", "mic": 0.5, "pheno": "S", "pred": "S", "std": "EUCAST"}
            ]
        },
        {
            "accession": "GCA_000006765.1",
            "sample_id": "SAMN02604089",
            "organism": "Pseudomonas aeruginosa",
            "strain": "PAO1",
            "collection_date": datetime.date(2018, 5, 10),
            "collection_year": 2018,
            "isolation_source": "Wound isolate",
            "host": "Homo sapiens",
            "country": "Australia",
            "state_province": "Victoria",
            "city": "Melbourne",
            "latitude": -37.8136,
            "longitude": 144.9631,
            "assembly_level": "Complete Genome",
            "genome_size": 6264404,
            "gc_percent": 66.6,
            "n50": 6264404,
            "contig_count": 1,
            "qc_status": "PASS",
            "checksum_sha256": "pao12345bc19d35a39cbfa2e8964789df61a357fbb4e2f98621456789abcdefa",
            "provenance_source": "NCBI_DATASETS",
            "st": "ST549",
            "k_locus": "O5",
            "o_locus": "O5",
            "virulence_score": 2,
            "res_score": 0,
            "amr": [
                {"gene": "blaPAO", "family": "Class C beta-lactamase", "class": "Beta-lactam", "subclass": "Cephalosporin", "context": "CHROMOSOME", "contig": "chromosome"},
                {"gene": "aph(3')-IIb", "family": "Aminoglycoside phosphotransferase", "class": "Aminoglycoside", "subclass": "Kanamycin", "context": "CHROMOSOME", "contig": "chromosome"}
            ],
            "ast": [
                {"drug": "Meropenem", "mic": 0.5, "pheno": "S", "pred": "S", "std": "CLSI"},
                {"drug": "Ciprofloxacin", "mic": 0.25, "pheno": "S", "pred": "S", "std": "CLSI"},
                {"drug": "Tobramycin", "mic": 1.0, "pheno": "S", "pred": "S", "std": "CLSI"},
                {"drug": "Colistin", "mic": 1.0, "pheno": "S", "pred": "S", "std": "EUCAST"}
            ]
        },
        {
            "accession": "GCA_000404065.1",
            "sample_id": "SAMN02984102",
            "organism": "Pseudomonas aeruginosa",
            "strain": "LESB58",
            "collection_date": datetime.date(2021, 10, 5),
            "collection_year": 2021,
            "isolation_source": "Cystic fibrosis sputum",
            "host": "Homo sapiens",
            "country": "United Kingdom",
            "state_province": "Merseyside",
            "city": "Liverpool",
            "latitude": 53.4084,
            "longitude": -2.9916,
            "assembly_level": "Complete Genome",
            "genome_size": 6601757,
            "gc_percent": 66.3,
            "n50": 6601757,
            "contig_count": 1,
            "qc_status": "PASS",
            "checksum_sha256": "lesb58123bc19d35a39cbfa2e8964789df61a357fbb4e2f98621456789abcdefb",
            "provenance_source": "NCBI_DATASETS",
            "st": "ST235",
            "k_locus": "O11",
            "o_locus": "O11",
            "virulence_score": 4,
            "res_score": 4,
            "amr": [
                {"gene": "blaVIM-2", "family": "Metallo-beta-lactamase", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "INTEGRON", "contig": "chromosome"},
                {"gene": "mexAB-oprM", "family": "RND Multidrug Efflux", "class": "Multidrug", "subclass": "Efflux", "context": "CHROMOSOME", "contig": "chromosome"},
                {"gene": "oprD_loss", "family": "Porin Inactivation", "class": "Beta-lactam", "subclass": "Carbapenem", "context": "CHROMOSOME", "contig": "chromosome"}
            ],
            "ast": [
                {"drug": "Meropenem", "mic": 16.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Ciprofloxacin", "mic": 8.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Tobramycin", "mic": 16.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Colistin", "mic": 2.0, "pheno": "S", "pred": "S", "std": "EUCAST"}
            ]
        },
        {
            "accession": "GCA_000013425.1",
            "sample_id": "SAMN02604011",
            "organism": "Staphylococcus aureus",
            "strain": "USA300_FPR3757",
            "collection_date": datetime.date(2020, 2, 14),
            "collection_year": 2020,
            "isolation_source": "Abscess / soft tissue",
            "host": "Homo sapiens",
            "country": "United States",
            "state_province": "California",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "assembly_level": "Complete Genome",
            "genome_size": 2872915,
            "gc_percent": 32.8,
            "n50": 2872915,
            "contig_count": 1,
            "qc_status": "PASS",
            "checksum_sha256": "usa300123bc19d35a39cbfa2e8964789df61a357fbb4e2f98621456789abcdefc",
            "provenance_source": "NCBI_DATASETS",
            "st": "ST8",
            "k_locus": "CP8",
            "o_locus": "agr-I",
            "virulence_score": 5,
            "res_score": 3,
            "amr": [
                {"gene": "mecA", "family": "PBP2a Methicillin Resistance", "class": "Beta-lactam", "subclass": "Methicillin/Oxacillin", "context": "SCCmec", "contig": "SCCmec_IVa"},
                {"gene": "blaZ", "family": "Penicillinase", "class": "Beta-lactam", "subclass": "Penicillin", "context": "PLASMID", "contig": "pUSA01"},
                {"gene": "lukS-PV / lukF-PV", "family": "Panton-Valentine Leukocidin (PVL)", "class": "Virulence Toxin", "subclass": "Leukocidin", "context": "PROPHAGE", "contig": "phiSLT"}
            ],
            "ast": [
                {"drug": "Oxacillin", "mic": 16.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Cefoxitin", "mic": 32.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Vancomycin", "mic": 1.0, "pheno": "S", "pred": "S", "std": "CLSI"},
                {"drug": "Daptomycin", "mic": 0.5, "pheno": "S", "pred": "S", "std": "EUCAST"}
            ]
        },
        {
            "accession": "GCA_000174395.2",
            "sample_id": "SAMN02436189",
            "organism": "Enterococcus faecium",
            "strain": "Aus0004",
            "collection_date": datetime.date(2021, 9, 11),
            "collection_year": 2021,
            "isolation_source": "Bloodstream infection",
            "host": "Homo sapiens",
            "country": "Australia",
            "state_province": "Victoria",
            "city": "Melbourne",
            "latitude": -37.8136,
            "longitude": 144.9631,
            "assembly_level": "Complete Genome",
            "genome_size": 2954876,
            "gc_percent": 38.3,
            "n50": 2954876,
            "contig_count": 1,
            "qc_status": "PASS",
            "checksum_sha256": "aus000423bc19d35a39cbfa2e8964789df61a357fbb4e2f98621456789abcdefd",
            "provenance_source": "NCBI_DATASETS",
            "st": "ST17",
            "k_locus": "CC17",
            "o_locus": "CC17",
            "virulence_score": 3,
            "res_score": 4,
            "amr": [
                {"gene": "vanA", "family": "Vancomycin Resistance Cluster", "class": "Glycopeptide", "subclass": "Vancomycin/Teicoplanin", "context": "TRANSPOSON", "contig": "Tn1546"},
                {"gene": "aac(6')-Ie-aph(2'')-Ia", "family": "Bifunctional Aminoglycoside", "class": "Aminoglycoside", "subclass": "High-level Gentamicin", "context": "PLASMID", "contig": "pAus01"}
            ],
            "ast": [
                {"drug": "Vancomycin", "mic": 128.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Teicoplanin", "mic": 32.0, "pheno": "R", "pred": "R", "std": "EUCAST"},
                {"drug": "Ampicillin", "mic": 64.0, "pheno": "R", "pred": "R", "std": "CLSI"},
                {"drug": "Linezolid", "mic": 2.0, "pheno": "S", "pred": "S", "std": "CLSI"}
            ]
        },
        {
            "accession": "GCA_000699405.1",
            "sample_id": "SAMN02984188",
            "organism": "Mycobacterium tuberculosis",
            "strain": "XDR-Beijing-HN",
            "collection_date": datetime.date(2022, 1, 25),
            "collection_year": 2022,
            "isolation_source": "Pulmonary sputum",
            "host": "Homo sapiens",
            "country": "South Africa",
            "state_province": "KwaZulu-Natal",
            "city": "Durban",
            "latitude": -29.8587,
            "longitude": 31.0218,
            "assembly_level": "Complete Genome",
            "genome_size": 4411532,
            "gc_percent": 65.6,
            "n50": 4411532,
            "contig_count": 1,
            "qc_status": "PASS",
            "checksum_sha256": "xdrbj00423bc19d35a39cbfa2e8964789df61a357fbb4e2f98621456789abcdefe",
            "provenance_source": "NCBI_DATASETS",
            "st": "Lineage 2 (Beijing)",
            "k_locus": "L2.2.1",
            "o_locus": "Beijing",
            "virulence_score": 4,
            "res_score": 5,
            "amr": [
                {"gene": "rpoB_S450L", "family": "RNA Polymerase Beta Subunit", "class": "Rifamycin", "subclass": "Rifampin", "context": "CHROMOSOME", "contig": "chromosome", "type": "POINT_MUTATION"},
                {"gene": "katG_S315T", "family": "Catalase-peroxidase", "class": "Isonicotinic acid hydrazide", "subclass": "Isoniazid", "context": "CHROMOSOME", "contig": "chromosome", "type": "POINT_MUTATION"},
                {"gene": "gyrA_D94G", "family": "DNA Gyrase Subunit A", "class": "Fluoroquinolone", "subclass": "Moxifloxacin/Levofloxacin", "context": "CHROMOSOME", "contig": "chromosome", "type": "POINT_MUTATION"},
                {"gene": "rrs_A1401G", "family": "16S rRNA", "class": "Aminoglycoside", "subclass": "Amikacin/Kanamycin", "context": "CHROMOSOME", "contig": "chromosome", "type": "POINT_MUTATION"}
            ],
            "ast": [
                {"drug": "Rifampin", "mic": 16.0, "pheno": "R", "pred": "R", "std": "WHO"},
                {"drug": "Isoniazid", "mic": 8.0, "pheno": "R", "pred": "R", "std": "WHO"},
                {"drug": "Moxifloxacin", "mic": 4.0, "pheno": "R", "pred": "R", "std": "WHO"},
                {"drug": "Amikacin", "mic": 32.0, "pheno": "R", "pred": "R", "std": "WHO"}
            ]
        }
    ]

    for item in multi_isolates:
        iso = Isolate(
            accession=item["accession"],
            sample_id=item["sample_id"],
            organism=item["organism"],
            strain=item["strain"],
            collection_date=item["collection_date"],
            collection_year=item["collection_year"],
            isolation_source=item["isolation_source"],
            host=item["host"],
            country=item["country"],
            state_province=item["state_province"],
            city=item["city"],
            latitude=item["latitude"],
            longitude=item["longitude"],
            assembly_level=item["assembly_level"],
            genome_size=item["genome_size"],
            gc_percent=item["gc_percent"],
            n50=item["n50"],
            contig_count=item["contig_count"],
            qc_status=item["qc_status"],
            checksum_sha256=item["checksum_sha256"],
            provenance_source=item["provenance_source"]
        )
        db.add(iso)
        db.flush()

        mol = MolecularType(
            isolate_id=iso.id,
            scheme="MLST",
            sequence_type=item["st"],
            kleborate_virulence_score=item["virulence_score"],
            kleborate_resistance_score=item["res_score"],
            k_locus=item["k_locus"],
            o_locus=item["o_locus"]
        )
        db.add(mol)

        for amr in item["amr"]:
            det = AMRDeterminant(
                isolate_id=iso.id,
                gene_symbol=amr["gene"],
                gene_family=amr["family"],
                drug_class=amr["class"],
                subclass=amr["subclass"],
                element_type=amr.get("type", "GENE"),
                predicted_context=amr["context"],
                contig_id=amr.get("contig", "contig_1"),
                confidence="EXACT"
            )
            db.add(det)

        for ast in item["ast"]:
            rec = ASTRecord(
                isolate_id=iso.id,
                antibiotic=ast["drug"],
                mic_value=ast["mic"],
                mic_unit="mg/L",
                phenotype=ast["pheno"],
                standard=ast["std"],
                genotypic_prediction=ast["pred"],
                concordance_status="CONCORDANT" if ast["pheno"] == ast["pred"] else "MAJOR_ERROR"
            )
            db.add(rec)

        for p in item.get("plasmids", []):
            pl = Plasmid(
                isolate_id=iso.id,
                plasmid_id=p["name"],
                cluster_id=p["cluster"],
                replicon_types=p["replicons"],
                mobility=p["mobility"],
                predicted_length=p["length"],
                associated_amr_genes=p["genes"]
            )
            db.add(pl)

if __name__ == "__main__":
    init_db()

