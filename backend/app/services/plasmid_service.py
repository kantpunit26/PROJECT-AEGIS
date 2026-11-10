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

    @staticmethod
    def get_resistome_mobilization_sankey() -> Dict[str, Any]:
        """
        Sankey (Alluvial) flow diagram tracking ARG mobilization from Klebsiella pneumoniae
        clonal lineages through specific resistance gene subtypes to plasmid mobility status.
        """
        nodes = [
            # Lineages (0-5)
            {"id": "lin_st11", "name": "ST11 (Asian CRKP)", "stage": 0, "color": "#f97316"},
            {"id": "lin_st147", "name": "ST147 (South Asian NDM)", "stage": 0, "color": "#ec4899"},
            {"id": "lin_st258", "name": "ST258 (US/EU KPC)", "stage": 0, "color": "#10b981"},
            {"id": "lin_st15", "name": "ST15 (European Clade)", "stage": 0, "color": "#38bdf8"},
            {"id": "lin_st307", "name": "ST307 (Global Clade)", "stage": 0, "color": "#a855f7"},
            {"id": "lin_st23", "name": "ST23 (Hypervirulent hvKP)", "stage": 0, "color": "#eab308"},

            # ARG Subtypes (6-16)
            {"id": "arg_ndm5", "name": "blaNDM-5", "stage": 1, "color": "#e11d48"},
            {"id": "arg_kpc2", "name": "blaKPC-2", "stage": 1, "color": "#e11d48"},
            {"id": "arg_oxa181", "name": "blaOXA-181", "stage": 1, "color": "#f43f5e"},
            {"id": "arg_ctxm15", "name": "blaCTX-M-15", "stage": 1, "color": "#fb7185"},
            {"id": "arg_rmtb", "name": "rmtB", "stage": 1, "color": "#38bdf8"},
            {"id": "arg_arma", "name": "armA", "stage": 1, "color": "#0ea5e9"},
            {"id": "arg_mgrb", "name": "mgrB (IS-interrupted)", "stage": 1, "color": "#818cf8"},
            {"id": "arg_fosa", "name": "fosA", "stage": 1, "color": "#64748b"},
            {"id": "arg_oqxab", "name": "oqxAB", "stage": 1, "color": "#94a3b8"},
            {"id": "arg_sul2", "name": "sul2", "stage": 1, "color": "#fb923c"},
            {"id": "arg_teta", "name": "tet(A)", "stage": 1, "color": "#fdba74"},

            # Mobility Status (17-19)
            {"id": "mob_mobile", "name": "Mobile (Conjugative / Mobilizable Plasmids)", "stage": 2, "color": "#e11d48"},
            {"id": "mob_transposon", "name": "Transposon-Associated (Composite / Integrative)", "stage": 2, "color": "#f59e0b"},
            {"id": "mob_immobile", "name": "Immobile (Chromosomal / Intrinsic)", "stage": 2, "color": "#3b82f6"},
        ]

        links = [
            # Lineage -> ARG
            {"source": "lin_st11", "target": "arg_kpc2", "value": 36},
            {"source": "lin_st11", "target": "arg_rmtb", "value": 28},
            {"source": "lin_st11", "target": "arg_mgrb", "value": 14},
            {"source": "lin_st11", "target": "arg_fosa", "value": 42},
            {"source": "lin_st11", "target": "arg_oqxab", "value": 42},
            {"source": "lin_st147", "target": "arg_ndm5", "value": 30},
            {"source": "lin_st147", "target": "arg_oxa181", "value": 26},
            {"source": "lin_st147", "target": "arg_arma", "value": 24},
            {"source": "lin_st147", "target": "arg_ctxm15", "value": 28},
            {"source": "lin_st147", "target": "arg_sul2", "value": 25},
            {"source": "lin_st147", "target": "arg_fosa", "value": 30},
            {"source": "lin_st258", "target": "arg_kpc2", "value": 38},
            {"source": "lin_st258", "target": "arg_teta", "value": 22},
            {"source": "lin_st258", "target": "arg_fosa", "value": 38},
            {"source": "lin_st15", "target": "arg_ctxm15", "value": 20},
            {"source": "lin_st15", "target": "arg_sul2", "value": 18},
            {"source": "lin_st15", "target": "arg_fosa", "value": 22},
            {"source": "lin_st307", "target": "arg_kpc2", "value": 16},
            {"source": "lin_st307", "target": "arg_ctxm15", "value": 19},
            {"source": "lin_st307", "target": "arg_fosa", "value": 19},
            {"source": "lin_st23", "target": "arg_fosa", "value": 14},
            {"source": "lin_st23", "target": "arg_oqxab", "value": 14},

            # ARG -> Mobility Status
            {"source": "arg_ndm5", "target": "mob_mobile", "value": 30},
            {"source": "arg_kpc2", "target": "mob_mobile", "value": 90},
            {"source": "arg_oxa181", "target": "mob_mobile", "value": 26},
            {"source": "arg_ctxm15", "target": "mob_mobile", "value": 52},
            {"source": "arg_rmtb", "target": "mob_mobile", "value": 28},
            {"source": "arg_arma", "target": "mob_mobile", "value": 24},
            {"source": "arg_sul2", "target": "mob_transposon", "value": 43},
            {"source": "arg_teta", "target": "mob_transposon", "value": 22},
            {"source": "arg_mgrb", "target": "mob_transposon", "value": 14},
            {"source": "arg_fosa", "target": "mob_immobile", "value": 165},
            {"source": "arg_oqxab", "target": "mob_immobile", "value": 56},
        ]

        return {
            "title": "ARG Mobilization & Horizontal Gene Transfer (Alluvial Flow)",
            "nodes": nodes,
            "links": links
        }

    @staticmethod
    def get_chromosome_vs_plasmid_heatmaps() -> Dict[str, Any]:
        """
        Side-by-side Dual Heatmap (Chromosome vs. Plasmid Partitioned Resistome)
        displaying ARG copy numbers, drug classes, and resistance mechanisms across clinical isolates.
        """
        isolate_accessions = [
            "HS11286 (ST11)", "SH-KP-02 (ST11)", "HZ-KP-09 (ST11)", "BJ-KP-14 (ST11)",
            "VAD-01 (ST147)", "VAD-04 (ST147)", "DEL-11 (ST147)", "MUM-08 (ST147)",
            "BOS-44 (ST258)", "NYC-12 (ST258)", "HOU-22 (ST258)", "CHI-07 (ST258)",
            "PAR-03 (ST15)", "BER-19 (ST15)", "MIL-18 (ST307)", "ROM-05 (ST307)",
            "MGH-78578 (ST38)", "TPE-01 (ST23)", "SGP-04 (ST23)", "LON-16 (ST16)"
        ]

        # Panel A: Chromosomal Resistome
        chrom_genes = [
            {"name": "blaSHV-1 / 11", "drug_class": "Beta-lactam", "mechanism": "Inactivation", "class_color": "#e11d48"},
            {"name": "oqxA", "drug_class": "Fluoroquinolone", "mechanism": "Efflux", "class_color": "#0ea5e9"},
            {"name": "oqxB", "drug_class": "Fluoroquinolone", "mechanism": "Efflux", "class_color": "#0ea5e9"},
            {"name": "fosA", "drug_class": "Fosfomycin", "mechanism": "Inactivation", "class_color": "#a855f7"},
            {"name": "acrA", "drug_class": "MDR", "mechanism": "Efflux", "class_color": "#3b82f6"},
            {"name": "acrB", "drug_class": "MDR", "mechanism": "Efflux", "class_color": "#3b82f6"},
            {"name": "tolC", "drug_class": "MDR", "mechanism": "Efflux", "class_color": "#3b82f6"},
            {"name": "GyrA_S83I", "drug_class": "Fluoroquinolone", "mechanism": "Target Alteration", "class_color": "#0ea5e9"},
            {"name": "ParC_S80I", "drug_class": "Fluoroquinolone", "mechanism": "Target Alteration", "class_color": "#0ea5e9"},
            {"name": "mgrB_disruption", "drug_class": "Polymyxin", "mechanism": "Target Alteration", "class_color": "#ec4899"},
            {"name": "ompK36_deficiency", "drug_class": "Beta-lactam", "mechanism": "Reduced Permeability", "class_color": "#e11d48"},
        ]

        # Matrix [gene_index][isolate_index] (copy number 0, 1, 2)
        chrom_matrix = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # blaSHV (intrinsic core)
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # oqxA
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # oqxB
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # fosA
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # acrA
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # acrB
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # tolC
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1], # GyrA
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0], # ParC
            [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # mgrB mut (colistin res)
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0], # ompK36 porin loss
        ]

        # Panel B: Plasmid-Borne Acquired Resistome
        plasmid_genes = [
            {"name": "blaKPC-2", "drug_class": "Carbapenem", "mechanism": "Inactivation", "class_color": "#e11d48"},
            {"name": "blaKPC-3", "drug_class": "Carbapenem", "mechanism": "Inactivation", "class_color": "#e11d48"},
            {"name": "blaNDM-5", "drug_class": "Carbapenem", "mechanism": "Inactivation", "class_color": "#e11d48"},
            {"name": "blaOXA-181", "drug_class": "Carbapenem", "mechanism": "Inactivation", "class_color": "#f43f5e"},
            {"name": "blaOXA-48", "drug_class": "Carbapenem", "mechanism": "Inactivation", "class_color": "#f43f5e"},
            {"name": "blaCTX-M-15", "drug_class": "Cephalosporin", "mechanism": "Inactivation", "class_color": "#fb7185"},
            {"name": "blaCTX-M-65", "drug_class": "Cephalosporin", "mechanism": "Inactivation", "class_color": "#fb7185"},
            {"name": "rmtB", "drug_class": "Aminoglycoside", "mechanism": "Target Protection", "class_color": "#38bdf8"},
            {"name": "armA", "drug_class": "Aminoglycoside", "mechanism": "Target Protection", "class_color": "#0ea5e9"},
            {"name": "aac(6')-Ib-cr", "drug_class": "Aminoglycoside", "mechanism": "Inactivation", "class_color": "#0ea5e9"},
            {"name": "sul1", "drug_class": "Sulfonamide", "mechanism": "Target Replacement", "class_color": "#fb923c"},
            {"name": "sul2", "drug_class": "Sulfonamide", "mechanism": "Target Replacement", "class_color": "#fb923c"},
            {"name": "tet(A)", "drug_class": "Tetracycline", "mechanism": "Efflux", "class_color": "#fdba74"},
            {"name": "dfrA14", "drug_class": "Diaminopyrimidine", "mechanism": "Target Replacement", "class_color": "#a855f7"},
            {"name": "mphA", "drug_class": "Macrolide", "mechanism": "Inactivation", "class_color": "#10b981"},
            {"name": "catB4", "drug_class": "Phenicol", "mechanism": "Inactivation", "class_color": "#cbd5e1"},
        ]

        # Matrix [gene_index][isolate_index] (copy numbers: 0, 1, 2, 3)
        plasmid_matrix = [
            [2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0], # blaKPC-2
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], # blaKPC-3
            [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # blaNDM-5
            [0, 0, 0, 0, 3, 3, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # blaOXA-181
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0], # blaOXA-48
            [0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1], # blaCTX-M-15
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # blaCTX-M-65
            [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # rmtB
            [0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # armA
            [1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1], # aac(6')-Ib-cr
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1], # sul1
            [1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], # sul2
            [1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 1, 1, 0, 0, 0, 0], # tet(A)
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0], # dfrA14
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0], # mphA
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], # catB4
        ]

        return {
            "title": "Partitioned Resistome Architecture (Chromosome vs. Plasmid)",
            "isolates": isolate_accessions,
            "chromosomal": {
                "genes": chrom_genes,
                "matrix": chrom_matrix
            },
            "plasmid": {
                "genes": plasmid_genes,
                "matrix": plasmid_matrix
            }
        }


plasmid_service = PlasmidService()

