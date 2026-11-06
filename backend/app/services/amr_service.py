from typing import List, Dict, Any, Optional
from collections import Counter
from sqlalchemy.orm import Session
from app.models.isolate import Isolate
from app.models.amr import AMRDeterminant

# Verified AMRFinderPlus Gene Classification Catalog
AMR_CLASSIFICATION_RULES = {
    # Carbapenemases
    "blaKPC": {"family": "KPC carbapenemase", "class": "Beta-lactam", "subclass": "Carbapenem"},
    "blaNDM": {"family": "Metallo-beta-lactamase", "class": "Beta-lactam", "subclass": "Carbapenem"},
    "blaOXA-48": {"family": "OXA-48-like carbapenemase", "class": "Beta-lactam", "subclass": "Carbapenem"},
    "blaOXA-181": {"family": "OXA-48-like carbapenemase", "class": "Beta-lactam", "subclass": "Carbapenem"},
    "blaOXA-232": {"family": "OXA-48-like carbapenemase", "class": "Beta-lactam", "subclass": "Carbapenem"},
    "blaVIM": {"family": "Metallo-beta-lactamase", "class": "Beta-lactam", "subclass": "Carbapenem"},
    "blaIMP": {"family": "Metallo-beta-lactamase", "class": "Beta-lactam", "subclass": "Carbapenem"},

    # Extended-Spectrum Beta-Lactamases (ESBL)
    "blaCTX-M": {"family": "CTX-M ESBL", "class": "Beta-lactam", "subclass": "Cephalosporin"},
    "blaSHV-12": {"family": "SHV ESBL", "class": "Beta-lactam", "subclass": "Cephalosporin"},
    "blaTEM": {"family": "TEM beta-lactamase", "class": "Beta-lactam", "subclass": "Penicillin/Cephalosporin"},

    # Colistin Resistance
    "mcr": {"family": "Phosphoethanolamine transferase", "class": "Polymyxin", "subclass": "Colistin"},
    "mgrB": {"family": "Lipid A regulator disruption", "class": "Polymyxin", "subclass": "Colistin"},

    # Aminoglycoside Resistance
    "armA": {"family": "16S rRNA methyltransferase", "class": "Aminoglycoside", "subclass": "Pan-aminoglycoside"},
    "rmt": {"family": "16S rRNA methyltransferase", "class": "Aminoglycoside", "subclass": "Pan-aminoglycoside"},
    "aac": {"family": "Aminoglycoside acetyltransferase", "class": "Aminoglycoside", "subclass": "Aminoglycoside"},
    "aad": {"family": "Aminoglycoside adenyltransferase", "class": "Aminoglycoside", "subclass": "Aminoglycoside"},
    "aph": {"family": "Aminoglycoside phosphotransferase", "class": "Aminoglycoside", "subclass": "Aminoglycoside"},

    # Fluoroquinolone Resistance
    "GyrA": {"family": "DNA gyrase mutation", "class": "Fluoroquinolone", "subclass": "Fluoroquinolone"},
    "ParC": {"family": "Topoisomerase IV mutation", "class": "Fluoroquinolone", "subclass": "Fluoroquinolone"},
    "qnr": {"family": "Pentapeptide repeat protein", "class": "Fluoroquinolone", "subclass": "Fluoroquinolone"},

    # Efflux Systems
    "acrA": {"family": "RND efflux pump membrane fusion", "class": "Multidrug Efflux", "subclass": "Multidrug"},
    "acrB": {"family": "RND efflux pump transporter", "class": "Multidrug Efflux", "subclass": "Multidrug"},
    "oqxA": {"family": "RND efflux pump subunit", "class": "Multidrug Efflux", "subclass": "Fluoroquinolone/Phenicol"},
    "oqxB": {"family": "RND efflux pump subunit", "class": "Multidrug Efflux", "subclass": "Fluoroquinolone/Phenicol"},
}

class AMRAnalysisService:
    """AMRFinderPlus determinant processing, prevalence aggregation, and co-occurrence computation."""

    @staticmethod
    def classify_determinant(gene_symbol: str) -> Dict[str, str]:
        """Maps an AMRFinderPlus gene symbol to functional family, class, and subclass."""
        for pattern, info in AMR_CLASSIFICATION_RULES.items():
            if pattern.lower() in gene_symbol.lower():
                return info
        return {"family": "Other AMR Determinant", "class": "Unclassified", "subclass": "Unclassified"}

    @staticmethod
    def get_amr_prevalence(db: Session, organism: Optional[str] = None) -> Dict[str, Any]:
        """Calculates population prevalence percentage of all detected AMR determinants."""
        query = db.query(Isolate)
        if organism:
            query = query.filter(Isolate.organism == organism)
        
        total_isolates = query.count()
        if total_isolates == 0:
            return {"total_isolates": 0, "determinants": []}

        # Query all determinants for these isolates
        iso_ids = [i.id for i in query.all()]
        determinants = db.query(AMRDeterminant).filter(AMRDeterminant.isolate_id.in_(iso_ids)).all()

        counts = Counter([d.gene_symbol for d in determinants])
        items = []
        for gene, count in counts.most_common():
            # Get metadata for this gene
            sample_det = next(d for d in determinants if d.gene_symbol == gene)
            items.append({
                "gene_symbol": gene,
                "gene_family": sample_det.gene_family,
                "drug_class": sample_det.drug_class,
                "subclass": sample_det.subclass,
                "count": count,
                "prevalence_percent": round((count / total_isolates) * 100.0, 2)
            })

        return {
            "total_isolates": total_isolates,
            "determinants": items
        }

    @staticmethod
    def get_amr_co_occurrence(db: Session, top_n: int = 10) -> Dict[str, Any]:
        """Computes pairwise co-occurrence matrix for high-frequency resistance genes."""
        determinants = db.query(AMRDeterminant).all()
        gene_counts = Counter([d.gene_symbol for d in determinants])
        top_genes = [g for g, _ in gene_counts.most_common(top_n)]

        # Map isolates to genes
        iso_genes: Dict[str, set] = {}
        for d in determinants:
            if d.isolate_id not in iso_genes:
                iso_genes[d.isolate_id] = set()
            iso_genes[d.isolate_id].add(d.gene_symbol)

        matrix = []
        for g1 in top_genes:
            row = []
            for g2 in top_genes:
                co_occur = sum(1 for genes in iso_genes.values() if g1 in genes and g2 in genes)
                row.append(co_occur)
            matrix.append(row)

        return {
            "genes": top_genes,
            "matrix": matrix
        }

amr_service = AMRAnalysisService()
