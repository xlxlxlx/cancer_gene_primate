#########
# Input: (1) divergence_time_clades.csv table
#        (2) table with species as rows, genes as columns, 
#         gene existence status in species as values
# Output: a table storing number of cds/genome hits 
#         in each primate clade, along with details
#         (such as list of genes, clade left and right 
#         branches, divergence time of the clade)
#########

import pandas as pd
import numpy as np

filter_thre = 80
identity_threshold = coverage_threshold = filter_thre

hit_thre_low = 3/5
hit_thre_high = 4/5

no_hit_thre = 1/5

# if multiple divergence time are suggested, 
# take the earliest one
dedup_count = 1
dedup = True
high_thre_only = True

# this script runs all combinations of the following two lists
# sequence_type_list choices: "genome", "cds"
# protein_type_list choices: "denovo", "cgc"
sequence_type_list = ["cds"]
protein_type_list = ["cgc","random339"]
# add custom suffix to result filename
suffix = ''

df_clades_hits_fn = 'All_clades_gene_hits'  
if high_thre_only:
    df_clades_hits_fn += '1.0' 
else :
    df_clades_hits_fn += '0.6'
    
if dedup:
    df_clades_hits_fn += '_dedup'

# input the organized data table with primate clades
# and other information such as their divergence times
df_clades = pd.read_csv("clades_divergence_time.csv")
df_clades_hits = df_clades.copy()

# this script runs all combinations of the following two lists
for sequence_type in sequence_type_list:
    for protein_type in protein_type_list:
        # this is the output of tblastn_summary_thre.py
        fn = f"{protein_type}_primate_genes_proper_subset_0000.csv"
        df = pd.read_csv(fn, index_col=0)

        clade_dict = {}
        df_rst = pd.DataFrame(columns = ["protein", "protein_type", "clade_divergence_time", "clade_divergence_time_range_start", "clade_divergence_time_range_end", "left_ranch_first_species", "clase_size","left_clade_size", "right_clade_size", "ratio_left", "ratio_right", "emergence"])

        for index, row in df_clades.iterrows():
            divergence_time, range_start, range_end, left_ranch_first_species, left_branch_species, right_branch_species, name, rank, right_clade, left_clade = row.tolist()
            clade_dict[divergence_time] = [
                right_clade.split(', '), 
                left_clade.split(', '), 
                range_start, 
                range_end, 
                left_ranch_first_species, 
                left_branch_species, 
                right_branch_species, 
                name, 
                rank]
        for protein in df:
            species_hit = df[protein][df[protein] != 0].index.tolist()
            for clade in clade_dict:
                emergence = None
                clade_size_left = len(clade_dict[clade][0])
                clade_size_right = len(clade_dict[clade][1])
                hits_left = len(np.intersect1d(clade_dict[clade][0], species_hit))
                hits_right = len(np.intersect1d(clade_dict[clade][1], species_hit))
                
                ratio_left = hits_left/clade_size_left
                ratio_right = hits_right/clade_size_right
                
                # assign gene emergence to clades based on thresholds
                if ratio_left >= hit_thre_high and ratio_right <= no_hit_thre:
                    emergence = sequence_type + "(left)(high)"
                elif ratio_right >= hit_thre_high and ratio_left <= no_hit_thre:
                    emergence = sequence_type + "(right)(high)"
                
                elif ratio_left >= hit_thre_low and ratio_right <= no_hit_thre and not high_thre_only:
                    emergence = sequence_type + "(left)(low)"
                elif ratio_right >= hit_thre_low and ratio_left <= no_hit_thre and not high_thre_only:
                    emergence = sequence_type + "(right)(low)"
                
                # proceed if the emergence time is estimated
                # to be within primates
                if emergence is not None:
                    df_rst = df_rst.append(
                        {"protein": protein, 
                        "protein_type": protein_type, 
                        "clade_divergence_time": clade, 
                        "clade_divergence_time_range_start": clade_dict[clade][2],"clade_divergence_time_range_end": clade_dict[clade][3],
                        "left_ranch_first_species": clade_dict[clade][4],
                        "clade_size": clade_dict[clade][5]+clade_dict[clade][6], 
                        "left_clade_size": clade_dict[clade][5],  
                        "right_clade_size": clade_dict[clade][6], 
                        "ratio_left": ratio_left,  
                        "ratio_right": ratio_right, 
                        "clade_left": clade_dict[clade][0],  
                        "clade_right": clade_dict[clade][1], 
                        "emergence": emergence},
                        ignore_index = True)

        #df_rst = df_rst.sort_values('clade_size', ascending=False)
        print(df_rst)
        
        df_rst.to_csv('original_'+df_clades_hits_fn+'.csv', index=False)
        
        # if dedup flag and multiple divergence time are suggested, 
        # take the earliest one
        if dedup:
            df_rst = df_rst.groupby('protein').head(dedup_count)
            df_rst = df_rst.sort_values('protein')
            
        divergence_sequence_dict = df_rst.groupby('clade_divergence_time')['protein'].apply(list).to_dict()
        
        divergence_sequence_count_dict = df_rst.groupby('clade_divergence_time')['protein'].size().to_dict()
        
        
        df_clades_hits[f'{sequence_type}_{protein_type}'] = df_clades_hits['divergence_time'].map(divergence_sequence_dict)
        df_clades_hits[f'{sequence_type}_{protein_type}'] = df_clades_hits[f'{sequence_type}_{protein_type}'].fillna(0)
        
        df_clades_hits[f'count_{sequence_type}_{protein_type}'] = df_clades_hits['divergence_time'].map(divergence_sequence_count_dict)
        df_clades_hits[f'count_{sequence_type}_{protein_type}']  = df_clades_hits[f'count_{sequence_type}_{protein_type}'].fillna(0)
        

# how balanced the clade is
#df_clades_hits['clade_size'] = df_clades_hits['#right_branch_species'] + df_clades_hits['#left_branch_species']
#df_clades_hits['clade_ratio'] = df_clades_hits['#right_branch_species'] / df_clades_hits['#left_branch_species']
      
df_clades_hits.to_csv(df_clades_hits_fn+'.csv', index=False) 
