# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:41:13 2016

@author: lsiqueira
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#sns.set(color_codes=True)

AO = pd.read_table('./data/monthly.ao.index.b50.current.ascii', sep='\s*', \
              parse_dates={'dates':[0, 1]}, header=None, index_col=0, squeeze=True)
NAO = pd.read_table('./data/norm.nao.monthly.b5001.current.ascii', sep='\s*', \
              parse_dates={'dates':[0, 1]}, header=None, index_col=0, squeeze=True)
PNA = pd.read_table('./data/norm.pna.monthly.b5001.current.ascii', sep='\s*', \
              parse_dates={'dates':[0, 1]}, header=None, index_col=0, squeeze=True)

ind = pd.DataFrame({'AO':AO, 'NAO':NAO, 'PNA':PNA})

ind.plot()
figname  ='./figs/fig1.pdf'
plt.subplots_adjust(left=0.1, right=0.92, bottom=0.1, top=0.98)
plt.savefig(figname, bbox_inches=0)

ao = np.asarray(ind.ix[:,0])
nao = np.asarray(ind.ix[:,1])
pna = np.asarray(ind.ix[:,2])
data = [ao, nao, pna]    
R = np.corrcoef(data)   

mask = np.zeros_like(R)
mask[np.triu_indices_from(mask)] = True
fig2 = plt.figure()
bx = fig2.add_subplot(1, 1, 1)
cbar_options = {'extend':'both','orientation':"vertical",
                'shrink':0.8,'fraction':.10,'pad':.02}
with sns.axes_style("white"):
    ax = sns.heatmap(R, mask=mask, vmax=1.0, square=True, linewidths=1.,
                     annot=True, fmt='1.2f', cbar_kws=cbar_options)
ax.set_xticklabels(['AO', 'NAO', 'PNA'],fontsize=14)
ax.set_yticklabels(['AO', 'NAO', 'PNA'],fontsize=14)
plt.title(r'Correlation', fontsize = 18)
figname  ='./figs/fig2.pdf'
plt.subplots_adjust(left=0.1, right=0.92, bottom=0.1, top=0.95)
plt.savefig(figname, bbox_inches=0)

sns.jointplot('AO', 'NAO', data=ind, kind='reg', size=7)
figname  ='./figs/fig3.pdf'
plt.subplots_adjust(left=0.1, right=0.92, bottom=0.1, top=0.98)
plt.savefig(figname, bbox_inches=0)
#plt.show()
