from maesters_of_clim.config import load_config

from bs4 import BeautifulSoup
import pandas as pd
from retrying import retry

from datetime import datetime, timedelta
import calendar
import requests

iri_index_forecast = load_config('index_forecast').get('iri')

nina34a_url = iri_index_forecast.get('nina34a').get('index_url')

def parse_table(table):
    thead = table.find('thead').find('tr')
    tbody = table.find('tbody').find_all('tr')
    columns = [c.text.strip() for c in thead.find_all('th')]
    data = []
    for row in tbody:
        row_data = row.find_all('td')
        data.append([d.text.strip() for d in row_data])

    if len(data)==0:
        return None

    return pd.DataFrame(data=data, columns=columns)


def parse_ensotable_response(response:requests.Response, source:str)->pd.DataFrame:
    """parse iri enso table from response

    Args:
        response (requests.Response): _description_
        source (str, optional): _description_. Defaults to 'iri'.

    Returns:
        pd.DataFrame: _description_
    """
    bs_items = BeautifulSoup(response.text, "html.parser")
    enso_tables = bs_items.find_all('table', attrs={'class':'ensoprob'})
    if source == 'cpc':
        return parse_table(enso_tables[0])
    elif source == 'iri':
        return parse_table(enso_tables[1])
    


def month2season(month:int)->str:
    month_dict = {
        1: 'DJF',
        2: 'JFM',
        3: 'FMA',
        4: 'MAM',
        5: 'AMJ',
        6: 'MJJ',
        7: 'JJA',
        8: 'JAS',
        9: 'ASO',
        10: 'SON',
        11: 'OND',
        12: 'NDJ',
    }
    return month_dict.get(month)

def season2month(season:str)->int:
    if len(season)>3:
        season=season[:3]
    season_dict = {
        'DJF': 1,
        'JFM': 2,
        'FMA': 3,
        'MAM': 4,
        'AMJ': 5,
        'MJJ': 6,
        'JJA': 7,
        'JAS': 8,
        'ASO': 9,
        'SON': 10,
        'OND': 11,
        'NDJ': 12,
    }
    return season_dict.get(season)


def format_iri(pred_month:datetime, df:pd.DataFrame)->pd.DataFrame:
    """format iri table

    Args:
        pred_month (datetime): _description_
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # if source == 'cpc':
    #     _,monthend = calendar.monthrange(pred_month.year, pred_month.month)
    #     pred_month =pred_month.replace(day=monthend) + timedelta(days=1)
    pred_month= pred_month.replace(day=1)

    df['Release_Month'] = pred_month.strftime('%Y-%m')
    df['Forecast_Season'] = df['Season'].apply(season2month)
    df['Forecast_Season'] = df['Forecast_Season'].apply(
        lambda x: f'{pred_month.year + 1}-{x:02}' if x - pred_month.month < 0 else f'{pred_month.year}-{x:02}'
        )
    df = df.rename(columns={'La Niña': 'LaNina', 'El Niño': 'ElNino'})
    return df


@retry(stop_max_attempt_number=5)
def get_iri_ensoprob_forecast(pred_month:datetime, source:str='iri')->pd.DataFrame:
    """ENSO Probability base on NINO3.4 SST Anomaly

    Args:
        pred_month (datetime): _description_
        source (str, optional): _description_. Defaults to 'iri'.

    Returns:
        pd.DataFrame: _description_
    """
    month_name = calendar.month_name[pred_month.month]
    request_url = pred_month.strftime(nina34a_url).format(MONTH_ENG=month_name, SOURCE=source)
    response = requests.get(
        request_url,
        timeout=5,
        )
    if response.status_code == 200:
        df = parse_ensotable_response(response, source)
        if df is not None:
            df = format_iri(pred_month, df)
        return df
    else:
        return None