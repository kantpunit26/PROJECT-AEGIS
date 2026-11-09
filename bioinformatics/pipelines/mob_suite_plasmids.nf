#!/usr/bin/env nextflow
nextflow.enable.dsl=2

/*
========================================================================================
   PROJECT AEGIS 2.0 — MOB-SUITE PLASMID RECONSTRUCTION PIPELINE
   Disentangles chromosomal vs. plasmid contigs and determines replicon incompatibility
========================================================================================
*/

params.assemblies = "${projectDir}/../../data/raw/assemblies/*.fna"
params.outdir     = "${projectDir}/../../data/processed/plasmids"

process MOB_RECON {
    tag "$sample_id"
    publishDir "${params.outdir}/${sample_id}", mode: 'copy'

    input:
    tuple val(sample_id), path(fasta)

    output:
    tuple val(sample_id), path("chromosome.fasta"), path("plasmid_*.fasta"), optional: true
    path "mobtyper_results.txt"

    script:
    """
    mob_recon \\
        --infile ${fasta} \\
        --outdir . \\
        --num_threads ${task.cpus} \\
        --run_typer
    """
}

workflow {
    ch_assemblies = Channel.fromPath(params.assemblies)
        .map { file -> tuple(file.baseName, file) }

    MOB_RECON(ch_assemblies)
}

