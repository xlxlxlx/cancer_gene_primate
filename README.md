# Concerning the Existence of Human Cancer Genes in Primate Species

This is a repository storing data and scripts used in our manuscript titled "Concerning the Existence of Human Cancer Genes in Primate Species".

## Data files
- genome_accession.xlsx    
The genome accession numbers for the 32 primate genomes and 4 non-primate species used in this study, obtained form Ensembl [^3] and NCBI [^4].

- uniprot_cgc.tsv   
The UniProt ID mapping [^1] result for the original 733 cancer associated genes obtained from Cancer Gene Census [^2]. Note that this table contains both reviewed and unreviewed proteins. 

- uniprot_cgc_reviewed_dedup.tsv   
The 727 cancer genes analyzed in the paper. The UniProt ID mapping [^1] result for the 727 cancer associated genes obtained from Cancer Gene Census [^2] with at least one "reviewed" protein and deduped. 

- uniprot_random100_reviewed_dedup.csv   
A random set of 100 human genes and their corresponding proteins used in this study.

- uniprot_random60_reviewed_dedup.csv   
A random set of 60 human genes and their corresponding proteins used in this study.

- uniprot_random180_reviewed_dedup.csv   
A random set of 180 human genes and their corresponding proteins used in this study.

- Homo_sapiens_GRCh38_cds_list.csv   
The full human gene list extracted from human CDS sequence obtained from Ensembl [^3]. Note there are duplicated gene names.

- fasta2genelist.py    
The script used to extract the full human gene list from human CDS sequence file.

- cgc_clade_large.csv   
The full table of human cancer genes that are completely absent from at least one large primate clade (size 5-8).

- cgc_clade_small.csv   
The full table of human cancer genes that are completely absent from at least one small primate clade (size 2-4).



## Scripts
The scripts are labeled according to their order of execution. If two scripts share the same preceeding number, this indicates that there is no strict sequence for executing them.

### 0_blast_alignment
Scripts and files under this folder are for human gene alignment to primate and nonprimate coding sequences.

- 1_tblastn_protein_cds.py   
Align protein sequence to CDS sequence   

- 2_tblastn_result2sql_cgc_nonprimate, 2_tblastn_result2sql_cgc_primate   
Input the aligning results into a relational database

- 3_tblastn_summary_thre_cgc_nonprimate, 3_tblastn_summary_thre_cgc_primate   
Summarize the aligning result into a gene x species matrix   

- primate_cgc_primate.sql, primate_cgc_nonprimate.sql   
The database table creation files when a new database table is needed   

### 1_result_filter_map
Inputs are outputs from 0_blast_alignment. The script maps proteins to genes.   

- protein2gene_name.py   
Map proteins to their gene names and filter results by a given gene list.   

### 2_result_distribution
Inputs are outputs from 1_result_filter_map. The script generates the binary distribution of genes across species.   

- values_to_binary.py   
Map values to 0 or 1, seperate the results into tables containing all 1s, all 0s, and the remaining.   

### 3_result_clades
Inputs are outputs from 2_result_distribution. The script combines primate gene distribution results with nonprimate patterns.   

- 1_clade_assigner.py   
Identify genes that are absent from an entire primate clade.   

- 2_clades_cancer_info_expand.py   
Expands the results from 1_clade_assigner.py with information obtained from Cancer Gene Census [^2].   

### 3_result_divergence_time
Inputs are outputs from 2_result_distribution. Scripts and files under this folder estimate gene emergence time among primates.    
- 1_divergence_time_clades_hits.py    
Estimate gene emergence time based on divergence time of primate clades   

- 2_divergence_time_plot.py   
Generate time-dependent distribution plot for gene emergence time    

- clades_divergence_time.csv
Input data where the divergence times are derived from TimeTree database [^5]. 

### 3_result_P_NPpattern
Inputs are outputs from 2_result_distribution. The script combines primate gene distribution results with nonprimate patterns.   

- primate_nonprimate_matching.py   
Generate nonprimate patterns based on gene binary distribution across nonprimate species. Then combines the nonprimate patterns with the gene distribution across primate species.    


### 4_result_NPpattern_only
Inputs are outputs from 3_result_clades. The scripts count the number of each nonprimate pattern within a given data set.   

- nonprimate_pattern_count.py   
Count the number of each nonprimate pattern in the entire cancer gene set.    

- nonprimate_pattern_count_clades.py   
Count the number of each nonprimate pattern in a given gene set (genes missing from large clades).    



[^1]: "UniProt: the universal protein knowledgebase in 2023." Nucleic Acids Research 51, no. D1 (2023): D523-D531.
[^2]: Sondka, Zbyslaw, et al. "The COSMIC Cancer Gene Census: describing genetic dysfunction across all human cancers." Nature Reviews Cancer 18.11 (2018): 696-705.
[^3]: Cunningham, Fiona, et al. "Ensembl 2022." Nucleic acids research 50.D1 (2022): D988-D995.
[^4]: Sayers, Eric W., et al. "Database resources of the national center for biotechnology information." Nucleic acids research 50.D1 (2022): D20.
[^5]: Kumar, Sudhir, et al. "TimeTree 5: An expanded resource for species divergence times." Molecular Biology and Evolution 39.8 (2022): msac174.


