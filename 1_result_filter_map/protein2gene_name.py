import pandas as pd


species_list = ["primate", "nonprimate"]

for species in species_list:
    filename = f"cds_cgc_{species}"
    df = pd.read_csv(filename+".csv", index_col=0)

    df2 = pd.read_csv('uniprot_cgc_reviewed_dedup.csv')

    gene_list = []
    matched_columns = []
    for column_name in df.columns:
        match_row = df2[df2['Entry'] == column_name]
        #print(match_row)
        if not match_row.empty:
            gene_list.append(match_row['From'].values[0])
            matched_columns.append(column_name)
        else:
            gene_list.append(None)  # Append None if there's no match

    df.loc[len(df)] = gene_list
    # filter df to keep only the columns where a match was found
    df = df[matched_columns]

    # save the updated dataframe to a new csv file
    df.to_csv(f'cds_cgc_{species}_genes.csv', index=True)