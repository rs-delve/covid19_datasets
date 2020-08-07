import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils
from age.data.load import ined
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen

_FILE_LIST_URL = 'https://api.covid19india.org/documentation/csv/'
_STANDARD_AGE_GROUPS = [
    '0-9', '10-19', '20-29', '30-39',  '40-49', '50-59', 
    '60-69', '70-79', '80-89', '90+'
]

ISO = 'IND'


def _get_sharded_file_urls():
    with urlopen(_FILE_LIST_URL) as f:
        soup = BeautifulSoup(f, 'html.parser')
    data_file_urls = []
    for a in soup.find_all('a'):
        if re.match(r'.*raw_data(\d){1,}.*', a.attrs['href']):
            data_file_urls.append(a.attrs['href'])
    return data_file_urls

def _get_raw_cases():
    all_data = []
    for file_url in _get_sharded_file_urls():
        df = pd.read_csv(file_url)
        df = df[~df['Age Bracket'].isna()]
        all_data.append(df)

    cases_raw = pd.concat(all_data, axis=0)
    cases_raw['Date Announced'] = pd.to_datetime(cases_raw['Date Announced'], format='%d/%m/%Y')
    return cases_raw


def _process_raw_data(raw_cases, status, field):
    cases_sample = raw_cases[(raw_cases['Current Status'] == 'Hospitalized') & (~raw_cases['Age Bracket'].isna()) & (~raw_cases['Gender'].isna())]
    cases_sample = cases_sample[['Entry_ID', 'Date Announced', 'Age Bracket', 'Gender']].rename(columns={
        'Date Announced': 'Date',
        'Age Bracket': 'Age',
        'Gender': 'Sex',
        'Entry_ID': field
    })

    cases_sample.Age = cases_sample.Age.apply(utils.map_age)
    cases_sample = cases_sample[cases_sample.Age.isin(_STANDARD_AGE_GROUPS)]
    cases_sample.Sex = cases_sample.Sex.replace({'M': 'm', 'F': 'f', 'M ': 'm'})
    cases_sample = cases_sample[cases_sample.Sex.isin(['m', 'f'])]
    cases_sample = cases_sample.groupby(['Date', 'Age', 'Sex']).count().reset_index()

    return cases_sample


class India(base.LoaderBase):
    def __init__(self, reference_data):
        self._raw_data = None
        self._reference_data = reference_data

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_data is None:
            self._raw_data = _get_raw_cases()
        return _process_raw_data(self._raw_data, 'Hospitalized', 'cases_new')

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_data is None:
            self._raw_data = _get_raw_cases()
        return _process_raw_data(self._raw_data, 'Deceased', 'deaths_new')

    def cases(self) -> pd.DataFrame:
        cases = self.raw_cases()
        cases = transformations.smooth_sample(cases)
        cases = transformations.add_both_sexes(cases)
        cases = transformations.rescale(cases, self._reference_data.query(f'ISO == "{ISO}"'), 'cases_new')
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths = transformations.smooth_sample(deaths)
        deaths = transformations.add_both_sexes(deaths)
        deaths = transformations.rescale(deaths, self._reference_data.query(f'ISO == "{ISO}"'), 'deaths_new')
        deaths['ISO'] = ISO
        return deaths
