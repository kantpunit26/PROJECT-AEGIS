from typing import Dict, Any, List, Optional
from collections import Counter
from sqlalchemy.orm import Session
from app.models.isolate import Isolate
from app.models.typing import MolecularType
from app.models.amr import AMRDeterminant

class MolecularTypingService:
    """Manages 7-gene MLST lineage classification and Kleborate virulence distributions."""

    @staticmethod
    def get_mlst_distribution(db: Session, organism: Optional[str] = None) -> List[Dict[str, Any]]:
        query = db.query(MolecularType).join(Isolate)
        if organism:
            query = query.filter(Isolate.organism == organism)
        
        types = query.all()
        total = len(types)
        if total == 0:
            return []

        counts = Counter([t.sequence_type for t in types])
        results = []
        for st, count in counts.most_common():
            # Find predominant carbapenemase associated with this ST
            st_iso_ids = [t.isolate_id for t in types if t.sequence_type == st]
            amrs = db.query(AMRDeterminant.gene_symbol).filter(
                AMRDeterminant.isolate_id.in_(st_iso_ids),
                AMRDeterminant.subclass == "Carbapenem"
            ).all()
            carb_counts = Counter([a[0] for a in amrs])
            predominant_carb = carb_counts.most_common(1)[0][0] if carb_counts else "None"

            results.append({
                "sequence_type": st,
                "count": count,
                "percentage": round((count / total) * 100.0, 2),
                "predominant_carbapenemase": predominant_carb
            })
        return results

    @staticmethod
    def get_kleborate_summary(db: Session) -> Dict[str, Any]:
        """Summarizes Kleborate 2D virulence vs. resistance score distributions."""
        records = db.query(MolecularType).all()
        # 6x4 matrix: virulence (0..5) x resistance (0..3)
        matrix = [[0 for _ in range(4)] for _ in range(6)]
        for r in records:
            v = min(max(r.kleborate_virulence_score or 0, 0), 5)
            res = min(max(r.kleborate_resistance_score or 0, 0), 3)
            matrix[v][res] += 1

        return {
            "virulence_scores": [0, 1, 2, 3, 4, 5],
            "resistance_scores": [0, 1, 2, 3],
            "distribution_matrix": matrix
        }

typing_service = MolecularTypingService()

