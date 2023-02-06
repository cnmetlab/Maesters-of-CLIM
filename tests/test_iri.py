from maesters_of_clim.fetcher.iri import get_iri_ensoprob_forecast

from datetime import datetime

def test_get_enso_forecast():
    cpc_forecast = get_iri_ensoprob_forecast(datetime(2022, 10, 1), 'cpc')
    iri_forecast = get_iri_ensoprob_forecast(datetime(2021, 5, 1), 'iri')

