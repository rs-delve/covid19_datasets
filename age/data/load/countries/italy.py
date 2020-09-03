import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils
from age.data.load import ined
import tabula

import logging

_log = logging.getLogger(__name__)


_CASE_PDFS = {  # Value is tuple(URL, Page Number, Parameter Set Index)
    '18 August 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_18-agosto-2020.pdf', 19, 0),
    '11 August 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_11-agosto-2020.pdf', 12, 3),
    '4 August 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_4-agosto-2020.pdf', 10, 3),
    '28 July 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_28-luglio-2020.pdf', 8, 0),
    '21 July 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_21-luglio-2020.pdf', 7, 0),
    '14 July 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_14-luglio-2020.pdf', 7, 0),
    '7 July 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_7-luglio-2020.pdf', 6, 0),
    '30 June 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_30-giugno-2020.pdf', 6, 0),
    '23 June 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_23-giugno-2020.pdf', 7, 0),
    '16 June 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_16-giugno-2020.pdf', 6, 0),
    '9 June 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_9-giugno-2020.pdf', 6, 1),  # Measurements are different!! 
    '3 June 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_3-giugno-2020.pdf', 6, 1),
    '26 May 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_26-maggio-2020.pdf', 6, 1),
    '20 May 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_20-maggio-2020.pdf', 7, 1),  
    '14 May 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_14-maggio-2020.pdf', 7, 1),
    '7 May 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_7-maggio-2020.pdf', 8, 1),
    '28 April 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_28-aprile-2020.pdf', 8, 1),
    '23 April 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_23-aprile-2020.pdf', 7, 1),
    '16 April 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_16-aprile-2020.pdf', 7, 1),
    '9 April 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_9-aprile-2020.pdf', 8, 1),
    '2 April 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_2-aprile-2020.pdf', 6, 2),  # Measurements change again here
    '30 March 2020': ('https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_30-marzo-2020.pdf', 6, 2)
}

_INED_PATH = 'https://dc-covid.site.ined.fr/en/data/italy/'

_MEASUREMENT_SETS = [
    # (top left bottom right)
    (2.73*72, 0.35*72, 5.28*72, 5.05*72),  
    (4*72, 0.78*72, 6.44*72, 5.32*72),
    (4.28*72, 0.78*72, 6.59*72, 5.32*72),
    (3.2*72, 0.35*72, 6*72, 5.05*72)
]

_AGE_GROUPS = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '>90']

ISO = 'ITA'

def _load_cases_from_pdfs(skip_dates=[]):
    all_age_dfs = []
    for date, (url, page, param_idx) in _CASE_PDFS.items():
        if pd.to_datetime(date) in skip_dates:
          _log.info(f'Skipping data for date {date}')
          continue

        measurements = _MEASUREMENT_SETS[param_idx]
        df = tabula.read_pdf(
            url, output_format='dataframe', pages=page, guess=False, 
            area=measurements, pandas_options={'dtype': 'str', 'header': None})
        age_df = df[0].iloc[:, [0, 1, -1]]
        age_df.columns = ['Age', 'm', 'f']
        age_df.Age = age_df.Age.replace('≥90', '>90')
        age_df = age_df[age_df.Age.isin(_AGE_GROUPS)]
        for age_grp in _AGE_GROUPS:
            assert age_grp in age_df.Age.values, f'Missing age group: {age_grp} in {url}, page {page}, using measurement set {param_idx}'
        def convert(s):
            return int(str(s).replace('.', ''))

        age_df.m = age_df.m.apply(convert)
        age_df.f = age_df.f.apply(convert)

        age_df['Date'] = pd.to_datetime(date)
        age_df = age_df.set_index(['Date', 'Age']).stack().reset_index().rename(columns={'level_2': 'Sex', 0: 'cases_new'})
        age_df.Age = age_df.Age.replace('>90', '90+')
        all_age_dfs.append(age_df)
    return pd.concat(all_age_dfs, axis=0)


class Italy(base.LoaderBase):
    def __init__(self):
        self._raw_cases = None
        self._raw_deaths = None

    def raw_cases(self, skip_dates=[]) -> pd.DataFrame:
        if self._raw_cases is None:
            self._raw_cases = _load_cases_from_pdfs(skip_dates)
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            raw_deaths = ined.read_ined_table(
                _INED_PATH, 
                sheet_name='Combined_Information')
            self._raw_deaths = raw_deaths
        return self._raw_deaths

    def cases(self, skip_dates=[]) -> pd.DataFrame:
        cases = self.raw_cases(skip_dates)
        cases = transformations.cumulative_to_new(cases)
        cases = transformations.add_both_sexes(cases)
        cases = transformations.periodic_to_daily(cases)
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths['ISO'] = ISO
        return deaths

