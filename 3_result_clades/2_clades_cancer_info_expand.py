import pandas as pd

fn = 'cgc724_clades3_clade_info_proper_set'

df_clade = pd.read_csv(fn+'.csv')
df_uniprot = pd.read_csv('uniprot_cgc_reviewed_dedup.csv')
df_cgc = pd.read_csv('cancer_gene_census_v97.csv')

df_merged = pd.merge(df_clade, df_uniprot, left_on='Column', right_on='Entry', how='left')

selected_columns = df_cgc[["Somatic","Germline","Tumour Types(Somatic)","Tumour Types(Germline)","Cancer Syndrome","Tissue Type","Molecular Genetics","Role in Cancer","Mutation Types","Translocation Partner","Other Germline Mut","Other Syndrome","Gene Symbol","Name","Entrez GeneId","Genome Location","Tier","Hallmark","Chr Band"]]

df_merged = pd.merge(df_merged, selected_columns, left_on='From', right_on='Gene Symbol', how='left')

df_merged.to_csv(fn+'_expanded.csv', index=False)

