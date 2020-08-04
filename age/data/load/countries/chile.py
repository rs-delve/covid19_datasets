import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils

_CASES_PATH = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto16/CasosGeneroEtario_std.csv'
_DEATHS_PATH = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario_std.csv'

_CASE_COLUMN_MAPPING = {
    'Grupo de edad': 'Age',
    'Sexo': 'Sex',
    'Fecha': 'Date',
    'Casos confirmados': 'cases_new'
}

_DEATHS_COLUMN_MAPPING = {
    'Grupo de edad': 'Age',
    'fecha': 'Date',
    'Casos confirmados': 'deaths_new'
}

ISO = 'CHL'

class Chile(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            raw_cases = pd.read_csv(_CASES_PATH, parse_dates=['Fecha'])
            raw_cases = raw_cases.rename(columns=_CASE_COLUMN_MAPPING)
            raw_cases.Age = raw_cases.Age.apply(lambda s: s.replace(' años', '').replace(' y más', '+'))
            raw_cases.Sex = raw_cases.Sex.replace({'M': 'm', 'F': 'f'})
            self._raw_cases = raw_cases
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            raw_deaths = pd.read_csv(_DEATHS_PATH, parse_dates=['fecha'])
            raw_deaths = raw_deaths.rename(columns=_DEATHS_COLUMN_MAPPING)
            raw_deaths['Sex'] = 'b'
            self._raw_deaths = raw_deaths
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        cases = self.raw_cases()
        cases = transformations.add_both_sexes(cases)
        cases = transformations.cumulative_to_new(cases)
        cases = transformations.periodic_to_daily(cases)
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths = transformations.cumulative_to_new(deaths)
        deaths['ISO'] = ISO
        return deaths
