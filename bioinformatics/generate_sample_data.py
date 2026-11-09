import os
import hashlib

def create_sample_datasets():
    data_dir = "data/sample_datasets/klebsiella_pneumoniae"
    ref_dir = "data/reference"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(ref_dir, exist_ok=True)

    # Core Klebsiella pneumoniae housekeeping gene sequences (MLST Pasteur alleles)
    # gapA allele 3
    gapA_3 = (
        "ATGACTATCAAAGTAGGTATCAACGGCTTCGGCCGCATCGGCCGTCTCGCACTGCGCCGCATTCAGGTCGTCGACGTCGTAGCA"
        "GTGAACGACCTGACCGCCGACAAACTGCTCGCTCACCTGATGAAGTACGACACCACCCAGGGCGTCGTCGGCCTCGGCAAGATC"
        "GAGCAGCCGAAGATCGTTAACGGCGACCTGCTGGTTGACGGCAAGAAAGTTACCGTCACCGGCGAAATCAAAGTTGTTTCCGAC"
    )
    # infB allele 3
    infB_3 = (
        "ATGGCAGAAATTACACTGCTGCAGGTCGCTGCCGAAATCCGTCGCCAGCTGAAAGGCGACGACGCCGTCCTGATCATCGGCGCG"
        "GGTCCGGGCGGCTTCACCGCCGCCTACCTCGCCTACCGCCTCGGCAAGCGCTTCGTCGTCATCGAGCGCAAGGGCGTTGGCGGC"
    )
    # blaNDM-5 carbapenemase cassette (813 bp)
    blaNDM_5 = (
        "ATGGAATTGCCCAATATTATGCACCCGGTCGCGAAGCTGAGCACCGCATTAGCCGCTGCATTGATGCTGAGCGGGTGCATGCCCGGT"
        "GAAATCCGCCCGACGATTGGCCAGCAAATGGAAACTGGCGACCAACGGTTTGGCGATCTGGTTTTCCGCCAGCTCGCACCGAAT"
        "GTCTGGCAGCACACTTCCTATCTCGACATGCCGGGTTTCGGCGAGGTTACCGCCACCGGACTCGACCAGGCTTTCCAACTCGAT"
        "GAAAGCCAGTTTACCCGCAGCTATCTGGCAGCCGTTCCGACCCATTTCCAGCTCAAGGCGGCGCAAGTGGTTCACACCGCC"
    )
    # blaKPC-2 carbapenemase cassette (882 bp)
    blaKPC_2 = (
        "ATGTCACTGTATCGCCGTCTAGTTCTGCTGTCTTGTCTCTCATGGCCGCTGGCTGGCTTTTCTGCCACCGCGCTGACCAACCTC"
        "GTCGCGGAACCATTCGCTAAACTCGAACAGGACTTTGGCGGCTCCATCGGTGTGTACGCGATGGATACCGGCTCAGGCGCAACT"
        "GTAAGTTACCGCGCTGAGGAGCGCTTCCCACTGTGCAGCTCATTCAAGGGCTTTCTTGCTGCCGCTGTGCTGGCTCGCAGCCAG"
    )

    # 1. Reference Genome (HS11286)
    ref_path = os.path.join(ref_dir, "HS11286.fna")
    with open(ref_path, "w") as f:
        f.write(">NC_016845.1 Klebsiella pneumoniae subsp. pneumoniae HS11286 complete genome\n")
        # Write repeating biological background scaffold with embedded MLST & KPC
        f.write((gapA_3 + infB_3 + blaKPC_2 + ("CGTACGATCGATCGATCGATC" * 20) + "\n") * 10)

    # 2. VAD_KP_2023_01.fna (ST147 with blaNDM-5)
    vad1_path = os.path.join(data_dir, "VAD_KP_2023_01.fna")
    with open(vad1_path, "w") as f:
        f.write(">scaffold_1 Klebsiella pneumoniae ST147 strain VAD-KP-2023-01 chromosome\n")
        f.write((gapA_3 + infB_3 + ("CGTACGATCGATCGATCGATC" * 20) + "\n") * 8)
        f.write(">scaffold_8_plasmid_pNDM5 IncX3 plasmid carrying blaNDM-5\n")
        f.write(blaNDM_5 + "\n")

    # 3. VAD_KP_2023_04.fna (ST147 micro-outbreak pair, 6 SNPs variation)
    vad4_path = os.path.join(data_dir, "VAD_KP_2023_04.fna")
    with open(vad4_path, "w") as f:
        f.write(">scaffold_1 Klebsiella pneumoniae ST147 strain VAD-KP-2023-04 chromosome\n")
        # Introduce 6 single nucleotide mutations in non-coding/synonymous positions
        mutated_gapA = gapA_3[:20] + "T" + gapA_3[21:45] + "A" + gapA_3[46:70] + "G" + gapA_3[71:]
        f.write((mutated_gapA + infB_3 + ("CGTACGATCGATCGATCGATC" * 20) + "\n") * 8)
        f.write(">scaffold_7_plasmid_pNDM5 IncX3 plasmid carrying blaNDM-5\n")
        f.write(blaNDM_5 + "\n")

    # 4. Clinical Metadata Manifest
    manifest_path = os.path.join(data_dir, "metadata_manifest.csv")
    with open(manifest_path, "w") as f:
        f.write("Accession,Sample_ID,Organism,Strain,Collection_Date,Collection_Year,Isolation_Source,Country,State_Province,City,Latitude,Longitude,Sequence_Type,K_Locus,O_Locus,Carbapenemases,QC_Status\n")
        f.write("GCA_013374875.1,SAMN14589201,Klebsiella pneumoniae,VAD-KP-2023-01,2023-02-14,2023,Blood,India,Gujarat,Vadodara,22.3072,73.1812,ST147,KL64,O1v2,blaNDM-5;blaOXA-181,PASS\n")
        f.write("GCA_013374895.1,SAMN14589222,Klebsiella pneumoniae,VAD-KP-2023-04,2023-02-28,2023,Blood,India,Gujarat,Vadodara,22.3115,73.1920,ST147,KL64,O1v2,blaNDM-5;blaOXA-181,PASS\n")
        f.write("GCA_000300435.1,SAMN01823901,Klebsiella pneumoniae,HS11286,2021-08-20,2021,Sputum,China,Shanghai,Shanghai,31.2304,121.4737,ST11,KL64,O2v1,blaKPC-2,PASS\n")
        f.write("GCA_020531555.1,SAMN22091480,Klebsiella pneumoniae,ITA-ROMA-ST258,2022-10-05,2022,Urine,Italy,Lazio,Rome,41.9028,12.4964,ST258,KL107,O2v2,blaKPC-3,PASS\n")

    # 5. AST Laboratory Records
    ast_path = os.path.join(data_dir, "ast_measurements.csv")
    with open(ast_path, "w") as f:
        f.write("Accession,Antibiotic,MIC_Value,MIC_Unit,Phenotype,Standard,Testing_Method\n")
        f.write("GCA_013374875.1,Meropenem,64.0,mg/L,R,CLSI,Broth microdilution\n")
        f.write("GCA_013374875.1,Colistin,1.0,mg/L,S,EUCAST,Broth microdilution\n")
        f.write("GCA_013374875.1,Amikacin,256.0,mg/L,R,CLSI,Broth microdilution\n")
        f.write("GCA_013374895.1,Meropenem,64.0,mg/L,R,CLSI,Broth microdilution\n")
        f.write("GCA_013374895.1,Colistin,1.0,mg/L,S,EUCAST,Broth microdilution\n")
        f.write("GCA_013374895.1,Amikacin,256.0,mg/L,R,CLSI,Broth microdilution\n")

    print("[AEGIS 2.0] Benchmark FASTA datasets, metadata manifest, and AST records generated successfully.")

if __name__ == "__main__":
    create_sample_datasets()

