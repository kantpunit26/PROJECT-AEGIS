#!/usr/bin/env nextflow
nextflow.enable.dsl=2

/*
========================================================================================
   PROJECT AEGIS 2.0 — MOLECULAR TYPING & VIRULENCE PIPELINE
   Executes 7-gene Pasteur MLST and Kleborate capsule (K-locus) & siderophore profiling
========================================================================================
*/

params.assemblies = "${projectDir}/../../data/raw/assemblies/*.fna"
params.outdir     = "${projectDir}/../../data/processed/typing"

process MLST_TYPING {
    tag "$sample_id"

    input:
    tuple val(sample_id), path(fasta)

    output:
    tuple val(sample_id), path("${sample_id}_mlst.tsv")

    script:
    """
    mlst --scheme kpneumoniae ${fasta} > ${sample_id}_mlst.tsv
    """
}

process KLEBORATE_PROFILING {
    tag "$sample_id"
    publishDir "${params.outdir}", mode: 'copy'

    input:
    tuple val(sample_id), path(fasta)

    output:
    tuple val(sample_id), path("${sample_id}_kleborate.tsv")

    script:
    """
    kleborate \\
        --all \\
        --assemblies ${fasta} \\
        --outfile ${sample_id}_kleborate.tsv
    """
}

workflow {
    ch_assemblies = Channel.fromPath(params.assemblies)
        .map { file -> tuple(file.baseName, file) }

    MLST_TYPING(ch_assemblies)
    KLEBORATE_PROFILING(ch_assemblies)
}

