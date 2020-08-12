"""Load age and sex disaggregated data for Korea."""

import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from urllib.request import urlopen
from bs4 import BeautifulSoup
from age.data.load import ined
import logging
from typing import Dict

_log = logging.getLogger(__name__)

ISO = 'KOR'

_BASE_URL = 'https://www.cdc.go.kr'
_START_URL = 'https://www.cdc.go.kr/board.es?mid=a30402000000&bid=0030&nPage='
_SEARCH_STRING = 'The updates on COVID-19 in Korea as of '
_CUTOFF_DATE = pd.to_datetime('7 March 2020')  # Age breakdowns availalbe on this date and after.
_INED_URL = 'https://dc-covid.site.ined.fr/en/data/korea/'

_EXPECTED_AGE_GROUPS = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80 and above', '80 or above', 'Above 80']

_CUMULATIVE_CUTOFF_DATE = pd.to_datetime('2020-04-15')  # Before this date, values are cumulative
# Except for these dates
_NON_CUMULATIVE_DATES = [
    '2020-03-31', '2020-04-02', '2020-04-04', '2020-04-06', '2020-04-08', '2020-04-09', 
    '2020-04-10', '2020-04-12', '2020-04-13', '2020-04-14'
]


def _scrape_num_pages() -> int:
    with urlopen(_START_URL + '1') as f:
        soup = BeautifulSoup(f, 'html.parser')

    page_info = soup.find_all("p", {"class": "page_info"})
    num_pages = int(page_info[0].find_all('span', {'class': 'txt_bold'})[1].contents[0])

    return num_pages

def _scrape_report_urls() -> Dict[str, str]:
    num_pages = _scrape_num_pages()
    
    all_report_urls = {}
    for page_i in range(1, num_pages+1):
        url = _START_URL + str(page_i)
        try:
            with urlopen(url) as f:
                soup = BeautifulSoup(f, 'html.parser')  
        except Exception as e:
            _log.error(f'Error Loading URL: {url}: {e}')
            raise e
        hrefs = soup.find_all('a')
        for a in hrefs:
            if 'title' in a.attrs and _SEARCH_STRING in a.attrs['title']:
                key = a.attrs['title'].replace(_SEARCH_STRING, '')
                value = a.attrs['href']
                all_report_urls[key] = value
                _log.info(f'Found {key}: {value}')
    return all_report_urls

def _scrape_cases(report_urls: Dict[str, str]) -> pd.DataFrame:
    all_case_dfs = []
    for date, url in report_urls.items():
        pd_date = pd.to_datetime(date + ' 2020')

        if pd_date < _CUTOFF_DATE:
            _log.info(f'Skipping {pd_date} which is before cuttoff date {_CUTOFF_DATE}')

        matched = None
        try:
            matched = pd.read_html(_BASE_URL + url, match='0-9')
        except:
            pass

        if matched is None:
            _log.warn(f'Skipping {date} due to no matching tables!')
            continue

        if len(matched) > 1:
            _log.info(f'{date} matched {len(matched)} tables')
        case_df = matched[0]

        age_column = 0
        for i, col in enumerate(case_df.columns):
            if '0-9' in case_df[col].values:
                age_column = i

        case_df = case_df[[age_column, age_column + 1]]
        case_df.columns = ['Age', 'cases_new']
        case_df = case_df[case_df.Age.isin(_EXPECTED_AGE_GROUPS)]
        case_df['Date'] = pd_date
        case_df['Sex'] = 'b'
        case_df.Age = case_df.Age.replace(['80 and above', '80 or above', 'Above 80'], '80+')
        if len(case_df.Age.unique()) != 9:
            _log.warn(f'THERE ARE NOT 9 AGE GROUPS ON {date}: {url}')
        all_case_dfs.append(case_df)

    raw_cases = pd.concat(all_case_dfs, axis=0)
    raw_cases.cases_new = raw_cases.cases_new.astype(int)
    return raw_cases


class Korea(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            self._raw_cases = _scrape_cases(_scrape_report_urls())
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            self._raw_deaths = ined.read_ined_table(
                _INED_URL, 'KCDC__by age and sex_Data')
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        raw_cases = self.raw_cases()

        unstacked = raw_cases.set_index(['Date', 'Age', 'Sex']).unstack().unstack()
        cumulative = unstacked.loc[:_CUMULATIVE_CUTOFF_DATE].copy()
        new = unstacked.loc[_CUMULATIVE_CUTOFF_DATE + pd.offsets.Day(1):].copy()

        for i, date in enumerate(cumulative.index):
            if date.strftime('%Y-%m-%d') in _NON_CUMULATIVE_DATES:
                cumulative.iloc[i] = cumulative.iloc[i] + cumulative.iloc[i-1]

        cases = pd.concat([cumulative.resample('d').interpolate().diff(), new], axis=0)
        cases.reindex(pd.date_range(cases.index.min(), cases.index.max(), freq='d')).fillna(0)
        cases = round(cases)
        cases[cases < 0] = 0
        cases = cases.stack().stack().reset_index()
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths['ISO'] = ISO
        return deaths