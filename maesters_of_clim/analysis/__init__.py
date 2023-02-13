import pandas as pd
import numpy as np

def enso_event(df:pd.DataFrame,column:str, temp:float, months:int=6)->pd.Series:
    """calc enso event that higher/lower than temp (degree celcius) for more than NUM consecutive months

    Args:
        df (pd.DataFrame): _description_
        column (str): _description_
        temp (float): _description_
        months (int, optional): _description_. Defaults to 6.

    Returns:
        pd.Series: 1 is ElNino/-1 LaNina/np.nan Neutral
    """
    df = df.copy()
    df['enso'] = np.where(df[column]>temp, 1, np.nan)
    df['enso'] = np.where((df['enso'].isna() & (df[column]<-temp)), -1, df['enso'])
    df['flag'] = np.where(df['enso'] != df['enso'].shift(1), 1, 0)
    df['flag_cumsum'] = df['flag'].cumsum()
    se_group = df.groupby(df['flag'].cumsum())['flag'].count()
    df['flag_count'] = df['flag_cumsum'].apply(lambda x: se_group.loc[x])
    df['enso'] = np.where(df['flag_count']>=months, df['enso'], np.nan)
    df['enso_flag'] = np.where(df['enso'] != df['enso'].shift(1), 0, 1)
    df['enso_flag_cumsum'] = df['enso_flag'].cumsum()
    df['enso'] = np.where((~df['enso'].isna()) &(df['enso_flag_cumsum']>=months-1), df['enso'],np.nan)
    return df['enso']


