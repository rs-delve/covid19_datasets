"""Load age and sex disaggregated data for Austria."""

import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import coverage

ISO = 'AUT'

class Austria(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None
        self._coverage_db = coverage.CoverageDB()

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            self._raw_cases = self._coverage_db.get_data_from_input_db('Austria', 'cases_new')
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            self._raw_deaths = self._coverage_db.get_data_from_input_db('Austria', 'deaths_new')
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
