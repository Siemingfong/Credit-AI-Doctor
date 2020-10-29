from bs4 import BeautifulSoup
from tqdm import trange
import pandas as pd
import requests


def main(params):
    final_df = pd.DataFrame(columns = params['columns'])
    for page in trange(100):
        form_data = params['form_data'].copy()
        if page < 10:
            form_data['code'] = '0' + str(page + 1)
            form_data['slt'] = '0' + str(page + 1)
        else:
            form_data['code'] = str(page + 1)
            form_data['slt'] = str(page + 1)
        
        response = requests.post(params['main_url'], data = form_data)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        
        cur_data = []
        final_data = []
        trs = soup.findAll('tr')
        if len(trs):
            for tr in trs:
                tds = tr.findAll('td')
                if len(tds) == 6:
                    for i in range(len(tds)):
                        cur_data.append(tds[i].text)
                    final_data.append(cur_data)
                    cur_data = []
                if len(tds) == 19:
                    for i in range(len(tds)):
                        cur_data.append(tds[i].text)
            df = pd.DataFrame(final_data, columns = params['columns'])
            final_df = pd.concat([final_df, df])
            # df.to_csv('industry_%s.csv' % form_data['code'], index=False, encoding='utf-8-sig')
        else:
            continue
    final_df.to_csv('industry_all.csv', index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    PARAMS = {}
    PARAMS['main_url'] = 'https://mops.twse.com.tw/mops/web/ajax_t123sb09'
    PARAMS['form_data'] = {'encodeURIComponent': '1',
                           'TYPEK': 'sii',
                           'step': '1',
                           'firstin': '1',
                           'code': '01',
                           'slt': '01'}
    PARAMS['columns'] = ['產業類別', '證券代號', '公司名稱', '快速連結', '每股淨值', '指標1', 
                         '指標2_1_1', '指標2_2_1', '指標2_3_1', '指標3_1', '指標3_2',
                         '指標4_1_1', '指標4_2_1', '指標4_3_1', '指標5', '指標6', '指標7', 
                         '指標8', '指標9', '指標2_1_2', '指標2_2_2', '指標2_3_2',
                         '指標4_1_2', '指標4_2_2', '指標4_3_2']
    
    main(PARAMS)