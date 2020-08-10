import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils
from age.data.load import ined
import logging
import datetime
from urllib.request import urlopen
import tabula
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

_log = logging.getLogger(__name__)

_LIST_URL = 'https://covid19.min-saude.pt/relatorio-de-situacao/'
_START_NUM = 8  # Ignore reports numbered below this
_MEASUREMENT1_NUM = 22  # Use measurement set 1 from here onwards
_LAST_CUMULATIVE_DATE = '2020-03-23'

_MEASUREMENT_SETS = [
    # (top left bottom right)
    (6.7*72, 0.6*72, 9.5*72, 3.7*72),
    (7*72, 4.2*72, 10.8*72, 8.2*72)
]

_URL_MAP = {
    'https://covid19.min-saude.pt/wp-content/uploads/2020/03/Relatório-de-Situação-11.pdf': 'https://covid19.min-saude.pt/wp-content/uploads/2020/03/Relato%CC%81rio-de-Situac%CC%A7a%CC%83o-11.pdf',
    'https://covid19.min-saude.pt/wp-content/uploads/2020/03/Relatório-de-Situação-10.pdf': 'https://covid19.min-saude.pt/wp-content/uploads/2020/03/Relato%CC%81rio-de-Situac%CC%A7a%CC%83o-11.pdf',
    'https://covid19.min-saude.pt/wp-content/uploads/2020/03/Relatório-de-Situação-9.pdf': 'https://covid19.min-saude.pt/wp-content/uploads/2020/03/Relato%CC%81rio-de-Situac%CC%A7a%CC%83o-9.pdf',
    'https://covid19.min-saude.pt/wp-content/uploads/2020/03/Relatório-de-Situação-8.pdf': 'https://covid19.min-saude.pt/wp-content/uploads/2020/03/Relato%CC%81rio-de-Situac%CC%A7a%CC%83o-8.pdf'
}

_EXPECTED_AGE_GROUPS = ['00-09 anos', '10-19 anos', '20-29 anos', '30-39 anos', '40-49 anos', '50-59 anos', '60-69 anos', '70-79 anos', '80+']
_INED_URL = 'https://dc-covid.site.ined.fr/en/data/portugal/'

ISO = 'PRT'


def _read_cases_from_pdf(url, measurements):
    url = _URL_MAP.get(url, url)
    with urlopen(url.replace('Ã', 'A%CC%83')) as f:
        df = tabula.read_pdf(f, output_format='dataframe', pages=2, 
                             guess=False, area=measurements, 
                             pandas_options={'dtype': 'str', 'header': None})


    return df[0]

def _read_all_cases():
    with urlopen(_LIST_URL) as f:
        soup = BeautifulSoup(f, 'html.parser')

    cases = {}

    for link in soup.find_all('a'):
        for c in link.children:
            if isinstance(c, NavigableString) and c.startswith('Relatório de Situação nº'):
                num = int(c.replace('Relatório de Situação nº ', '')[:3])
                if num < _START_NUM:
                    _log.info(f'Skipping report number {num} which is before the start')
                    continue

                date = c[c.index('|')+1:]
                if date == ' 29/04/2':
                    date = ' 29/04/2020'

                url = link.attrs['href']
                measurements = _MEASUREMENT_SETS[0] if num < _MEASUREMENT1_NUM else _MEASUREMENT_SETS[1]
                try:
                    df = _read_cases_from_pdf(url, measurements)
                except Exception as e:
                    print(f'Error processing URL {url} with measurements {measurements}')
                    raise e
                cases[date] = df
                _log.info(f'Loaded report {num} for date {date}')

    return cases

def _read_raw_cases(cases):
    processed_dfs = []

    for date, df in cases.items():
        df = df.copy()
        if len(df.columns) != 3:
            _log.warn(f'{date} has {len(df.columns)} columns, skipping!')
            continue
        df.columns=['Age', 'm', 'f']
        df = df[df.Age.isin(_EXPECTED_AGE_GROUPS)]
        if len(df) != len(_EXPECTED_AGE_GROUPS):
            _log.warn(f'{date} DOES NOT HAVE THE EXPECTED NUMBER OF AGE GROUPS')

        df = df.set_index('Age').stack().reset_index().rename(columns={'level_1': 'Sex', 0: 'cases_new'})
        df['Date'] = pd.to_datetime(date.strip(), format='%d/%m/%Y')
        df.Age = df.Age.apply(lambda s: s.replace(' anos', ''))
        if df.cases_new.str.contains('%').any():
            _log.warn(f'Data on {date} is in percentages, skipping!')
            continue
        df.cases_new = df.cases_new.astype(int)
        processed_dfs.append(df)

    return pd.concat(processed_dfs, axis=0)


class Portugal(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            self._raw_cases = _read_raw_cases(_read_all_cases())
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            self._raw_deaths = ined.read_ined_table(_INED_URL, 'min-sau_Data', 'Population on 01/07/2019')
        
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        raw_cases = self.raw_cases()
        cases = transformations.cumulative_to_new(raw_cases)
        cases = transformations.add_both_sexes(cases)
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths['ISO'] = ISO
        return deaths
