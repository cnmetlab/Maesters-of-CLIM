# Maesters-of-Clim

![](./static/maesters_of_clim.jpg)

Maesters-of-Clim tempt to help retriving climate data (climate index, reanalysis) from the main-stream climate insitution (like IRI, PSL, NCEI, RDA). 

### Install
```shell
pip install maesters_of_clim==0.0.1
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
```


