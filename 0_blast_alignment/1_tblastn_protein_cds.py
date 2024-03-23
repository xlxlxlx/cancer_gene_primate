import os
import subprocess
import random

# to queue tasks in batch
# not the best practice, can be improved
task_list = "tblastn_batch_task.txt"

# store all the protein sequence files in lists
filepath_cgc= "../protein_sequence_cgc/"
filepath_rst = "rst10_cds_cgc"

protein_sequence_list_cgc= []

for f in os.listdir(filepath_random):
    if not f.endswith(".fasta"):
        continue
    protein_id = f.split(".")[0]
    protein_sequence_list_random.append(protein_id)

# store all the genome and cds database files in lists
filepath_ensembl = "../cds2_ensembl/"
filepath_ncbi = "../cds2_ncbi/"

cds_sequence_ensembl = {}
cds_sequence_ncbi = {}

for f in os.listdir(filepath_ensembl):
    print(f)
    if not f.endswith(".cds.all.fa"):
        continue
    species_name = f.split(".")[0]
    cds_sequence_ensembl[species_name] = f

for f in os.listdir(filepath_ncbi):
    print(f)
    if not f.endswith("cds_from_genomic.fna"):
        continue
    species_name = f.split(".")[0]
    cds_sequence_ncbi[species_name] = f

# queue tblastn jobs in batch
# cds
for protein in protein_sequence_list:
    for species in cds_sequence_ncbi:
        species_db = cds_sequence_ncbi[species]
        task = f"../tools/blast/ncbi-blast-2.13.0+/bin/tblastn -db {species_db} -query {filepath_tissue}/{protein}.fasta -outfmt '7 sscinames scomnames stitle qacc sacc pident length mismatch gapopens qstart qend sstart send evalue bitscore qcovs qcovhsp qseq sseq'  -out {filepath_rst}/{protein}_{species}_ncbi.tab"
        print(task)
        with open(task_list, 'w') as f:
            f.write(task)
        cmd = 'batch < ' + task_list
        os.system(cmd)
    for species in cds_sequence_ensembl:
        species_db = cds_sequence_ensembl[species]
        task = f"../tools/blast/ncbi-blast-2.13.0+/bin/tblastn -db {species_db} -query {filepath_tissue}/{protein}.fasta  -outfmt '7 sscinames scomnames stitle qacc sacc pident length mismatch gapopens qstart qend sstart send evalue bitscore qcovs qcovhsp qseq sseq'  -out {filepath_rst}/{protein}_{species}_ensembl.tab"
        print(task)
        with open(task_list, 'w') as f:
            f.write(task)
        cmd = 'batch < ' + task_list
        os.system(cmd)
