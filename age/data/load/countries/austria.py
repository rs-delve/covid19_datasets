"""Load age and sex disaggregated data for Austria."""

import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import coverage

ISO = 'AUT'

def _age_conform(s: str) -> str:
    if s == '85':
        return '85+'
    elif s == '0':
        return '0-4'
    else:
        val = int(s)
        return s + '-' + str(int(s) + 9)

class Austria(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None
        self._coverage_db = coverage.CoverageDB()

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
             self._raw_cases = self._coverage_db.get_data_from_input_db('Austria', 'cases_new')
             self._raw_cases.Age =  self._raw_cases.Age.apply(_age_conform)
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            deaths = self._coverage_db.get_data_from_input_db('Austria', 'deaths_new')
            deaths.Age = deaths.Age.apply(_age_conform)
            self._raw_deaths = deaths
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        raw_cases = self.raw_cases()
        cases = transformations.cumulative_to_new(raw_cases)
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        raw_deaths = self.raw_deaths()
        deaths = transformations.cumulative_to_new(raw_deaths)
        deaths['ISO'] = ISO
        return deaths
