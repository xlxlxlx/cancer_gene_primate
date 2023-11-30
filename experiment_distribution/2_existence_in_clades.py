import pandas as pd

# The proportion of "existing" species for a gene to exist in a clade
ratio_thre = 1

def is_selected_column(column, clades):
    """
    Check if the column should be selected based on existence in clades.
    """
    zeros_in_clade = False
    ones_in_clade = False
    zero_clades = []
    one_clades = []
    
    # Check each clade
    for clade in clades:
        sub_col = column[clade]
        zero_ratio = (sub_col == " ").sum() / len(sub_col)
        one_ratio = (sub_col != " ").sum() / len(sub_col)
        
        if zero_ratio >= ratio_thre:
            zeros_in_clade = True
            zero_clades.append(clade)
        if one_ratio >= ratio_thre:
            ones_in_clade = True
            one_clades.append(clade)
            
    # If both conditions have been satisfied
    if zeros_in_clade and ones_in_clade:
        return True, zero_clades, one_clades
            
    return False, zero_clades, one_clades

# large clades
clades = [["Otolemur garnettii","Prolemur simus","Lemur catta","Propithecus coquereli","Microcebus murinus"],
["Callithrix jacchus","Aotus nancymaae","Saimiri boliviensis boliviensis","Cebus imitator","Cebus capucinus","Sapajus apella"],
["Chlorocebus sabaeus","Mandrillus leucophaeus","Cercocebus atys","Papio anubis","Theropithecus gelada","Macaca fascicularis","Macaca mulatta","Macaca nemestrina"],
["Piliocolobus tephrosceles","Colobus angolensis palliatus","Trachypithecus francoisi","Rhinopithecus roxellana","Rhinopithecus bieti"]
]

# small clades
small_clades = [
["Callithrix jacchus","Aotus nancymaae"],
["Cebus imitator","Cebus capucinus","Sapajus apella"],
["Hylobates moloch","Nomascus leucogenys"],
["Gorilla gorilla","Pan paniscus","Pan troglodytes"],
["Mandrillus leucophaeus","Cercocebus atys","Papio anubis","Theropithecus gelada"],
["Macaca fascicularis","Macaca mulatta","Macaca nemestrina"],
["Piliocolobus tephrosceles","Colobus angolensis palliatus"],
["Trachypithecus francoisi","Rhinopithecus roxellana","Rhinopithecus bieti"]
]

df = pd.read_csv('tblastn_id80_cover80_cds_cgc_728-4_dedup_fixed_gene_proper_set.csv', index_col=0)


# Large clades
clade_info = []
# For each column, check if it meets the criteria
for col in df.columns:
    selected, zero_clades, one_clades = is_selected_column(df[col], clades)
    clade_info.append([col, zero_clades, one_clades])

# Record the clades with all 0s and clades with all 1s 
df_clade_info = pd.DataFrame(clade_info, columns=['Column', 'Zero Clades', 'One Clades'])
df_clade_info.to_csv('cgc724_clades3_clade_info_proper_set.csv')


# Small clades
clade_info = []
# For each column, check if it meets the criteria
for col in df.columns:
    selected, zero_clades, one_clades = is_selected_column(df[col], small_clades)
    clade_info.append([col, zero_clades, one_clades])

# Record the clades with all 0s and clades with all 1s 
df_clade_info = pd.DataFrame(clade_info, columns=['Column', 'Zero Clades', 'One Clades'])
df_clade_info.to_csv('cgc724_clades3_clade_info_proper_set_small.csv')



