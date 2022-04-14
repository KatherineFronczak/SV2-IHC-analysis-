import pandas as pd
import re
import numpy as np


#clean data
SV2_df = pd.read_csv('SV2_IHC.csv')
SV2_df.columns = SV2_df.columns.str.strip()
SV2_df['status'] = SV2_df['status'].str.strip()

#seperate injured and sham animals
SV2_sham_df = SV2_df.where(SV2_df['status']=='sham').dropna()
SV2_Inj_df = SV2_df.where(SV2_df['status']=='Inj').dropna()

#regex pattern for finding columns
iA = "^i.+A$"
cA = "^c.+A$"
iB = "^i.+B$"
cB = "^c.+B$"

#seperate data into unique groups (injured vs sham, ipsilateral vs contralateral, SV2A vs SV2B)
def split(df,r):
    return df.filter(regex=r)

SV2A_isham_df = split(SV2_sham_df,iA)
SV2A_csham_df = split(SV2_sham_df,cA)
SV2A_iInj_df = split(SV2_Inj_df,iA)
SV2A_cInj_df = split(SV2_Inj_df,cA)

SV2B_isham_df = split(SV2_sham_df,iB)
SV2B_csham_df = split(SV2_sham_df,cB)
SV2B_iInj_df = split(SV2_Inj_df,iB)
SV2B_cInj_df = split(SV2_Inj_df,cB)

#normalizing data by subtracting background white matter from each of the other values for an animal
def norm(df,b):
    df = df.sub(df[b], axis=0)
    return df.drop([b], axis=1)

SV2A_isham_df = norm(SV2A_isham_df,'iWM-A')
SV2A_csham_df = norm(SV2A_csham_df,'cWM-A')
SV2A_iInj_df = norm(SV2A_iInj_df,'iWM-A')
SV2A_cInj_df = norm(SV2A_cInj_df,'cWM-A')

SV2B_isham_df = norm(SV2B_isham_df,'iWM-B')
SV2B_csham_df = norm(SV2B_csham_df,'cWM-B')
SV2B_iInj_df = norm(SV2B_iInj_df,'iWM-B')
SV2B_cInj_df = norm(SV2B_cInj_df,'cWM-B')

#claculating %diff by dividing each value in column by mean of a column (for shams)
sh_ls = [SV2A_isham_df,SV2A_csham_df,SV2B_isham_df,SV2B_csham_df]
df_norm_sham = []
sham_mn = []

for df in  sh_ls:
    mn = df.mean()
    sham_mn.append(mn)
    n=0
    ser_norm_ls = []
    for col in df:
        ser_norm =df[col].apply(lambda x: (x/mn[n])*100)
        n+=1
        ser_norm_ls.append(ser_norm)
    df_norm = pd.DataFrame(ser_norm_ls).T
    df_norm.columns = ['Hil','Gran','Mol','CA3','CA2','CA1']
    df_norm_sham.append(df_norm)


#calculating %diff to sham means by dividing each value in column by mean of corresponding sham column (ie "sham contra SV2A CA1" to "Inj contra SV2A CA1")
Inj_ls = [SV2A_iInj_df,SV2A_cInj_df,SV2B_iInj_df,SV2B_cInj_df]
df_norm_Inj = []
w=0

for df in  Inj_ls:
    mn = sham_mn[w]
    w+=1
    n=0
    ser_norm_ls = []
    for col in df:
        ser_norm =df[col].apply(lambda x: (x/mn[n])*100)
        n+=1
        ser_norm_ls.append(ser_norm)
    df_norm = pd.DataFrame(ser_norm_ls).T
    df_norm.columns = ['Hil','Gran','Mol','CA3','CA2','CA1']
    df_norm_Inj.append(df_norm)

#unpacking lists of df to relabel
SV2A_isham_df = df_norm_sham[0]
SV2A_csham_df = df_norm_sham[1]
SV2A_iInj_df = df_norm_Inj[0]
SV2A_cInj_df = df_norm_Inj[1]

SV2B_isham_df = df_norm_sham[2]
SV2B_csham_df = df_norm_sham[3]
SV2B_iInj_df = df_norm_Inj[2]
SV2B_cInj_df = df_norm_Inj[3]
