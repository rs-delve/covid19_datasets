"""Load age and sex disaggregated data for Brazil."""

import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import coverage


ISO = 'BRA'

class Brazil(base.LoaderBase):
    def __init__(self, reference_data):
        self._raw_deaths = None
        self._coverage_db = coverage.CoverageDB()
        self._reference_data = reference_data

    def raw_cases(self) -> pd.DataFrame:
        return None

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            self._raw_deaths = self._coverage_db.get_data_from_input_db('Brazil', 'deaths_new', region='All')
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        return None

    def deaths(self) -> pd.DataFrame:
        brazil_deaths = self.raw_deaths()
        ref_data = self._reference_data.query('ISO == "BRA"')
        brazil_deaths = transformations.rescale(brazil_deaths, ref_data, 'deaths_new')
        brazil_deaths['ISO'] = ISO
        return brazil_deaths