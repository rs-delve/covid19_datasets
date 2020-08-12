import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils
from age.data.load import ined


_CASES_PATH = 'https://www.data.gouv.fr/fr/datasets/r/57d44bd6-c9fd-424f-9a72-7834454f9e3c'
_INED_PATH = 'https://dc-covid.site.ined.fr/en/data/france/'

_CASES_COLUMN_MAP = {
    'fra': 'France',
    'jour': 'Date',
    'cl_age90': 'Age',
    'pop': 'Reference population',
    'P': 'b',
    'pop_h': 'Population Male',
    'P_h': 'm',
    'pop_f': 'Population Female',
    'P_f': 'f',
}


ISO = 'FRA'


def _age_bucket(age):
    if age == 90:
        return '90+'
    lower = (age // 10) * 10
    return f'{lower}-{age}'


class France(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            raw_cases = pd.read_csv(_CASES_PATH, parse_dates=['jour'], sep=';')
            raw_cases = raw_cases.rename(columns=_CASES_COLUMN_MAP)
            raw_cases = (raw_cases[['Age', 'Date', 'f', 'm', 'b']]
                        .set_index(['Age', 'Date'])
                        .stack()
                        .to_frame()
                        .reset_index()
                        .rename(columns={'level_2': 'Sex', 0: 'cases_new'}))
            raw_cases = raw_cases.query('Age != 0')  # Age bucket 0 is the total
            raw_cases.Age = raw_cases.Age.apply(_age_bucket)
            self._raw_cases = raw_cases
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            raw_deaths = ined.read_ined_table(
                _INED_PATH, 
                sheet_name='SpF_by age and sex_HospitalData')
            self._raw_deaths = raw_deaths
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        cases = self.raw_cases()
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths['ISO'] = ISO
        return deaths
