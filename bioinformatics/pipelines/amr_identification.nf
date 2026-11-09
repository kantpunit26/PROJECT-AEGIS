#!/usr/bin/env nextflow
nextflow.enable.dsl=2

/*
========================================================================================
   PROJECT AEGIS 2.0 — NCBI AMRFinderPlus PIPELINE
   Identifies acquired resistance genes, point mutations, and virulence determinants
========================================================================================
*/

params.assemblies = "${projectDir}/../../data/raw/assemblies/*.fna"
params.organism   = "Klebsiella_pneumoniae"
params.outdir     = "${projectDir}/../../data/processed/amrfinder"

process AMRFINDER_PLUS {
    tag "$sample_id"
    publishDir "${params.outdir}", mode: 'copy'

    input:
    tuple val(sample_id), path(fasta)

    output:
    tuple val(sample_id), path("${sample_id}_amrfinder.tsv")

    script:
    """
    amrfinder \\
        -n ${fasta} \\
        -O ${params.organism} \\
        --plus \\
        --threads ${task.cpus} \\
        --output ${sample_id}_amrfinder.tsv
    """
}

workflow {
    ch_assemblies = Channel.fromPath(params.assemblies)
        .map { file -> tuple(file.baseName, file) }

    AMRFINDER_PLUS(ch_assemblies)
}

