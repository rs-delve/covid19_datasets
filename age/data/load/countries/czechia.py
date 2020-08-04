import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils


_CASES_PATH = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv'
_DEATHS_PATH = 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv'

_COLUMN_MAPPING = {
    'datum': 'Date',
    'vek': 'Age',
    'pohlavi': 'Sex',
    'kraj_nuts_kod': 'Region_Code'
}

ISO = 'CZE'

def _process_czechia(raw_data, field):
    data = raw_data.rename(columns=_COLUMN_MAPPING)
    data.Age = data.Age.apply(utils.map_age)
    data = data.groupby(['Date', 'Age', 'Sex'], as_index=False)['Region_Code'].count().rename(columns={'Region_Code': field})
    data.Sex = data.Sex.replace({'M': 'm', 'Z': 'f'})
    return data


class Czechia(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            raw_cases = pd.read_csv(_CASES_PATH, parse_dates=['datum'])
            raw_cases = _process_czechia(raw_cases, 'cases_new')
            self._raw_cases = raw_cases
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            raw_deaths = pd.read_csv(_DEATHS_PATH, parse_dates=['datum'])
            raw_deaths = _process_czechia(raw_deaths, 'deaths_new')
            self._raw_deaths = raw_deaths
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        cases = self.raw_cases()
        cases = transformations.add_both_sexes(cases)
        cases = transformations.periodic_to_daily(cases)
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths = transformations.add_both_sexes(deaths)
        deaths = transformations.periodic_to_daily(deaths)
        deaths['ISO'] = ISO
        return deaths
