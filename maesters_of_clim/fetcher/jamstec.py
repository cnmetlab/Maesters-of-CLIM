from maesters_of_clim.config import load_config

from bs4 import BeautifulSoup
import pandas as pd
from retrying import retry

from datetime import datetime, timedelta
import calendar
import requests

iri_index_forecast = load_config('index_forecast').get('jamstec')

dmi_url = iri_index_forecast.get('dmi').get('index_url')


@retry(stop_max_attempt_number=5)
def get_jamstec_dmi_forecast() -> pd.DataFrame:
    df = pd.read_csv(dmi_url, parse_dates=['time'])
    df = df.sort_values('time').set_index('time')
    release_month = df[df.isna().all(axis=1).values].iloc[0].name
    forecast_cols = ['Mean'] + list(set(df.columns) - set(['Obs', 'time', 'Mean']))
    df['Forecast_Month'] = df.index.map(lambda x: x.strftime('%Y-%m'))
    df['Release_Month'] = release_month.strftime('%Y-%m')
    return df[df.index>release_month].reset_index()[forecast_cols+['Forecast_Month', 'Release_Month']]
