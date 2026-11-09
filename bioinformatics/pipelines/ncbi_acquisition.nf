#!/usr/bin/env nextflow
nextflow.enable.dsl=2

/*
========================================================================================
   PROJECT AEGIS 2.0 — NCBI DATA ACQUISITION & INGESTION PIPELINE
   Retrieves assemblies, computes SHA256 checksums, and extracts provenance metadata
========================================================================================
*/

params.accessions = "${projectDir}/../../data/raw/accessions.txt"
params.outdir     = "${projectDir}/../../data/raw/assemblies"

process NCBI_DOWNLOAD {
    tag "$accession"
    publishDir "${params.outdir}", mode: 'copy'

    input:
    val accession

    output:
    tuple val(accession), path("${accession}.fna"), path("${accession}.sha256")

    script:
    """
    echo "[AEGIS 2.0] Fetching NCBI Dataset for accession ${accession}..."
    
    # Download genome data package using NCBI Datasets CLI
    datasets download genome accession ${accession} --filename ${accession}.zip --include genome
    unzip -q -o ${accession}.zip
    
    # Standardize assembly path
    find ncbi_dataset/data/${accession}/ -name "*.fna" -exec cp {} ${accession}.fna \\;
    
    # Cryptographic checksum generation
    sha256sum ${accession}.fna > ${accession}.sha256
    """
}

workflow {
    ch_accessions = Channel.fromPath(params.accessions).splitText().map { it.trim() }
    NCBI_DOWNLOAD(ch_accessions)
}

