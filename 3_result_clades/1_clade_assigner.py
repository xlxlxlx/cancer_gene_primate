import pandas as pd

ratio_thre = 1

fn = f"cds_cgc_primate_genes_proper_subset"
df = pd.read_csv(f'{fn}.csv', index_col=0)


def is_selected_column(column, clades):
    """
    Check if the column should be selected based on clades.
    """
    zeros_in_clade = False
    ones_in_clade = False
    zero_clades = []
    one_clades = []

    # check each clade
    for clade in clades:
        sub_col = column[clade]
        zero_ratio = (sub_col == 0).sum() / len(sub_col)
        one_ratio = (sub_col == 1).sum() / len(sub_col)

        if zero_ratio >= ratio_thre:
            zeros_in_clade = True
            zero_clades.append(clade)
        if one_ratio >= ratio_thre:
            ones_in_clade = True
            one_clades.append(clade)
    
    print(zero_clades, zeros_in_clade)
    if zeros_in_clade and ones_in_clade:
        return True, zero_clades, one_clades

    return False, zero_clades, one_clades

# clades 
clades = [["Otolemur garnettii","Prolemur simus","Lemur catta","Propithecus coquereli","Microcebus murinus"],
["Callithrix jacchus","Aotus nancymaae","Saimiri boliviensis boliviensis","Cebus imitator","Cebus capucinus","Sapajus apella"],
["Chlorocebus sabaeus","Mandrillus leucophaeus","Cercocebus atys","Papio anubis","Theropithecus gelada","Macaca fascicularis","Macaca mulatta","Macaca nemestrina"],
["Piliocolobus tephrosceles","Colobus angolensis palliatus","Trachypithecus francoisi","Rhinopithecus roxellana","Rhinopithecus bieti"]
]

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

clade_info = []

# large clades
for col in df.columns:
    selected, zero_clades, one_clades = is_selected_column(df[col], clades)
    clade_info.append([col, zero_clades, one_clades])

df_clade_info = pd.DataFrame(clade_info, columns=['Column', 'Zero Clades', 'One Clades'])
df_clade_info.to_csv(f'{fn}_clade_large.csv')


# small clades
clade_info = []

for col in df.columns:
    selected, zero_clades, one_clades = is_selected_column(df[col], small_clades)
    clade_info.append([col, zero_clades, one_clades])

df_clade_info = pd.DataFrame(clade_info, columns=['Column', 'Zero Clades', 'One Clades'])
df_clade_info.to_csv(f'{fn}_clade_small.csv')
