import pandas as pd
import numpy as np
import itertools
from collections import Counter

df1, df2 = pd.read_csv('tblastn_id80_cover80_cds_cgc724.csv', index_col=0), pd.read_csv('tblastn_id80_cover80_cds_cgc_nonprimates_distribution.csv')

# Generate all possible patterns of 4 bits (0s and 1s)
patterns = list(itertools.product([0, 1], repeat=4))

df_new = pd.DataFrame()

for column in df1.columns:
    for pattern in patterns:
        pattern = list(pattern)
        if df2[column].tolist() == pattern:
            # Append the pattern as a row to the column
            df_new[column] = df1[column].tolist() + ["'" + "".join(map(str, pattern)) + "'"]

df_new.index = list(df1.index) + ['non_primates']

# Keep leading zeros in patterns
df_new.loc["non_primates"] = df_new.loc["non_primates"].astype(str)

# Sort columns by the pattern row (last row)
df_new = df_new.reindex(sorted(df_new.columns, key = lambda x: df_new[x].iloc[-1]), axis=1)


df_new.to_csv('cgc724_with_patterns.csv', index=True)


#################


# Dictionary to hold column names and their corresponding patterns
col_patterns = {}

# Check each column in df2
for column in df2.columns:
    for pattern in patterns:
        pattern = list(pattern)
        if df2[column].tolist() == pattern:
            # Add the pattern as a key and column name as a value to the dictionary
            col_patterns[column] = "".join(map(str, pattern))


# Sort df2 columns by the patterns
df2 = df2[sorted(col_patterns, key=col_patterns.get)]

# Save the sorted DataFrame to a new CSV file
df2.to_csv('tblastn_summary_id80_cover80_cds_cgc_nonprimates_distribution_sorted.csv', index=True)


# Create pattern-count table for df2
pattern_counts = Counter(col_patterns.values())
df_pattern_counts = pd.DataFrame.from_dict(pattern_counts, orient='index', columns=['Count'])
df_pattern_counts.index.name = 'Pattern'

# Save the pattern-count table to a CSV file
df_pattern_counts.to_csv('nonprimates_distribution_pattern_counts.csv')

