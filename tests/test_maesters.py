from maesters_of_clim import Climate_Maester

from datetime import datetime


def test_clim_maesters_history():
    c = Climate_Maester(['nina34a', 'pdo'], 'psl')
    df = c.history()

def test_clim_maesters_enso_forecast():
    c = Climate_Maester('enso', 'iri')
    iridf = c.forecast(pred_at=datetime(2022, 10, 1))
    c = Climate_Maester('enso', 'cpc')
    cpcdf = c.forecast(pred_at=datetime(2022, 10, 1))

