import pandas as pd

filename = "tblastn_summary_id80_cover80_cds_cgc_4nonprimates"

df = pd.read_csv(filename+".csv", index_col=0)
df_new = df.copy()

# For each value in df, if the value is " ", assign the value "0" to the corresponding cell in df_new. Otherwise, assign "1"
df_new = df_new.applymap(lambda x: '0' if x == ' ' else '1')

df_new.to_csv(filename+"_distribution.csv", index=True)


# All the genes with all 1s
df_ones = df_new.loc[:, (df_new == '1').all()]
df_ones.to_csv(filename+'_all_ones.csv', index=True)

# All the genes with all 0s
df_zeros = df_new.loc[:, (df_new == '0').all()]
df_zeros.to_csv(filename+'_all_zeros.csv', index=True)

df_cols = set(df.columns)
df_ones_cols = set(df_ones.columns)
df_zeros_cols = set(df_zeros.columns)

# Other genes
remaining_cols = df_cols - (df_ones_cols.union(df_zeros_cols))
df_remaining = df[remaining_cols]
df_remaining.to_csv(filename+'_proper_set.csv', index=False)
