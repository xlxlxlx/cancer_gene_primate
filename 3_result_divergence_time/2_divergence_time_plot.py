#########
# Input: (1) a table storing number of cds/genome hits 
#            in each primate clade 
#            (output of divergence_time_clades_hits.py)
#        (2) climate66mya.csv table
# Output: a plot shows estimated gene frequency along with
#         global surface temperature in recent 66 million years
#########

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# this is the output of divergence_time_clades_hits.py
fn = "clades_gene_hits_0.8_dedup.csv"
df = pd.read_csv(fn)

fn2 = "climate66mya.csv"
df2 = pd.read_csv(fn2)

fig, ax=plt.subplots(figsize=(40, 20))

ax.plot(df.divergence_time, df.count_cds_random339, marker="o", color="blue")
ax.plot(df.divergence_time, df.count_cds_cgc, marker="o", color="red")

ax.set_ylim(ymin=0)
ax.set_yticks(range(0, 150, 5))
ax.set_xlabel("Time (Ma)", fontsize=30)
ax.set_ylabel("# Emerged Gene (estimated)", fontsize=30)
ax.legend([])
ax.tick_params(axis='x', which='both', labelsize=20)
ax.tick_params(axis='y', which='both', labelsize=22)
ax.invert_xaxis()

x_axis_list = np.arange(0, 71)
ax.set_xticks(range(0, 71, 1))
ax.set_xticks(x_axis_list)

for (tickvalue, ticklbl) in zip(x_axis_list, ax.xaxis.get_ticklabels()):
    ticklbl.set_color('blue' if tickvalue % 5 == 0 else 'black')

plt.savefig('output_plot.png',  bbox_inches='tight')
plt.show()