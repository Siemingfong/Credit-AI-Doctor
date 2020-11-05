from bs4 import BeautifulSoup
from tqdm import trange, tqdm
import pandas as pd
import requests


def replace_all_df(text, lis, mode):
    if mode == 'list':
        for i in lis:
            text = text.str.replace(i, '')
    elif mode == 'dict':
        for k, v in lis.items():
            text = text.str.replace(k, v)
    return text

def replace_all(text, lis, mode):
    if mode == 'list':
        for i in lis:
            text = text.replace(i, '')
    elif mode == 'dict':
        for k, v in lis.items():
            text = text.replace(k, v)
    return text

def preprocess_twrating_cns(df, rep, which=None, mode='list'):
    cns = df[which].str.lower().str.strip()
    df['merge_key'] = replace_all_df(cns, rep, mode)
    return df

def main(params):
    df1 = pd.read_csv(params['mops_data'])
    df2 = pd.read_csv(params['twrating_data'])
    
    rep1 = ['corporation', 'financial', 'industry', 'company', 'limited',
           'corp', 'ltd', 'inc', 'ind', 'the', 'co.', 
           ',', '.', ' ', '&', '(', ')']
    rep2 = {'holdings': 'holding'}
    # process twrating keys (df1)
    df1 = preprocess_twrating_cns(df1, rep1, 'en_name', mode='list')
    df1 = preprocess_twrating_cns(df1, rep2, 'merge_key', mode='dict')
    # print(df1)

    # process mops keys (df2)
    df2 = preprocess_twrating_cns(df2, rep1, 'entity', mode='list')
    df2 = preprocess_twrating_cns(df2, rep2, 'merge_key', mode='dict')
    # print(df2)
    
    df2 = df2.merge(df1, how='right', left_on='merge_key', right_on='merge_key')
    df2 = df2.drop(['entity', 'merge_key'], axis=1)
    df2.to_csv('industry_all_merge.csv', index=False, encoding='utf-8-sig')
            

if __name__ == '__main__':
    PARAMS = {}
    PARAMS['mops_data'] = 'industry_all.csv'
    PARAMS['twrating_data'] = 'twrating.csv'
    
    main(PARAMS)