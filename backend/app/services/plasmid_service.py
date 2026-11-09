from typing import List, Dict, Any, Optional
from collections import Counter
from sqlalchemy.orm import Session
from app.models.plasmid import Plasmid
from app.models.isolate import Isolate
from app.models.amr import AMRDeterminant

class PlasmidService:
    """MOB-suite replicon profiling, mobility typing, and chromosome-vs-plasmid AMR partitioning."""

    @staticmethod
    def get_plasmid_summary(db: Session) -> Dict[str, Any]:
        plasmids = db.query(Plasmid).all()
        total_plasmids = len(plasmids)
        
        # Replicon family distribution
        replicons_flat = []
        for p in plasmids:
            if p.replicon_types:
                replicons_flat.extend(p.replicon_types)
        
        replicon_counts = Counter(replicons_flat)
        mobility_counts = Counter([p.mobility for p in plasmids])

        return {
            "total_plasmids": total_plasmids,
            "mobility_distribution": dict(mobility_counts),
            "replicon_prevalence": [
                {"replicon": rep, "count": count, "percentage": round((count / max(1, total_plasmids)) * 100.0, 1)}
                for rep, count in replicon_counts.most_common()
            ]
        }

    @staticmethod
    def get_chromosome_vs_plasmid_matrix(db: Session) -> Dict[str, Any]:
        """Calculates genomic context partitioning (Chromosome vs. Plasmid vs. Unknown) for AMR classes."""
        determinants = db.query(AMRDeterminant).all()
        classes = sorted(list(set(d.drug_class for d in determinants)))

        matrix = []
        for drug_cls in classes:
            class_dets = [d for d in determinants if d.drug_class == drug_cls]
            chrom_count = sum(1 for d in class_dets if d.predicted_context == "CHROMOSOME")
            plasmid_count = sum(1 for d in class_dets if d.predicted_context == "PLASMID")
            unknown_count = sum(1 for d in class_dets if d.predicted_context not in ("CHROMOSOME", "PLASMID"))
            total = len(class_dets)

            matrix.append({
                "drug_class": drug_cls,
                "total": total,
                "chromosome_count": chrom_count,
                "plasmid_count": plasmid_count,
                "unknown_count": unknown_count,
                "plasmid_percentage": round((plasmid_count / total) * 100.0, 1) if total > 0 else 0.0
            })

        return {
            "categories": classes,
            "data": matrix
        }

plasmid_service = PlasmidService()

