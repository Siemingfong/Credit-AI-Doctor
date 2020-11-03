from bs4 import BeautifulSoup
from tqdm import trange, tqdm
import pandas as pd
import requests
import time
import os


def get_company_en_name(params):
    company_ids = params['final_df']['證券代號']
    for i in trange(len(company_ids)):
        if params['final_df']['en_name'].loc[i] == 0:
            form_data = {
                'inpuType': 'pro_co_id',
                'step': '0a',
                'co_id': '%s' % company_ids[i],
                'caption_id': '000001',
                'keyword': '',
            }
            url = 'https://emops.twse.com.tw/server-java/t58query'
            try:
                response = requests.post(url, data = form_data)
                content = response.content
                soup = BeautifulSoup(content, 'html.parser')

                title = soup.find_all('div', {'id': 'tabtitle'})
                if title:
                    title = title[0].findChildren('div', recursive=False)[0].text.split('(')[0]
                    params['final_df']['en_name'].loc[i] = title
                    print(params['final_df']['en_name'].loc[i])
                else:
                    params['final_df']['en_name'].loc[i] = 0
                params['final_df'].to_csv(params['csv_name'], index=False, encoding='utf-8-sig')
                time.sleep(1)
            except:
                print('[Err] Error happens in cid: %s' % company_ids[i])
                time.sleep(5)


def crawl_mops_indicators(params):
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
        else:
            continue
    final_df.to_csv(params['csv_name'], index=False, encoding='utf-8-sig')
    params['final_df'] = final_df


def main(params):
    files = os.listdir('./')
    if params['csv_name'] in files:
        params['final_df'] = pd.read_csv('./industry_all.csv')
        if 'en_name' not in params['final_df'].columns:
            params['final_df']['en_name'] = 0
            get_company_en_name(params)
        else:
            get_company_en_name(params)
    else:
        crawl_mops_indicators(params)
        get_company_en_name(params)


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
    PARAMS['csv_name'] = 'industry_all.csv'
    PARAMS['final_df'] = None
    main(PARAMS)