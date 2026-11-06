from typing import Dict, Any, Tuple

# Quality Control Thresholds for Klebsiella pneumoniae & Enterobacteriaceae
QC_SPECIFICATIONS = {
    "Klebsiella pneumoniae": {
        "min_genome_size": 5_000_000,
        "max_genome_size": 6_000_000,
        "min_gc_percent": 56.0,
        "max_gc_percent": 59.0,
        "min_n50": 30_000,
        "max_contig_count": 500,
    },
    "Escherichia coli": {
        "min_genome_size": 4_400_000,
        "max_genome_size": 5_800_000,
        "min_gc_percent": 49.5,
        "max_gc_percent": 52.0,
        "min_n50": 25_000,
        "max_contig_count": 500,
    },
    "Acinetobacter baumannii": {
        "min_genome_size": 3_600_000,
        "max_genome_size": 4_400_000,
        "min_gc_percent": 38.0,
        "max_gc_percent": 40.5,
        "min_n50": 20_000,
        "max_contig_count": 400,
    }
}

def evaluate_assembly_qc(
    organism: str,
    genome_size: int,
    gc_percent: float,
    n50: int,
    contig_count: int
) -> Tuple[str, str]:
    """
    Evaluates assembly quality against taxon-specific biological parameters.
    Returns (qc_status, qc_notes), where qc_status is 'PASS', 'WARNING', or 'FAIL'.
    """
    specs = QC_SPECIFICATIONS.get(organism, QC_SPECIFICATIONS["Klebsiella pneumoniae"])
    flags = []

    # Genome size check
    if genome_size < specs["min_genome_size"] * 0.85 or genome_size > specs["max_genome_size"] * 1.25:
        flags.append(f"Genome size {genome_size:,} bp deviates severely from expected range [{specs['min_genome_size']:,} - {specs['max_genome_size']:,} bp].")
        return "FAIL", "; ".join(flags)
    elif genome_size < specs["min_genome_size"] or genome_size > specs["max_genome_size"]:
        flags.append(f"Genome size {genome_size:,} bp slightly outside canonical boundaries.")

    # GC content check (contamination indicator)
    if gc_percent < specs["min_gc_percent"] - 2.0 or gc_percent > specs["max_gc_percent"] + 2.0:
        flags.append(f"GC content {gc_percent:.1f}% indicates potential inter-species taxonomic contamination.")
        return "FAIL", "; ".join(flags)
    elif gc_percent < specs["min_gc_percent"] or gc_percent > specs["max_gc_percent"]:
        flags.append(f"GC content {gc_percent:.1f}% deviates from typical {organism} profile.")

    # Contig fragmentation & N50
    if n50 < specs["min_n50"] or contig_count > specs["max_contig_count"]:
        flags.append(f"High fragmentation: N50={n50:,} bp, contigs={contig_count}.")
        return "WARNING", "; ".join(flags)

    if not flags:
        return "PASS", "Assembly satisfies all rigorous completeness and taxonomic conformity checks."
    
    return "WARNING", "; ".join(flags)
