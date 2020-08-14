import pandas as pd
import numpy as np
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils
import logging
import datetime
from urllib.request import urlopen, Request
from io import BytesIO


_DEATHS_URL = 'https://data.cdc.gov/api/views/vsak-wrfu/rows.csv?accessType=DOWNLOAD'
_CASES_URL = 'https://www.cdc.gov/coronavirus/2019-ncov/covid-data/covidview/07242020/csv/public-health-lab.csv'

ISO = 'USA'

def _load_raw_deaths():
    deaths_raw = pd.read_csv(_DEATHS_URL)
    deaths = deaths_raw[['Week ending Date', 'Sex', 'Age Group', 'COVID-19 Deaths']].rename(columns={
        'Week ending Date': 'Date',
        'Age Group': 'Age',
        'COVID-19 Deaths': 'deaths_new'
    })
    deaths.Date = pd.to_datetime(deaths.Date, format=r'%m/%d/%Y')
    deaths.Sex = deaths.Sex.replace({'Female': 'f', 'Male': 'm', 'All Sex': 'b'})
    deaths.Age = deaths.Age.apply(lambda a: a.replace(' years', ''))
    deaths.Age = deaths.Age.replace({
        '85 and over': '85+',
        'Under 1 year': '0-1'
    })
    return deaths

def _load_raw_cases():
    cases_raw = pd.read_csv(_CASES_URL, skiprows=6, header=[0, 1])
    cases_raw = cases_raw.drop([('Unnamed: 20_level_0', 'Unnamed: 20_level_1'), ('Unnamed: 21_level_0', 'Unnamed: 21_level_1')], axis='columns')

    updated_columns = ['Week', 'Num Labs']
    for i in range(2, len(cases_raw.columns), 3):
        level0 = cases_raw.columns[i][0]
        updated_columns.append(level0 + '_tested')
        updated_columns.append(level0)
        updated_columns.append(level0 + '_pct')

    cases_raw.columns = updated_columns

    cases_raw = cases_raw.drop([c for c in cases_raw.columns if '_tested' in c or '_pct' in c], axis='columns')
    cases_raw = cases_raw.drop(['Num Labs', 'Total  (incl. age unknown)'], axis='columns')
    cases_raw = cases_raw.iloc[:-1]
    cases_raw = cases_raw[cases_raw.Week.str.match(r'\d{5}').fillna(False)]

    for col in cases_raw.columns:
        if col == "Week":
            continue
        cases_raw.loc[:, col] = cases_raw.loc[:, col].str.replace(',', '').astype(float)

    us_cases = cases_raw.groupby('Week', as_index=False).sum()
    us_cases.Week = us_cases.Week.astype(str).apply(lambda w: w[-2:]).astype(int)
    us_cases['Date'] = us_cases.Week.apply(lambda w: utils.last_day_of_calenderweek(2020, w))
    us_cases = us_cases.drop('Week', axis='columns').set_index('Date')
    us_cases = us_cases.stack().reset_index().rename(columns={'level_1': 'Age', 0: 'cases_new'})
    us_cases['Sex'] = 'b'
    us_cases['Age'] = us_cases['Age'].apply(lambda a: a.replace(' years', ''))

    return us_cases


class USA(base.LoaderBase):
    def __init__(self, reference_data):
        self._raw_cases = None
        self._raw_deaths = None
        self._reference_data = reference_data

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_cases is None:
            self._raw_cases = _load_raw_cases()
        return self._raw_cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_deaths is None:
            self._raw_deaths = _load_raw_deaths()
        
        return self._raw_deaths

    def cases(self) -> pd.DataFrame:
        raw_cases = self.raw_cases()
        cases = transformations.periodic_to_daily(raw_cases)
        cases = transformations.rescale(cases, self._reference_data.query(f'ISO == "{ISO}"'), 'cases_new')
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths = transformations.periodic_to_daily(deaths)
        deaths['ISO'] = ISO
        return deaths
