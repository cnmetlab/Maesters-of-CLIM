from maesters_of_clim.config import load_config

import numpy as np
import pandas as pd

psl_index_history = load_config('index_history').get('psl')


def is_yearstr(s:str)->bool:
    try:
        intstr = int(s)
        if intstr > 0 and intstr < 2200:
            return True
        else:
            return False
    except:
        return False

def format_psl_default(df:pd.DataFrame, colname:str, missing:float=-99.99)->pd.DataFrame:
    df = df[df['year'].apply(is_yearstr)]
    df = df[~df.isna().any(axis=1)]
    df = df.set_index('year').astype(float)
    df = df.applymap(lambda x: np.nan if x==missing else x)
    df_list = []
    for n,i in df.iterrows():
        tmp  = i.T
        tmp.index = tmp.index.map(lambda x: f'{n}-{x.zfill(2)}')
        df_list.append(tmp)
    res = pd.concat(df_list).to_frame(name=colname)
    res = res.reset_index()
    res = res.rename(columns={'index': 'month'})
    res['month'] = pd.to_datetime(res['month'])
    return res

def get_psl_url(index_name:str)->dict:
    return psl_index_history.get(index_name)

def get_psl_index_history(index_name:str)->pd.DataFrame:
    index_dict = get_psl_url(index_name)
    index_url = index_dict.get('index_url')
    columns = index_dict.get('columns', psl_index_history.get('default').get('columns'))
    missing = index_dict.get('missing', psl_index_history.get('default').get('missing'))
    df = pd.read_csv(index_url, delimiter='\s+', names=columns)

    if index_name in []:
        pass
    else:
        df = format_psl_default(df, colname=index_name, missing=missing)
    return df


