import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils
from age.data.load import ined
import logging
import datetime
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from io import BytesIO

_ONS_URL = 'https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/weeklyprovisionalfiguresondeathsregisteredinenglandandwales'
_PHE_CASES_PATH = 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/896777/Weekly_COVID19_report_data_current.xlsx'
_EXPECTED_AGE_GROUP_VALUES = ['Persons - UK', 'Males - UK', 'Females - UK', 'Under 1 year', '01-14', '15-44', '45-64', '65-74', '75-84', '85+', '']

ISO = 'GBR'


def _find_excel_url():
    req = Request(_ONS_URL, headers={'User-Agent':'Mozilla/5.0'})
    with urlopen(req) as f:
        soup = BeautifulSoup(f.read())
    xl_url = None
    for a in soup.find_all('a'):
        for child in a.children:
            if isinstance(child, Tag) and child.children and any(c == 'Download Deaths registered weekly in England and Wales, provisional: 2020 in xlsx format' for c in child.children):
                xl_url = a.attrs['href']

    if xl_url is None:
        raise ValueError('Could not find URL of Excel file')

    return xl_url

def _load_raw_deaths():
    xl_url = _find_excel_url()

    req = Request('https://www.ons.gov.uk/' + xl_url, headers={'User-Agent':'Mozilla/5.0'})
    with urlopen(req) as f:
        b = BytesIO(f.read())

    deaths_raw = pd.read_excel(b, sheet_name='UK - Covid-19 - Weekly reg', skiprows=4)

    deaths_raw = deaths_raw.drop('Week ended', axis='columns').rename(columns={'Unnamed: 1': 'Age'})
    deaths_raw = deaths_raw[deaths_raw.Age.isin(_EXPECTED_AGE_GROUP_VALUES)]

    def extract_data(find_text, sex):
        idx = int(np.argwhere(deaths_raw.Age.values == find_text).flatten())
        data = deaths_raw.iloc[idx+1:idx+8]
        data = data.set_index('Age').stack().to_frame().reset_index().rename(columns={0: 'deaths_new', 'level_1': 'Date'})
        data['Sex'] = sex
        return data

    uk_deaths = pd.concat([
        extract_data('Persons - UK', 'b'),
        extract_data('Males - UK', 'm'),
        extract_data('Females - UK', 'f')
    ], axis=0)

    return uk_deaths


class UnitedKingdom(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            self._raw_cases = _read_raw_cases(_read_all_cases())
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            self._raw_deaths = _load_raw_deaths()
        
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        raw_cases = self.raw_cases()
        cases = transformations.cumulative_to_new(raw_cases)
        cases = transformations.add_both_sexes(cases)
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths = transformations.periodic_to_daily(deaths)
        deaths['ISO'] = ISO
        return deaths


