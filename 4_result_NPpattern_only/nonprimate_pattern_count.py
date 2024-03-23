import pandas as pd
import numpy as np
import itertools
from collections import Counter

fn = f'cds_cgc_nonprimate_genes_distribution'
df = pd.read_csv(f'{fn}.csv', index_col=0)

# generate all 8 possible patterns of 4 bits (0s and 1s)
patterns = list(itertools.product([0, 1], repeat=4))

indices_nonprimate = ['Mus musculus','Canis lupus familiaris','Orycteropus afer afer','Danio rerio']

# dictionary to hold column names and their corresponding patterns
col_patterns = {}

# check each column
for column in df.columns:
    for pattern in patterns:
        pattern = list(pattern)
        pattern = [str(i) for i in pattern]
        if df.loc[indices_nonprimate, column].tolist() == pattern:
            # add the pattern as a key and column name as a value to the dictionary
            col_patterns[column] = "".join(map(str, pattern))


# sort columns by the patterns
df = df[sorted(col_patterns, key=col_patterns.get)]

# save the sorted DataFrame to a new csv file
df.to_csv(f'{fn}_sorted.csv', index=True)

# create pattern-count table 
pattern_counts = Counter(col_patterns.values())
df_pattern_counts = pd.DataFrame.from_dict(pattern_counts, orient='index', columns=['Count'])
df_pattern_counts.index.name = 'Pattern'


# save the pattern-count table to a csv file
df_pattern_counts.to_csv(f'{fn}_pattern_counts.csv')