from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.comparative import PhylogeneticTree
from app.models.isolate import Isolate

class PhylogeneticsService:
    """Manages IQ-TREE Maximum-Likelihood trees, substitution model records, and metadata tracks."""

    @staticmethod
    def get_default_tree(db: Session, organism: str = "Klebsiella pneumoniae") -> Optional[Dict[str, Any]]:
        tree = db.query(PhylogeneticTree).filter(PhylogeneticTree.organism == organism).first()
        if not tree:
            return None

        # Gather isolate metadata tracks
        isolates = db.query(Isolate).filter(Isolate.organism == organism).all()
        tracks = {
            "ST": {},
            "Country": {},
            "Carbapenemase": {},
            "IsolationSource": {},
            "VirulenceScore": {}
        }
        for iso in isolates:
            tracks["Country"][iso.accession] = iso.country or "Unknown"
            tracks["IsolationSource"][iso.accession] = iso.isolation_source or "Unknown"
            if iso.molecular_types:
                tracks["ST"][iso.accession] = iso.molecular_types[0].sequence_type
                tracks["VirulenceScore"][iso.accession] = iso.molecular_types[0].kleborate_virulence_score or 0
            carbs = [d.gene_symbol for d in iso.amr_determinants if d.subclass == "Carbapenem"]
            tracks["Carbapenemase"][iso.accession] = ", ".join(carbs) if carbs else "Negative"

        return {
            "id": tree.id,
            "tree_name": tree.tree_name,
            "organism": tree.organism,
            "newick_string": tree.newick_string,
            "substitution_model": tree.substitution_model,
            "log_likelihood": tree.log_likelihood,
            "bootstrap_replicates": tree.bootstrap_replicates,
            "metadata_tracks": tracks,
            "created_at": tree.created_at
        }

phylo_service = PhylogeneticsService()

