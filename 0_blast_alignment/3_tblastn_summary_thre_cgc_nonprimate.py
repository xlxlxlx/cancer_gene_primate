#########
# Input: tblastn result database table
# Output: table with species as rows, genes as columns, 
#         gene existence status in species as values
#########

import os
import sqlite3
import pandas as pd
import random

# thresholds
filter_thre = 80
# genome or cds
sequence_type = "cds" 
# denovo or cgc
protein_type = "cgc"
table_name = "protein_nonprimate_cgc_thre80"

column_names = ["protein",
                "subject_sci_names",
                "subject_com_names",
                "subject_title",
                "query_accuracy",
                "subject_accuracy",
                "percentage_identity",
                "alignment_length",
                "mismatches",
                "query_start",
                "query_end",
                "sequence_start",
                "sequence_end",
                "e_value",
                "bit_score",
                "percentage_query_coverage_per_subject",
                "percentage_query_coverage_per_hsp",
                "qseq",
                "sseq"
               ]
               
filepath_cgc = "../protein_sequences_cgc/"
protein_sequence_list_cgc = []
for f in os.listdir(filepath_cgc):
    if not f.endswith(".fasta"):
        continue
    protein_id = f.split(".")[0]
    protein_sequence_list_cgc.append(protein_id)


nonprimate_species = ['Mus musculus', 'Canis lupus familiaris', 'Orycteropus afer afer', 'Danio rerio']
con = sqlite3.connect('cancer_primate.db')
cur = con.cursor()

protein_sequence_list = protein_sequence_list_cgc

identity_threshold = coverage_threshold = filter_thre

query_cmd = f"select * from {table_name} where Percentage_identity > {identity_threshold} and Percentage_query_coverage_per_subject > {coverage_threshold}"

rst = cur.execute(query_cmd)

df = pd.DataFrame(rst.fetchall())
df.columns = column_names

# make blank cells visually obvious
df_result = pd.DataFrame(columns = protein_sequence_list, index = nonprimate_species).fillna(' ')

for index, row in df.iterrows():
    protein = row['protein']
    species = row['subject_sci_names']    
    df_result.loc[species, protein] = row['subject_title']

df_result.to_csv(f'tblastn_summary_id{identity_threshold}_cover{coverage_threshold}_cds_cgc_nonprimate2.csv')
