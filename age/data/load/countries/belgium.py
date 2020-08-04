import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations

ISO = 'BEL'

_CASES_PATH = 'https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv'
_DEATHS_PATH = 'https://epistat.sciensano.be/Data/COVID19BE_MORT.csv'

COLUMN_MAP = {
    'DATE': 'Date',
    'AGEGROUP': 'Age',
    'SEX': 'Sex',
    'CASES': 'cases_new',
    'DEATHS': 'deaths_new'
}


def _process_raw_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    processed = (raw_data
                 .groupby(['DATE', 'AGEGROUP', 'SEX'])
                 .sum()
                 .unstack()
                 .unstack()
                 .fillna(0.)
                 .resample('d')
                 .ffill()
                 .stack()
                 .stack()
                 .reset_index()
                 .rename(columns=COLUMN_MAP)
                 .replace({'F': 'f', 'M': 'm'}))
    return processed


class Belgium(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            raw_cases = pd.read_csv(_CASES_PATH, parse_dates=['DATE'])
            raw_cases = _process_raw_data(raw_cases)
            self._raw_cases = raw_cases
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            raw_deaths = pd.read_csv(_DEATHS_PATH, parse_dates=['DATE'])
            raw_deaths = _process_raw_data(raw_deaths)
            self._raw_deaths = raw_deaths
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        cases = self.raw_cases()
        cases = transformations.add_both_sexes(cases)
        cases['ISO'] = 'ISO'
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths = transformations.add_both_sexes(deaths)
        deaths['ISO'] = 'ISO'
        return deaths
