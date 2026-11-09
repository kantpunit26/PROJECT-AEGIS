#!/usr/bin/env nextflow
nextflow.enable.dsl=2

/*
========================================================================================
   PROJECT AEGIS — CORE-GENOME SNP & PHYLOGENETICS PIPELINE
   Reference alignment (Snippy/Parsnp), SNP distance matrix, and IQ-TREE inference
========================================================================================
*/

params.assemblies       = "${projectDir}/../../data/raw/assemblies/*.fna"
params.reference_genome = "${projectDir}/../../data/reference/HS11286.fna"
params.outdir           = "${projectDir}/../../data/processed/comparative"

process SNIPPY_ALIGN {
    tag "$sample_id"

    input:
    tuple val(sample_id), path(fasta)
    path ref

    output:
    tuple val(sample_id), path("${sample_id}/snps.consensus.fa"), path("${sample_id}/snps.tab")

    script:
    """
    snippy --cpus ${task.cpus} --outdir ${sample_id} --ref ${ref} --ctgs ${fasta}
    """
}

process SNIPPY_CORE {
    publishDir "${params.outdir}", mode: 'copy'

    input:
    path consensus_dirs
    path ref

    output:
    path "core.full.aln", emit: full_aln
    path "core.aln", emit: clean_aln
    path "snp_distance_matrix.tsv", emit: distance_matrix

    script:
    """
    snippy-core --ref ${ref} ${consensus_dirs}
    snp-dists -m core.aln > snp_distance_matrix.tsv
    """
}

process IQTREE_PHYLOGENY {
    publishDir "${params.outdir}", mode: 'copy'

    input:
    path clean_aln

    output:
    path "aegis_phylogeny.treefile", emit: treefile
    path "aegis_phylogeny.iqtree", emit: log

    script:
    """
    iqtree2 \\
        -s ${clean_aln} \\
        -m ${params.iqtree_model} \\
        -B ${params.iqtree_bootstrap} \\
        --alrt 1000 \\
        -T AUTO \\
        --prefix aegis_phylogeny
    """
}

workflow {
    ch_assemblies = Channel.fromPath(params.assemblies)
        .map { file -> tuple(file.baseName, file) }
    ch_ref = file(params.reference_genome)

    snippy_out = SNIPPY_ALIGN(ch_assemblies, ch_ref)
    core_out   = SNIPPY_CORE(snippy_out.map{ it[1] }.collect(), ch_ref)
    IQTREE_PHYLOGENY(core_out.clean_aln)
}

