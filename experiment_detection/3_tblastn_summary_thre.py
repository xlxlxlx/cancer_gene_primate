#########
# Input: tblastn result database table
# Output: table with species as rows, genes as columns, 
#         gene existence status in species as values
#########

import os
import sqlite3
import pandas as pd

# thresholds
filter_thre = 80
# genome or cds
sequence_type = "cds" 
# cgc or random
protein_type = "random100"

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

filepath_random100 = "../protein_sequence_random100/"
protein_sequence_list_random100 = []

for f in os.listdir(filepath_random100):
    if not f.endswith(".fasta"):
        continue
    protein_id = f.split(".")[0]
    protein_sequence_list_random100.append(protein_id)


nonprimate_species = ['Mus musculus','Canis lupus familiaris','Danio rerio','Orycteropus afer afer']
primate_species = [
    'Saimiri boliviensis boliviensis', 'Theropithecus gelada', 'Aotus nancymaae', 'Callithrix jacchus', 'Carlito syrichta', 'Cebus capucinus', 'Cercocebus atys', 'Chlorocebus sabaeus', 'Colobus angolensis palliatus', 'Gorilla gorilla', 'Homo sapiens', 'Macaca fascicularis', 'Macaca mulatta', 'Macaca nemestrina', 'Mandrillus leucophaeus', 'Microcebus murinus', 'Nomascus leucogenys', 'Otolemur garnettii', 'Pan paniscus', 'Pan troglodytes', 'Papio anubis', 'Piliocolobus tephrosceles', 'Pongo abelii', 'Prolemur simus', 'Propithecus coquereli', 'Rhinopithecus bieti', 'Rhinopithecus roxellana', 'Cebus imitator', 'Hylobates moloch', 'Lemur catta', 'Sapajus apella', 'Trachypithecus francoisi'
    ]

con = sqlite3.connect('climate_primate.db')
cur = con.cursor()

protein_sequence_list = eval(f"protein_sequence_list_{protein_type}")

identity_threshold = coverage_threshold = filter_thre
table_name = f"protein_primate_species_{sequence_type}_{protein_type}_thre{filter_thre}"

query_cmd = f"select * from {table_name} where Percentage_identity > {identity_threshold} and percentage_query_coverage_per_subject > {coverage_threshold}"

rst = cur.execute(query_cmd)

df = pd.DataFrame(rst.fetchall())
df.columns = column_names

# make blank cells visually obvious
df_result = pd.DataFrame(columns = protein_sequence_list, index = primate_species).fillna(' ')

for index, row in df.iterrows():
    protein = row['protein']
    species = row['subject_sci_names']    
    df_result.loc[species, protein] = row['subject_title']

df_result.to_csv(f'tblastn_summary_id{identity_threshold}_cover{coverage_threshold}_{sequence_type}_{protein_type}.csv')    
