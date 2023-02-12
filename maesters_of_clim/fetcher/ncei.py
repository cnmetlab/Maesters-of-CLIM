from maesters_of_clim.config import load_config

import numpy as np
import pandas as pd

ncei_index_history = load_config('index_history').get('ncei')


def is_yearstr(s:str)->bool:
    try:
        intstr = int(s)
        if intstr > 0 and intstr < 2200:
            return True
        else:
            return False
    except:
        return False

def format_ncei_default(df:pd.DataFrame,colname:str, missing:float=99.99)->pd.DataFrame:
    df = df[df['year'].apply(is_yearstr)]
    df = df[~df.isna().any(axis=1)]
    df['month'] = df.apply(lambda x: f"{int(x['year'])}-{int(x['month']):02}", axis=1)
    df.pop('year')
    df['month'] = pd.to_datetime(df['month'])
    if colname in df.columns:
        df = df[['month', colname]]
    
    return df

def format_ncei_month_col(df, colname:str, missing:float=99.99)->pd.DataFrame:
    df = df[df['year'].apply(is_yearstr)]
    df = df[~df.isna().any(axis=1)]
    df = df.set_index('year').astype(float)
    df_list = []
    for n,i in df.iterrows():
        tmp  = i.T
        tmp.index = tmp.index.map(lambda x: f'{n}-{x.zfill(2)}')
        df_list.append(tmp)
    res = pd.concat(df_list).to_frame(name=colname)
    res = res.reset_index()
    res = res.rename(columns={'index': 'month'})
    res['month'] = pd.to_datetime(res['month'])
    
    res = res.set_index('month').applymap(lambda x: np.nan if x==missing else x)
    return res.reset_index()

def get_ncei_url(index_name:str)->dict:
    return ncei_index_history.get(index_name)

def get_ncei_index_history(index_name:str)->pd.DataFrame:
    if index_name in ['nina12a', 'nina34a', 'nina3a', 'nina4a', 'all']:
        ncei_index = 'ninaa'
    elif index_name in ['nina12', 'nina34', 'nina3', 'nina4']:
        ncei_index = 'nina'
    else:
        ncei_index = index_name
    
    index_dict = get_ncei_url(ncei_index)
    index_url = index_dict.get('index_url')
    columns = index_dict.get('columns', ncei_index_history.get('default').get('columns'))
    missing = index_dict.get('missing', ncei_index_history.get('default').get('missing'))
    skiprows =  index_dict.get('skiprows', ncei_index_history.get('default').get('skiprows'))
    df = pd.read_csv(index_url, delimiter='\s+', names=columns, skiprows=skiprows)

    if index_name in ['pdo']:
        df = format_ncei_month_col(df, index_name,)
    else:
        df = format_ncei_default(df, index_name)
    return df


