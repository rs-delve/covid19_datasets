import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils
from age.data.load import ined
import logging
import datetime
from urllib.request import urlopen

_CASES_PATH = 'https://data.rivm.nl/covid-19/COVID-19_casus_landelijk.csv'
_INED_URL = 'https://dc-covid.site.ined.fr/en/data/netherlands/'

_COLUMN_MAP = {
    'Date_statistics': 'Date',
    'Agegroup': 'Age',
}

ISO = 'NLD'

def _load_raw_cases():
    df = pd.read_csv(_CASES_PATH, sep=';')
    df = (df.rename(columns=_COLUMN_MAP)
            .groupby(['Date', 'Age', 'Sex'])
            .Date_file
            .count()
            .reset_index()
            .rename(columns={'Date_file': 'cases_new'}))
    df.Date = pd.to_datetime(df.Date)
    df.Sex = df.Sex.replace({'Female': 'f', 'Male': 'm'})
    df = df[df.Sex != "Unknown"]
    return df

class Netherlands(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            self._raw_cases = _load_raw_cases()
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            self._raw_deaths = ined.read_ined_table(_INED_URL, 'RIVM_Data', num_rows=20)
        
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        raw_cases = self.raw_cases()
        cases = transformations.ensure_contiguous(raw_cases)
        cases = transformations.add_both_sexes(cases)
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths['ISO'] = ISO
        return deaths
