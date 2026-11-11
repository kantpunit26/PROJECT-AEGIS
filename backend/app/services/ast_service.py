from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.ast import ASTRecord
from app.models.amr import AMRDeterminant
from app.models.isolate import Isolate

class ASTValidationService:
    """Evaluates genotype vs phenotype antimicrobial susceptibility concordance and diagnostic accuracy."""

    @staticmethod
    def calculate_concordance_metrics(
        db: Session,
        antibiotic: Optional[str] = None,
        organism: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query = db.query(ASTRecord)
        if organism:
            query = query.join(Isolate, ASTRecord.isolate_id == Isolate.id).filter(Isolate.organism.ilike(f"%{organism}%"))
        if antibiotic:
            query = query.filter(ASTRecord.antibiotic == antibiotic)

        records = query.all()
        if not records:
            return []

        # Group by antibiotic
        antibiotics = sorted(list(set(r.antibiotic for r in records)))
        metrics_list = []

        for ab in antibiotics:
            ab_records = [r for r in records if r.antibiotic == ab]
            tp = sum(1 for r in ab_records if r.phenotype == "R" and r.genotypic_prediction == "R")
            tn = sum(1 for r in ab_records if r.phenotype in ("S", "I") and r.genotypic_prediction == "S")
            me = sum(1 for r in ab_records if r.phenotype in ("S", "I") and r.genotypic_prediction == "R") # False Positive
            vme = sum(1 for r in ab_records if r.phenotype == "R" and r.genotypic_prediction == "S")      # False Negative
            total = len(ab_records)

            sensitivity = round((tp / (tp + vme)) * 100.0, 2) if (tp + vme) > 0 else 100.0
            specificity = round((tn / (tn + me)) * 100.0, 2) if (tn + me) > 0 else 100.0
            precision_ppv = round((tp / (tp + me)) * 100.0, 2) if (tp + me) > 0 else 100.0
            concordance = round(((tp + tn) / total) * 100.0, 2) if total > 0 else 100.0

            metrics_list.append({
                "antibiotic": ab,
                "total_tested": total,
                "true_positive_resistant": tp,
                "true_negative_susceptible": tn,
                "major_error_false_resistant": me,
                "very_major_error_false_susceptible": vme,
                "sensitivity": sensitivity,
                "specificity": specificity,
                "precision_ppv": precision_ppv,
                "concordance_rate": concordance,
                "confusion_matrix": {
                    "predicted_resistant": {"actual_resistant": tp, "actual_susceptible": me},
                    "predicted_susceptible": {"actual_resistant": vme, "actual_susceptible": tn}
                }
            })

        return metrics_list

ast_service = ASTValidationService()

