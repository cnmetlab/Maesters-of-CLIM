from maesters_of_clim.fetcher.iri import get_iri_ensoprob_forecast
from maesters_of_clim.fetcher.psl import get_psl_index_history
from maesters_of_clim.fetcher.ncei import get_ncei_index_history
from maesters_of_clim.fetcher.jamstec import get_jamstec_dmi_forecast
from maesters_of_clim.config import load_config

import pandas as pd

from datetime import datetime

class Climate_Maester:
    def __init__(self,
        indexes:list,
        source:str=None
        ) -> None:
        if isinstance(indexes, str):
            indexes = [indexes]
        self.indexes = indexes
        self.source = source
        pass
    
    def history(self)->pd.DataFrame:
        if self.source == 'psl':
            df = None
            for i in self.indexes:
                tmp = get_psl_index_history(i)
                if df is None:
                    df = tmp
                else:
                    df = df.merge(tmp, how='outer', on='month')
        elif self.source == 'ncei':
            df = None
            for i in self.indexes:
                tmp = get_ncei_index_history(i)
                if df is None:
                    df = tmp
                else:
                    df = df.merge(tmp, how='outer', on='month')

        return df

    def forecast(self, pred_at:datetime=None, source:str=None)->pd.DataFrame:
        source = self.source if source is None else source
        if source in ['iri', 'cpc'] and 'enso' in self.indexes:
            df = get_iri_ensoprob_forecast(pred_month=pred_at, source=source)
        elif source in ['jamstec'] and 'dmi' in self.indexes:
            df = get_jamstec_dmi_forecast()
        elif self.source is not None:
            df = get_iri_ensoprob_forecast(pred_month=pred_at, source=source)
        else:
            df = get_iri_ensoprob_forecast(pred_month=pred_at)
        return df
    
    @staticmethod
    def list_history_indexes(source:str=None):
        if source is None:
            source = ['ncei', 'psl']
        elif isinstance(source, str):
            source = [source]
        config = load_config('index_history')
        result = {s: [] for s in source}
        for s in source:
            idxes = [i for i in config.get(s, {}).keys() if i != 'default']
            result[s].extend(idxes)
        return result
            