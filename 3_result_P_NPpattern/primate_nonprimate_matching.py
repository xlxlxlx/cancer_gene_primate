import pandas as pd
import numpy as np
import itertools
from collections import Counter


dist_list = ['all_zeros', "proper_subset", "all_ones"]

for dist in dist_list:
    fn = f"cgc_primate_genes_{dist}"
    df1, df2 = pd.read_csv(f'cds_{fn}.csv', index_col=0), pd.read_csv(f'cds_cgc_nonprimate_genes_distribution.csv')

    # generate all 8 possible patterns of 3 bits (0s and 1s)
    patterns = list(itertools.product([0, 1], repeat=4))

    df_new = pd.DataFrame()

    for column in df1.columns:
        for pattern in patterns:
            pattern = list(pattern)
            if df2[column][:4].astype(int).tolist() == pattern:
                # append the pattern as a row to the column
                df_new[column] = df1[column].tolist() + ["'" + "".join(map(str, pattern)) + "'"]

    df_new.index = list(df1.index) + ['non_primates']

    # convert the pattern row to the object type to keep leading zeros
    df_new.loc["non_primates"] = df_new.loc["non_primates"].astype(str)

    # sort columns by the pattern row (last row)
    df_new = df_new.reindex(sorted(df_new.columns, key = lambda x: df_new[x].iloc[-1]), axis=1)

    df_new.to_csv(f'{fn}_with_patterns.csv', index=True)
