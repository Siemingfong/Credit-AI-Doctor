from bs4 import BeautifulSoup
from tqdm import trange
import pandas as pd
import requests
import sys


def main(params):
    url = 'https://www.taiwanratings.com/portal/front/sp?fbclid=IwAR2h6sYLuv_ZrfpIX_Li4X0CLAnTM4stgQqLVCkGzw77lM7yXcGTCYYluh0'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'lxml')  # 'html.parser'
    
    table = soup.find('table', {'class': 'listsnprating'})
    table_rows = table.find_all('tr')    
    
    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td]
        l.append(row)

    df = pd.DataFrame(l, columns = params['columns'])
    df.dropna(axis=0, how='any', inplace=True)
    for i in range(2, 4):
        df[params['columns'][i]] = df[params['columns'][i]].str.split('/').str.get(0).str.strip()
    
    df.to_csv(params['csv_name'], index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    PARAMS = {}
    PARAMS['csv_name'] = 'twrating.csv'
    PARAMS['columns'] = ['entity', 'rating_date', 'local_currency', 'foreign_currency']
    
    main(PARAMS)