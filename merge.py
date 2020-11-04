from bs4 import BeautifulSoup
from tqdm import trange, tqdm
import pandas as pd
import requests


def replace_all_df(text, lis):
    for i in lis:
        text = text.str.replace(i, '')
    return text

def replace_all(text, lis):
    for i in lis:
        text = text.replace(i, '')
    return text

def preprocess_twrating_cns(df, rep):
    cns = df['en_name'].str.lower().str.strip()
    df['en_name'] = replace_all_df(cns, rep)
    return df
    
# def main(params):
#     df1 = pd.read_csv(params['mops_data'])
#     df2 = pd.read_csv(params['twrating_data'])
    
#     rep = ['corporation', 'corp', 'ltd', 'co', ',', '.', ' ', '&']
#     df2 = preprocess_twrating_cns(df2, rep)
#     print(df2['entity'])
#     for idx, row in df1.iterrows():
#         cn = row['en_name'].lower().strip()
#         cn = replace_all(cn, rep)
#         # print(cn)
#         if row['證券代號'] == 1303:
#             print(cn)
#             print(df2['entity'].loc[0])
#         if cn in list(df2['entity']):
#             print('Yoooooo!')

def main(params):
    df1 = pd.read_csv(params['mops_data'])
    df2 = pd.read_csv(params['twrating_data'])
    
    rep = ['corporation', 'corp', 'ltd', 'co', ',', '.', ' ', '&']
    df1 = preprocess_twrating_cns(df1, rep)
    print(df1)

    for idx, row in df2.iterrows():
        cn = row['entity'].lower().strip()
        cn = replace_all(cn, rep)

        if cn in list(df1['en_name']):
            print('Yoooooo!')
        else:
            print(cn)
            

if __name__ == '__main__':
    PARAMS = {}
    PARAMS['mops_data'] = 'industry_all.csv'
    PARAMS['twrating_data'] = 'twrating.csv'
    
    main(PARAMS)