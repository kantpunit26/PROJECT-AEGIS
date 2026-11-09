from typing import List, Optional
import time
import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.isolate import Isolate
from app.models.amr import AMRDeterminant
from app.models.typing import MolecularType
from app.schemas.isolate import IsolateOut, IsolateDetailOut, IsolateCreate
from app.services.ncbi_service import ncbi_service
from app.services.fasta_service import fasta_service

router = APIRouter()

@router.get("", response_model=List[IsolateOut], summary="List & Filter Isolates")
def list_isolates(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    organism: Optional[str] = None,
    country: Optional[str] = None,
    year: Optional[int] = None,
    qc_status: Optional[str] = None,
    amr_gene: Optional[str] = None
):
    query = db.query(Isolate)
    if organism:
        query = query.filter(Isolate.organism.ilike(f"%{organism}%"))
    if country:
        query = query.filter(Isolate.country.ilike(f"%{country}%"))
    if year:
        query = query.filter(Isolate.collection_year == year)
    if qc_status:
        query = query.filter(Isolate.qc_status == qc_status)

    if amr_gene:
        query = query.join(AMRDeterminant).filter(AMRDeterminant.gene_symbol.ilike(f"%{amr_gene}%"))

    isolates = query.offset(skip).limit(limit).all()
    results = []
    for iso in isolates:
        amr_count = len(iso.amr_determinants)
        st = iso.molecular_types[0].sequence_type if iso.molecular_types else None
        
        iso_dict = {
            "id": iso.id,
            "accession": iso.accession,
            "sample_id": iso.sample_id,
            "organism": iso.organism,
            "taxon_id": iso.taxon_id,
            "strain": iso.strain,
            "collection_date": iso.collection_date,
            "collection_year": iso.collection_year,
            "isolation_source": iso.isolation_source,
            "host": iso.host,
            "country": iso.country,
            "state_province": iso.state_province,
            "city": iso.city,
            "latitude": iso.latitude,
            "longitude": iso.longitude,
            "assembly_level": iso.assembly_level,
            "genome_size": iso.genome_size,
            "gc_percent": iso.gc_percent,
            "n50": iso.n50,
            "contig_count": iso.contig_count,
            "qc_status": iso.qc_status,
            "qc_notes": iso.qc_notes,
            "checksum_sha256": iso.checksum_sha256,
            "provenance_source": iso.provenance_source,
            "created_at": iso.created_at,
            "updated_at": iso.updated_at,
            "amr_count": amr_count,
            "sequence_type": st
        }
        results.append(iso_dict)
    return results

@router.get("/{id}", summary="Get Detailed Isolate Profile")
def get_isolate(id: str, db: Session = Depends(get_db)):
    iso = db.query(Isolate).filter(Isolate.id == id).first()
    if not iso:
        iso = db.query(Isolate).filter(Isolate.accession == id).first()
    if not iso:
        raise HTTPException(status_code=404, detail=f"Isolate '{id}' not found")

    return {
        "id": iso.id,
        "accession": iso.accession,
        "sample_id": iso.sample_id,
        "organism": iso.organism,
        "strain": iso.strain,
        "collection_date": iso.collection_date,
        "collection_year": iso.collection_year,
        "isolation_source": iso.isolation_source,
        "host": iso.host,
        "country": iso.country,
        "state_province": iso.state_province,
        "city": iso.city,
        "latitude": iso.latitude,
        "longitude": iso.longitude,
        "assembly_level": iso.assembly_level,
        "genome_size": iso.genome_size,
        "gc_percent": iso.gc_percent,
        "n50": iso.n50,
        "contig_count": iso.contig_count,
        "qc_status": iso.qc_status,
        "qc_notes": iso.qc_notes,
        "checksum_sha256": iso.checksum_sha256,
        "provenance_source": iso.provenance_source,
        "created_at": iso.created_at,
        "updated_at": iso.updated_at,
        "amr_determinants": [
            {
                "id": d.id,
                "gene_symbol": d.gene_symbol,
                "gene_family": d.gene_family,
                "drug_class": d.drug_class,
                "subclass": d.subclass,
                "element_type": d.element_type,
                "mutation_name": d.mutation_name,
                "predicted_context": d.predicted_context,
                "contig_id": d.contig_id,
                "confidence": d.confidence
            }
            for d in iso.amr_determinants
        ],
        "molecular_types": [
            {
                "scheme": m.scheme,
                "sequence_type": m.sequence_type,
                "k_locus": m.k_locus,
                "o_locus": m.o_locus,
                "kleborate_virulence_score": m.kleborate_virulence_score,
                "kleborate_resistance_score": m.kleborate_resistance_score
            }
            for m in iso.molecular_types
        ],
        "ast_records": [
            {
                "antibiotic": a.antibiotic,
                "mic_value": a.mic_value,
                "mic_unit": a.mic_unit,
                "phenotype": a.phenotype,
                "standard": a.standard,
                "genotypic_prediction": a.genotypic_prediction,
                "concordance_status": a.concordance_status
            }
            for a in iso.ast_records
        ],
        "plasmids": [
            {
                "plasmid_id": p.plasmid_id,
                "cluster_id": p.cluster_id,
                "replicon_types": p.replicon_types,
                "mobility": p.mobility,
                "predicted_length": p.predicted_length,
                "associated_amr_genes": p.associated_amr_genes
            }
            for p in iso.plasmids
        ]
    }

