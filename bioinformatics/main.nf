#!/usr/bin/env nextflow
nextflow.enable.dsl=2

/*
========================================================================================
   PROJECT AEGIS 2.0 — END-TO-END GENOMIC SURVEILLANCE MASTER PIPELINE
   Advanced Genomic Epidemiology & Intelligence System
========================================================================================
*/

include { QUAST_QC }            from './pipelines/qc_assembly.nf'
include { AMRFINDER_PLUS }      from './pipelines/amr_identification.nf'
include { MLST_TYPING }         from './pipelines/molecular_typing.nf'
include { KLEBORATE_PROFILING } from './pipelines/molecular_typing.nf'
include { SNIPPY_ALIGN }        from './pipelines/core_snp_alignment.nf'
include { SNIPPY_CORE }         from './pipelines/core_snp_alignment.nf'
include { IQTREE_PHYLOGENY }    from './pipelines/core_snp_alignment.nf'
include { MOB_RECON }           from './pipelines/mob_suite_plasmids.nf'

params.assemblies       = "${projectDir}/../data/sample_datasets/klebsiella_pneumoniae/*.fna"
params.reference_genome = "${projectDir}/../data/reference/HS11286.fna"
params.outdir           = "${projectDir}/../data/processed"

workflow {
    log.info """
    ======================================================================
    PROJECT AEGIS 2.0 — SCIENTIFIC BIOINFORMATICS WORKFLOW
    Organism Reference : ${params.organism}
    Target Assemblies  : ${params.assemblies}
    Output Directory   : ${params.outdir}
    ======================================================================
    """

    ch_assemblies = Channel.fromPath(params.assemblies)
        .map { file -> tuple(file.baseName, file) }

    ch_ref = file(params.reference_genome)

    // Stage 1: Quality Control
    qc_out = QUAST_QC(ch_assemblies)

    // Stage 2: AMR Determinants Identification (AMRFinderPlus)
    amr_out = AMRFINDER_PLUS(ch_assemblies)

    // Stage 3: Molecular Typing (MLST & Kleborate)
    mlst_out = MLST_TYPING(ch_assemblies)
    kleb_out = KLEBORATE_PROFILING(ch_assemblies)

    // Stage 4: Comparative Genomics & Core SNP Calling
    snippy_aln = SNIPPY_ALIGN(ch_assemblies, ch_ref)
    core_out   = SNIPPY_CORE(snippy_aln.map{ it[1] }.collect(), ch_ref)

    // Stage 5: Maximum-Likelihood Phylogenetics
    phylo_out  = IQTREE_PHYLOGENY(core_out.clean_aln)

    // Stage 6: Plasmid Reconstruction & Replicon Characterization
    mob_out    = MOB_RECON(ch_assemblies)
}

