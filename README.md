# Concerning the Existence of Human Cancer Genes in Primate Species

This is a repository storing data and scripts used in our manuscript titled "Concerning the Existence of Human Cancer Genes in Primate Species".

## Data files
- uniprot_cgc.tsv   
The UniProt ID mapping [^1] result for the original 733 cancer associated genes obtained from Cancer Gene Census [^2]. Note that this table contains both reviewed and unreviewed proteins. 

- uniprot_random100_reviewed_dedup.csv   
A random set of 100 human genes and their corresponding proteins used in this study.

- uniprot_random60_reviewed_dedup.csv   
A random set of 60 human genes and their corresponding proteins used in this study.

- uniprot_random180_reviewed_dedup.csv   
A random set of 180 human genes and their corresponding proteins used in this study.

- genome_accession.xlsx    
The genome accession numbers for the 32 primate genomes and 4 non-primate species used in this study, obtained form Ensembl [^3] and NCBI [^4].

- Homo_sapiens_GRCh38_cds_list.csv   
The full human gene list extracted from human CDS sequence obtained from Ensembl [^3]. Note there are duplicated gene names.

- cgc724_large_clades.csv   
The full table of human cancer genes that are completely absent from at least one large primate clade (size 5-8).

- cgc724_small_clades.csv   
The full table of human cancer genes that are completely absent from at least one small primate clade (size 2-3).

- fasta2genelist.py    
The script used to extract the full human gene list from human CDS sequence file.


## Scripts
The scripts are labeled according to their order of execution. If two scripts share the same preceeding number, this indicates that there is no strict sequence for executing them.

### experiment_detection
Scripts and files under this folder is for human gene detection in primate and nonprimate coding sequences.

- 1_tblastn_genome_cds.py    
Align protein sequence to genome or CDS sequence

- 2_tblastn_result2sql.py    
Input the aligning results into a relational database

- 3_tblastn_summary_thre.py   
Summarize the aligning result into a gene x species matrix

- climate_primate.sql    
The database table creation file when a new database table is needed

### experiment_distribution
Scripts under this folder is for the distribution of human cancer and random genes among primate and non-primate species.

- 1_binary_tables.py   
Convert the result table of experiment_detection into binary distribution tables.

- 2_existence_in_clades   
Match genes to their existing and absent primate clades.

- 2_nonprimate_pattern_matching   
Match genes to their existing patterns in 4 non-primate species.

### experiment_primate_emergence
Scripts and files under this folder is for estimating gene emergence time among primates. 

- 1_divergence_time_clades_hits.py    
Estimate gene emergence time based on divergence time of primate clades   

- 2_divergence_time_plot.py   
Generate time-dependent distribution plot for gene emergence time    

- clades_divergence_time.csv
Input data where the divergence times are derived from TimeTree database [^5]. 



[^1]: "UniProt: the universal protein knowledgebase in 2023." Nucleic Acids Research 51, no. D1 (2023): D523-D531.
[^2]: Sondka, Zbyslaw, et al. "The COSMIC Cancer Gene Census: describing genetic dysfunction across all human cancers." Nature Reviews Cancer 18.11 (2018): 696-705.
[^3]: Cunningham, Fiona, et al. "Ensembl 2022." Nucleic acids research 50.D1 (2022): D988-D995.
[^4]: Sayers, Eric W., et al. "Database resources of the national center for biotechnology information." Nucleic acids research 50.D1 (2022): D20.
[^5]: Kumar, Sudhir, et al. "TimeTree 5: An expanded resource for species divergence times." Molecular Biology and Evolution 39.8 (2022): msac174.


