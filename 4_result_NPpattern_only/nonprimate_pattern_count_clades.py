import pandas as pd
import numpy as np
import itertools
from collections import Counter

fn = f'cds_cgc_nonprimate_genes_distribution'
df = pd.read_csv(f'{fn}.csv', index_col=0)

filter_list = ['A6NNL0',
 'O00221',
 'O14522',
 'O14746',
 'O15360',
 'O15393',
 'O60224',
 'O75081',
 'O75177',
 'O75444',
 'O94761',
 'P04198',
 'P05412',
 'P08575',
 'P09669',
 'P0DPQ6',
 'P10275',
 'P11912',
 'P15941',
 'P16455',
 'P20151',
 'P20848',
 'P23025',
 'P25445',
 'P31040',
 'P31151',
 'P31271',
 'P31994',
 'P35125',
 'P38398',
 'P40259',
 'P40337',
 'P49715',
 'P49792',
 'P51587',
 'P56279',
 'P58012',
 'P61769',
 'P78324',
 'Q13882',
 'Q14191',
 'Q15696',
 'Q16384',
 'Q16385',
 'Q2M1V0',
 'Q5HY64',
 'Q5VT03',
 'Q5VW00',
 'Q63HN8',
 'Q6PCD5',
 'Q86SG4',
 'Q86V71',
 'Q86VZ1',
 'Q86YC2',
 'Q8NA66',
 'Q8NDY4',
 'Q8NG31',
 'Q8WXI7',
 'Q92956',
 'Q96JC4',
 'Q96PJ5',
 'Q99102',
 'Q99643',
 'Q9BQ51',
 'Q9BUK0',
 'Q9BZE9',
 'Q9BZJ0',
 'Q9HC73',
 'Q9NNX6',
 'Q9NPI8',
 'Q9NZQ7',
 'Q9UH17',
 'Q9UHD8',
 'Q9UM73',
 'Q9UPS6']
df2 = df[[col for col in filter_list if col in df.columns]]



# generate all 8 possible patterns of 4 bits (0s and 1s)
patterns = list(itertools.product([0, 1], repeat=4))

indices_nonprimate = ['Mus musculus','Canis lupus familiaris','Orycteropus afer afer','Danio rerio']

# dictionary to hold column names and their corresponding patterns
col_patterns = {}

# check each column
for column in df2.columns:
    for pattern in patterns:
        pattern = list(pattern)
        pattern = [str(i) for i in pattern]
        if df2.loc[indices_nonprimate, column].tolist() == pattern:
            # add the pattern as a key and column name as a value to the dictionary
            col_patterns[column] = "".join(map(str, pattern))


# sort columns by the patterns
df2 = df2[sorted(col_patterns, key=col_patterns.get)]

# save the sorted DataFrame to a new csv file
df2.to_csv(f'{fn}_sorted.csv', index=True)

# create pattern-count table 
pattern_counts = Counter(col_patterns.values())
df_pattern_counts = pd.DataFrame.from_dict(pattern_counts, orient='index', columns=['Count'])
df_pattern_counts.index.name = 'Pattern'


# save the pattern-count table to a csv file
df_pattern_counts.to_csv(f'{fn}_pattern_counts.csv')