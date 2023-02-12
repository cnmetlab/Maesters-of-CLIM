import pandas as pd
import numpy as np

def generate_enso_from_nina34a(df:pd.DataFrame,column:str)->pd.Series:
    df = df.copy()
    df['enso'] = np.where(df[column]>0.4, 1, np.nan)
    df['enso'] = np.where(df[column].isna() & (df[column]<-0.4), -1, df['enso'])
    df['flag'] = np.where(df['enso'] != df['enso'].shift(1), 1, 0)
    df['flag_cumsum'] = df['flag'].cumsum()
    se_group = df.groupby(df['flag'].cumsum())['flag'].count()
    df['flag_count'] = df['flag_cumsum'].apply(lambda x: se_group.loc[x])
    
    df['enso'] = np.where(df['flag_count']>=6, df['enso'], np.nan)
    # TODO
    return df