@router.post("", response_model=IsolateOut, status_code=status.HTTP_201_CREATED, summary="Register New Isolate")
def create_isolate(isolate_in: IsolateCreate, db: Session = Depends(get_db)):
    existing = db.query(Isolate).filter(Isolate.accession == isolate_in.accession).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Isolate accession '{isolate_in.accession}' already registered")

    iso = Isolate(**isolate_in.model_dump())
    db.add(iso)
    db.commit()
    db.refresh(iso)
    return iso

@router.post("/ingest/ncbi", summary="Trigger Automated NCBI Ingestion")
def ingest_from_ncbi(accession: str, db: Session = Depends(get_db)):
    """Fetches assembly metadata and QC from NCBI Datasets API."""
    existing = db.query(Isolate).filter(Isolate.accession == accession).first()
    if existing:
        return {"status": "exists", "isolate_id": existing.id, "accession": accession}

    meta = ncbi_service.fetch_assembly_metadata(accession)
    iso = Isolate(**meta)
    db.add(iso)
    db.commit()
    db.refresh(iso)
    return {"status": "ingested", "isolate_id": iso.id, "accession": accession, "qc_status": iso.qc_status}

@router.post("/upload-fasta", summary="Upload & Analyze Raw FASTA Assembly")
async def upload_fasta(
    file: UploadFile = File(...),
    organism: str = Form("Klebsiella pneumoniae"),
    strain: Optional[str] = Form(None),
    country: Optional[str] = Form("Unknown"),
    city: Optional[str] = Form(None),
    isolation_source: Optional[str] = Form("Clinical"),
    db: Session = Depends(get_db)
):
    """
    Accepts raw FASTA/FNA genome assemblies, calculates SHA256 checksums,
    N50, GC content, contig count, evaluates taxonomic QC, screens AMR cassettes,
    and registers the isolate.
    """
    try:
        contents = await file.read()
        analysis = fasta_service.analyze_fasta_content(contents, file.filename, organism)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse FASTA file: {str(e)}")

    clean_filename = file.filename.rsplit(".", 1)[0].replace(" ", "_")
    accession = f"LOCAL_{clean_filename}_{int(time.time())}"

    iso = Isolate(
        accession=accession,
        sample_id=f"SAMPLE_{clean_filename}",
        organism=organism,
        strain=strain or clean_filename,
        country=country,
        city=city,
        isolation_source=isolation_source,
        collection_date=datetime.date.today(),
        collection_year=datetime.date.today().year,
        assembly_level="Contig" if analysis["contig_count"] > 1 else "Complete Genome",
        genome_size=analysis["genome_size"],
        gc_percent=analysis["gc_percent"],
        n50=analysis["n50"],
        contig_count=analysis["contig_count"],
        qc_status=analysis["qc_status"],
        qc_notes=analysis["qc_notes"],
        checksum_sha256=analysis["checksum_sha256"],
        provenance_source=analysis["provenance_source"]
    )
    db.add(iso)
    db.flush()

    # Add detected AMR determinants
    created_amr = []
    for amr_det in analysis["detected_amr"]:
        det = AMRDeterminant(
            isolate_id=iso.id,
            gene_symbol=amr_det["gene_symbol"],
            gene_family=amr_det["gene_family"],
            drug_class=amr_det["drug_class"],
            subclass=amr_det["subclass"],
            element_type="GENE",
            confidence=amr_det["confidence"],
            predicted_context=amr_det["predicted_context"],
            contig_id=amr_det["contig_id"]
        )
        db.add(det)
        created_amr.append(amr_det["gene_symbol"])

    # Basic molecular type tag
    mol = MolecularType(
        isolate_id=iso.id,
        scheme="PASTEUR",
        sequence_type="ST-Local",
        kleborate_virulence_score=1,
        kleborate_resistance_score=len(created_amr)
    )
    db.add(mol)
    db.commit()
    db.refresh(iso)

    return {
        "status": "success",
        "isolate_id": iso.id,
        "accession": iso.accession,
        "organism": iso.organism,
        "strain": iso.strain,
        "genome_size": iso.genome_size,
        "gc_percent": iso.gc_percent,
        "n50": iso.n50,
        "contig_count": iso.contig_count,
        "qc_status": iso.qc_status,
        "qc_notes": iso.qc_notes,
        "detected_amr": created_amr
    }


