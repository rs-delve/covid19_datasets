import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils

_CASES_SAMPLE_PATH = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/cases.csv'
_DEATHS_SAMPLE_PATH = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/mortality.csv'

_AGE_MAPPING = {
    '50': '50-59',
    '61': '60-69',
    '65-79': '70-79',
    '<1': '0-9',
    '<10': '0-9',
    '<18': '10-19',
    '<19': '10-19',
    '<20': '10-19',
    '>90': '90+',
    '100-109': '90+',
    '90-99': '90+',
    '>70': '70-79'
}

_EXPECTED_AGE_GROUPS = ['0-9', '10-19', '20-29', '30-39',
                        '40-49', '50-59', '60-69', '70-79', '80-89', '90+']


def _process_canada_raw(raw_data, field, date_field, count_field):
    raw_data[date_field] = pd.to_datetime(
        raw_data[date_field], format='%d-%m-%Y')

    # Rename age buckets that are subsets of the standard ones
    raw_data.age = raw_data.age.replace(_AGE_MAPPING)
    # Map any specific ages to the respective bucket:
    raw_data.age = raw_data.age.apply(utils.map_age)
    # Remove any remaining unexpected age groups
    raw_data = raw_data[raw_data.age.isin(_EXPECTED_AGE_GROUPS)]

    data = raw_data.query('age != "Not Reported" and sex != "Not Reported"').groupby([date_field, 'age', 'sex'])[count_field].count().reset_index().rename(columns={
        date_field: 'Date',
        'age': 'Age',
        'sex': 'Sex',
        count_field: field
    }).replace({'Male': 'm', 'Female': 'f'})

    return data


class Canada(base.LoaderBase):
  def __init__(self, reference_data):
    self._raw_cases = None
    self._raw_deaths = None
    self._reference_data = reference_data

  def raw_cases(self) -> pd.DataFrame:
    if self._raw_cases is None:
      raw_cases = pd.read_csv(_CASES_SAMPLE_PATH)
      raw_cases = _process_canada_raw(raw_cases, 'cases_new', 'date_report', 'case_id')
      self._raw_cases = raw_cases
    return self._raw_cases

  def raw_deaths(self) -> pd.DataFrame:
    if self._raw_deaths is None:
      raw_deaths = pd.read_csv(_DEATHS_SAMPLE_PATH)
      raw_deaths = _process_canada_raw(raw_deaths, 'deaths_new', 'date_death_report', 'death_id')
      self._raw_deaths = raw_deaths
    return self._raw_deaths

  def cases(self) -> pd.DataFrame:
    cases = self.raw_cases()
    cases = transformations.ensure_contiguous(cases)
    cases = transformations.add_both_sexes(cases)
    cases = transformations.smooth_sample(cases, rolling_window=5)
    cases = transformations.rescale(cases, self._reference_data.query('ISO == "CAN"'), 'cases_new')
    return cases

  def deaths(self) -> pd.DataFrame:
    deaths = self.raw_deaths()
    deaths = transformations.ensure_contiguous(deaths)
    deaths = transformations.add_both_sexes(deaths)
    deaths = transformations.smooth_sample(deaths, rolling_window=5)
    deaths = transformations.rescale(deaths, self._reference_data.query('ISO == "CAN"'), 'deaths_new')
    return deaths
