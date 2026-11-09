import io
import csv
import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.isolate import Isolate
from app.models.amr import AMRDeterminant
from app.models.ast import ASTRecord
from app.models.comparative import PhylogeneticTree

class SurveillanceExportService:
    """Exports genomic and epidemiological datasets in CSV, GeoJSON, JSON, Newick, and WHO GLASS formats."""

    @staticmethod
    def export_csv(db: Session, organism: Optional[str] = None) -> str:
        query = db.query(Isolate)
        if organism:
            query = query.filter(Isolate.organism == organism)
        isolates = query.all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Accession", "Sample_ID", "Organism", "Strain", "Collection_Date", "Collection_Year",
            "Isolation_Source", "Country", "State_Province", "City", "Latitude", "Longitude",
            "Sequence_Type", "K_Locus", "O_Locus", "Carbapenemases", "Colistin_Genes", "QC_Status"
        ])

        for iso in isolates:
            st = iso.molecular_types[0].sequence_type if iso.molecular_types else ""
            k_locus = iso.molecular_types[0].k_locus if iso.molecular_types else ""
            o_locus = iso.molecular_types[0].o_locus if iso.molecular_types else ""
            carbs = ";".join([d.gene_symbol for d in iso.amr_determinants if d.subclass == "Carbapenem"])
            col = ";".join([d.gene_symbol for d in iso.amr_determinants if d.subclass == "Colistin"])

            writer.writerow([
                iso.accession, iso.sample_id, iso.organism, iso.strain, iso.collection_date, iso.collection_year,
                iso.isolation_source, iso.country, iso.state_province, iso.city, iso.latitude, iso.longitude,
                st, k_locus, o_locus, carbs, col, iso.qc_status
            ])

        return output.getvalue()

    @staticmethod
    def export_geojson(db: Session, organism: Optional[str] = None) -> Dict[str, Any]:
        """Generates RFC 7946 compliant GeoJSON FeatureCollection."""
        query = db.query(Isolate).filter(Isolate.latitude.isnot(None), Isolate.longitude.isnot(None))
        if organism:
            query = query.filter(Isolate.organism == organism)
        isolates = query.all()

        features = []
        for iso in isolates:
            carbs = [d.gene_symbol for d in iso.amr_determinants if d.subclass == "Carbapenem"]
            st = iso.molecular_types[0].sequence_type if iso.molecular_types else None

            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [iso.longitude, iso.latitude]
                },
                "properties": {
                    "accession": iso.accession,
                    "organism": iso.organism,
                    "strain": iso.strain,
                    "country": iso.country,
                    "city": iso.city,
                    "collection_year": iso.collection_year,
                    "sequence_type": st,
                    "carbapenemases": carbs,
                    "qc_status": iso.qc_status
                }
            })

        return {
            "type": "FeatureCollection",
            "features": features
        }

    @staticmethod
    def export_who_glass_format(db: Session) -> List[Dict[str, Any]]:
        """
        Maps AST records into WHO Global Antimicrobial Resistance Surveillance System (GLASS)
        data submission format specifications.
        """
        records = db.query(ASTRecord).join(Isolate).all()
        glass_rows = []

        for r in records:
            iso = r.isolate
            # Map specimen type to GLASS standardized categories
            specimen_map = {
                "Blood": "BLOOD",
                "Urine": "URINE",
                "Sputum": "RESPIRATORY",
                "Rectal Swab": "STOOL",
                "Wound": "PUS_WOUND"
            }
            specimen = specimen_map.get(iso.isolation_source, "OTHER")

            glass_rows.append({
                "Country": iso.country,
                "Year": iso.collection_year,
                "Specimen": specimen,
                "Pathogen": "KLEPNE" if "pneumoniae" in iso.organism else "ESCCOL",
                "Antibacterial": r.antibiotic.upper(),
                "Testing_Method": r.testing_method or "MIC",
                "Standard": r.standard,
                "SIR_Result": r.phenotype,
                "Genotypic_Carbapenemase_Detected": any(d.subclass == "Carbapenem" for d in iso.amr_determinants)
            })

        return glass_rows

    @staticmethod
    def export_newick(db: Session, tree_id: Optional[str] = None) -> str:
        query = db.query(PhylogeneticTree)
        if tree_id:
            query = query.filter(PhylogeneticTree.id == tree_id)
        tree = query.first()
        return tree.newick_string if tree else "();"

export_service = SurveillanceExportService()

