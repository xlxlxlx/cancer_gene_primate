#########
# This script stores tblastn results in SQLite database
#
# Input: tblastn results in .tab files
# Output: SQLite database table storing results
#         (the table needs to be created beforehand)
#########

import os
import sqlite3
import numbers

con = sqlite3.connect('cancer_primate.db')
cur = con.cursor()

# if there are too many hits in whole genome, 
# take first k that pass the threshold
#
# this handles the case where there are too 
# many findings to go through
line_limit_per_f = 1

# thresholds for both percentage_identity and percentage_query_coverage
# can be separated if needed
filter_thre = 80

# genome or cds
sequence_type = "cds" 
# denovo or cgc
protein_type = "cgc"

filepath = f".../rst_blast_protein_genome/rst_cgc/"
table_name = f"protein_primate_cgc_thre80"

for f in os.listdir(filepath):
    print(f)
    if not f.endswith(".tab"):
        continue
    f_values = [f[:-4].split("_")[0]]
    line_count = 0
    with open(filepath+f,'r') as f_open:
        for line in f_open:
            if line_count >= line_limit_per_f:
                break
            if line.startswith("#"):
                continue   
            line_values_list = f_values+line.split('\n')[0].split("\t")
            line_values_list = [x.replace("'","") for x in line_values_list]
            # filter result entries based on thresholds
            if int(line_values_list[-4]) < filter_thre or float(line_values_list[6]) < filter_thre:
                continue
            # add species name for nonprimates
            species_name = ' '.join(f[:-4].split("_")[1:-1])
            line_values_list = [x if x.isdigit() or x.replace('.', '', 1).isdigit() else "'{0}'".format(x) for x in line_values_list]
            line_values_list = [line_values_list[0]]+["'{0}'".format(species_name)]+["'{0}'".format(species_name)]+line_values_list[3:]
            line_values = ','.join(line_values_list) 
            print(line_values)    
            line_count += 1
            cur.execute(f"INSERT OR IGNORE INTO {table_name} VALUES ({line_values})")
            con.commit()
            
