###########
# imports #
###########
import scrublet as scr
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from numpy import savetxt

# Image parameters
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rc('font', size=14)
plt.rcParams['pdf.fonttype'] = 42
# 

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

jobname = sys.argv[1]
inputfolder = sys.argv[2]
outputfolder = sys.argv[3]
npcs = int(sys.argv[4])
# 

counts_matrix = scipy.io.mmread(inputfolder + '/' + jobname + '_filtered.mtx').T.tocsc()

print('Counts matrix shape: {} rows, {} columns'.format(counts_matrix.shape[0], counts_matrix.shape[1]))


scrub = scr.Scrublet(counts_matrix, expected_doublet_rate=0.06)

doublet_scores, predicted_doublets = scrub.scrub_doublets(min_counts=2, 
                                                          min_cells=3, 
                                                          min_gene_variability_pctl=85, 
                                                          n_prin_comps=npcs)

scrub.call_doublets(threshold=0.25)

# Duplet score for cells
savetxt(outputfolder + '/' + jobname + '_duplets_score.csv', scrub.doublet_scores_obs_, delimiter=',')
# Simulated duplets
savetxt(outputfolder + '/' + jobname + '_sim_duplets_score.csv', scrub.doublet_scores_sim_, delimiter=',')

# UMAP
print('Running UMAP...')
umap = scr.get_umap(scrub.manifold_obs_, n_neighbors=10, min_dist=0.1)
savetxt(outputfolder + '/' + jobname + '_umap_scrublet.csv', umap, delimiter=',')

   
print('Done.')

