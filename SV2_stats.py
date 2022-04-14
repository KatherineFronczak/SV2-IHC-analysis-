from SV2_analysis import *
import scipy.stats as stats
from scipy.stats import ttest_ind

#prep for making 3 tuples of inj df, sham df, and region
sham_ls = [SV2A_isham_df,SV2A_csham_df,SV2B_isham_df,SV2B_csham_df]
Inj_ls = [SV2A_iInj_df,SV2A_cInj_df,SV2B_iInj_df,SV2B_cInj_df]
regions = ['Hil','Gran','Mol','CA3','CA2','CA1']

#make 2 tuple of inj and sham dfs
s_I_zip = list(zip(sham_ls,Inj_ls))

#make 3 tuple with each region for inj and sham pairs
s_I_r_zip = []
for i in s_I_zip:
    for u in regions:
        tup = i +(u,)
        s_I_r_zip.append(tup)

#calculate pvals using students t-test, comparing inj and sham for each region
pvals = []
for x,y,z in s_I_r_zip:
    t_stat, p = ttest_ind(x[z], y[z])
    pvals.append(p)

#list for making dictionary with pvals and labels 
names = ['iA_Hil','iA_Gran','iA_Mol','iA_CA3','iA_CA2','iA_CA1',
'cA_Hil','cA_Gran','cA_Mol','cA_CA3','cA_CA2','cA_CA1',
'iB_Hil','iB_Gran','iB_Mol','iB_CA3','iB_CA2','iB_CA1',
'cB_Hil','cB_Gran','cB_Mol','cB_CA3','cB_CA2','cB_CA1']

pvals_dic = dict(zip(names,pvals))
