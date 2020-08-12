import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils
import json
from urllib.request import urlopen

_JSON_URL = 'https://services7.arcgis.com/nuPvVz1HGGfa0Eh7/arcgis/rest/services/korona_tapauksia_jakauma/FeatureServer/0/query?f=json&where=1%3D1&outFields=OBJECTID,alue,date,tapauksia,miehia,naisia,Ika_0_9,ika_10_19,ika_20_29,ika_30_39,ika_40_49,ika_50_59,ika_60_69,ika_70_79,ika_80_,koodi&returnGeometry=false'
_CUTOFF_DATE = '2020-03-25'

def _load_raw_cases():
    with urlopen(_JSON_URL) as response:
        data = json.load(response)

    df = pd.DataFrame([f['attributes'] for f in data['features']])
    df.columns=['object_id', 'area', 'Date', 'Cases', 'm', 'f', 'age_0-9', 'age_10-19', 'age_20-29', 'age_30-39', 'age_40-49', 'age_50-59', 'age_60-69', 'age_70-79', 'age_80+', 'code']
    df = df[df.Date.notna()]
    df.Date = pd.to_datetime(df.Date, unit='ms')
    df.Date = df.Date.dt.normalize()

    df['m_ratio'] = df['m'] / df['Cases']
    df['f_ratio'] = df['f'] / df['Cases']
    age_cols = [c for c in df.columns if c.startswith('age')]
    df = df.set_index('Date')
    male = round(df.loc[:, age_cols].multiply(df['m_ratio'], axis=0))
    female = round(df.loc[:, age_cols].multiply(df['f_ratio'], axis=0))

    male['Sex'] = 'm'
    female['Sex'] = 'f'

    cases = pd.concat([male, female], axis=0).reset_index()
    cases = cases.melt(id_vars=['Date', 'Sex'], var_name='Age', value_name='cases_new')
    cases.Age = cases.Age.str.replace('age_', '')
    return cases

ISO = 'FIN' 

class Finland(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            self._raw_cases = _load_raw_cases()
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        return None

    def cases(self) -> pd.DataFrame:
        cases = self.raw_cases()
        cases = transformations.ensure_contiguous(cases)
        cases = transformations.cumulative_to_new(cases)
        cases = transformations.add_both_sexes(cases)
        cases = cases.query('Date > "2020-03-25"')
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        return None
