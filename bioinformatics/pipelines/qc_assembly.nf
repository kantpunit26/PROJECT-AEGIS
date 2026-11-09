#!/usr/bin/env nextflow
nextflow.enable.dsl=2

/*
========================================================================================
   PROJECT AEGIS 2.0 — ASSEMBLY QUALITY CONTROL PIPELINE
   Executes QUAST metrics, contig length filtering, and taxonomic GC checks
========================================================================================
*/

params.assemblies = "${projectDir}/../../data/raw/assemblies/*.fna"
params.outdir     = "${projectDir}/../../data/processed/qc"

process QUAST_QC {
    tag "$sample_id"
    publishDir "${params.outdir}/${sample_id}", mode: 'copy'

    input:
    tuple val(sample_id), path(fasta)

    output:
    tuple val(sample_id), path("report.tsv"), path("transposed_report.tsv")

    script:
    """
    quast.py ${fasta} \\
        -o . \\
        --threads ${task.cpus} \\
        --min-contig 500 \\
        --k-mer-stats
    """
}

workflow {
    ch_assemblies = Channel.fromPath(params.assemblies)
        .map { file -> tuple(file.baseName, file) }

    QUAST_QC(ch_assemblies)
}

