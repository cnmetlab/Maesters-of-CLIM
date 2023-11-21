# Maesters-of-Clim

![](./static/maesters_of_clim.jpg)

Maesters-of-Clim tempt to help retriving climate data (climate index, reanalysis) from the main-stream climate insitution (like IRI, PSL, NCEI, RDA). 

The following support

|Institution|Source|DataType|DataName|FetchData|
|--|--|--|--|--|
|IRI|IRI|forecast|ENSO Probability|`Climate_Maester(['enso'], 'iri').forecast(pred_at=date)`|
|IRI|CPC|forecast|ENSO Probability|`Climate_Maester(['enso'], 'cpc').forecast(pred_at=date)`|
|PSL/NCEI|PSL/NCEI|history|Nina 34 Anomaly|`Climate_Maester(['nina34a'], 'ncei').history()`|
|PSL/NCEI|PSL/NCEI|history|Nina 3 Anomaly|`Climate_Maester(['nina3'], 'ncei').history()`|
|PSL/NCEI|PSL/NCEI|history|Nina 4 Anomaly|`Climate_Maester(['nina4'], 'ncei').history()`|
|PSL|PSL|history|Nina 1 Anomaly|`Climate_Maester(['nina1a'], 'psl').history()`|
|NCEI|NCEI|history|Nina 1.2 Anomaly|`Climate_Maester(['nina12a'], 'ncei').history()`|
|NCEI|NCEI|history|Nina 1.2 SST|`Climate_Maester(['nina12'], 'ncei').history()`|
|NCEI|NCEI|history|Nina 3 SST|`Climate_Maester(['nina3'], 'ncei').history()`|
|NCEI|NCEI|history|Nina 3.4 SST|`Climate_Maester(['nina34'], 'ncei').history()`|
|NCEI|NCEI|history|Nina 4 SST|`Climate_Maester(['nina4'], 'ncei').history()`|
|NCEI|NCEI|history|Indian Ocean Dipole|`Climate_Maester(['iod'], 'ncei').history()`|
|PSL|PSL|history|Southern Oscillation Index|`Climate_Maester(['soi'], 'psl').history()`|
|PSL|PSL|history|Oceanic Nino index|`Climate_Maester(['oni'], 'psl').history()`|
|PSL|PSL|history|Trans Nino index|`Climate_Maester(['tni'], 'psl').history()`|
|PSL|PSL|history|Arctic Oscillation|`Climate_Maester(['ao'], 'psl').history()`|
|PSL|PSL|history|Bivariate ENSO from nina3.4 & soi|`Climate_Maester(['censo'], 'psl').history()`|
|PSL|PSL|history|Western Pacific Index|`Climate_Maester(['wp'], 'psl').history()`|
|PSL|PSL|history|AMO smoothed|`Climate_Maester(['amo_sm'], 'psl').history()`|
|PSL/NCEI|PSL/NCEI|history|AMO unsmoothed|`Climate_Maester(['amo'], 'ncei').history()`|
|PSL/NCEI|PSL/NCEI|history|Pacific Decadal Oscillation|`Climate_Maester(['pdo'], 'ncei').history()`|


### Install
```shell
pip install maesters-clim
```

### Usage
```python
from maesters_of_clim import Climate_Maester
from datetime import datetime

# retrive history climate index from nina
c = Climate_Maester(
    indexes=['nina34a', 'pdo', 'soi'],
    source='psl'
)
df = c.history()

# retrive half-year ENSO forecast probability
c = Climate_Maester(
    indexes='enso',
    source='iri'
)
iridf = c.forecast(pred_at=datetime(2022, 10, 1))

c = Climate_Maester(
    indexes='enso',
    source='cpc'
)
cpcdf = c.forecast(pred_at=datetime(2022, 10, 1))

# calculate ENSO event from nina34a/nina3a/soi ...
from maesters_of_clim.analysis import enso_event
df['enso_event'] = enso_event(df, column='nina34a', temp=0.5, months=6)
df[~df['enso_event'].isna()]
```

## TODO

The following support is on the way. 🚀🚀🚀
> 1. Data
- [ ] ERA5 reanalysis from RDA and AWS

> 2. Basic Computation
- [ ] Compiste Analysis


