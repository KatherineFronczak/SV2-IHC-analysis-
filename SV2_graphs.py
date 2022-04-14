from SV2_analysis import *
import matplotlib.pyplot as plt

#calculate mean of all subregions
def summary(df1, df2):
    df1_m = df1.mean().rename('sham')
    df2_m = df2.mean().rename('inj')
    #combine all like groups for comparison (sham vs inj)
    df = pd.DataFrame([df1_m, df2_m])
    df = df.T
    x = df.plot.bar()
    return plt.show()

#graph all of the like groups (sham vs inj)
iA_graph = summary(SV2A_isham_df,SV2A_iInj_df)
cA_graph = summary(SV2A_csham_df,SV2A_cInj_df)
iB_graph = summary(SV2B_isham_df,SV2B_iInj_df)
cB_graph = summary(SV2B_csham_df,SV2B_cInj_df)

print(iA_graph)
print(cA_graph)
print(iB_graph)
print(cB_graph)
