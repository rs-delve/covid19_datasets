from typing import Callable
import pandas as pd
import numpy as np
import logging
from .constants import *
_log = logging.getLogger(__name__)


_OWID_PATH = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
_AGE_PATH = 'https://github.com/rs-delve/covid19_datasets/raw/master/data/median-age.csv'


COLUMN_NAMES = {
    'total_cases': 'cases_total',
    'new_cases': 'cases_new',
    'total_deaths': 'deaths_total',
    'new_deaths': 'deaths_new',
    'total_cases_per_million': 'cases_total_per_million',
    'new_cases_per_million': 'cases_new_per_million',
    'total_deaths_per_million': 'deaths_total_per_million',
    'new_deaths_per_million': 'deaths_new_per_million',
    'total_tests': 'tests_total',
    'new_tests': 'tests_new',
    'total_tests_per_thousand': 'tests_total_per_thousand',
    'new_tests_per_thousand': 'tests_new_per_thousand',
    'new_tests_smoothed': 'tests_new_smoothed',
    'new_tests_smoothed_per_thousand': 'tests_new_smoothed_per_thousand',
    'days_since_first_case': 'cases_days_since_first',
    'days_since_first_death': 'deaths_days_since_first',
    'population': 'stats_population',
    'population_density': 'stats_population_density',
    'median_age': 'stats_median_age',
    'gdp_per_capita': 'stats_gdp_per_capita'
}


_FILL_COLUMNS = [  # These are static reference data, so we can forward and backward fill
    ISO_COLUMN_NAME,
    'population',
    'population_density',
    'median_age',
    'gdp_per_capita'
]

_FFILL_GAPS_COLUMNS = [  # Forward fill gaps created by "holes" in dates
    'total_cases', 
    'total_deaths', 
    'total_cases_per_million', 
    'total_deaths_per_million', 
    'total_tests', 
    'total_tests_per_thousand', 
    'location'
]

_ZERO_FILL_GAPS_COLUMNS = [  # Zero fill gaps created by "holes" in dates
    'new_cases',
    'new_deaths',
    'new_cases_per_million',
    'new_deaths_per_million',
    'new_tests',
    'new_tests_per_thousand'
]


def _fill_gaps(series, ffill=True):
  series = series.copy()
  non_nans = series[~series.apply(np.isnan)]
  start, end = non_nans.index[0], non_nans.index[-1]
  if ffill:
    series.ix[start:end] = series.ix[start:end].fillna(method='ffill')
  else:
    series.ix[start:end] = series.ix[start:end].fillna(0.)
  return series


def _compute_anchor(col: str) -> Callable[[pd.DataFrame], pd.Timestamp]:
    def _apply(rows: pd.DataFrame) -> pd.Timestamp:
        anchor = rows.query(f'{col} > 0')
        if len(anchor) > 0:
            anchor = anchor.iloc[0].DATE 
        else:
            anchor = rows.DATE.max()
        return anchor
    return _apply


def _add_days_since(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate number of days since first case and first death."""
    first_cases = df.groupby('ISO').apply(_compute_anchor('total_cases')).reset_index().rename(columns={0: 'first_case'})
    first_deaths = df.groupby('ISO').apply(_compute_anchor('total_deaths')).reset_index().rename(columns={0: 'first_death'})
    df = df.merge(first_cases, on='ISO').merge(first_deaths, on='ISO')
    df['days_since_first_case'] = (df.DATE - df.first_case).dt.days
    df.loc[df.days_since_first_case < 0, 'days_since_first_case'] = 0
    df['days_since_first_death'] = (df.DATE - df.first_death).dt.days
    df.loc[df.days_since_first_death < 0, 'days_since_first_death'] = 0
    df = df.drop(['first_case', 'first_death'], axis='columns')
    return df


def _fill_dates(rows):
    """Ensure that dates are contiguous."""
    rows = rows.set_index(DATE_COLUMN_NAME)
    rows = rows.reindex(pd.date_range(rows.index.min(), rows.index.max(), freq='D'))
    # Forward fill certain columns
    
    rows.loc[:, _FILL_COLUMNS] = rows.loc[:, _FILL_COLUMNS].ffill().bfill()
    for col in _FFILL_GAPS_COLUMNS:
        rows.loc[:, col] = _fill_gaps(rows.loc[:, col], ffill=True)
    for col in _ZERO_FILL_GAPS_COLUMNS:
        rows.loc[:, col] = _fill_gaps(rows.loc[:, col], ffill=False)
    
    return rows.drop(ISO_COLUMN_NAME, axis='columns')


def _load_covid19_raw() -> pd.DataFrame:
    df = pd.read_csv(_OWID_PATH)
    df = df.rename(columns={
        'iso_code': ISO_COLUMN_NAME,
        'date': DATE_COLUMN_NAME
    })
    df.DATE = pd.to_datetime(df.DATE)
    return df


def _load_covid19_dataset() -> pd.DataFrame:
    _log.info(f'Loading dataset from {_OWID_PATH}')
    df = _load_covid19_raw()
    df = df.groupby(ISO_COLUMN_NAME).apply(_fill_dates).reset_index().rename(columns={'level_1': DATE_COLUMN_NAME})
    df = _add_days_since(df)
    _log.info('Loaded')
    return df


def _load_age_dataset() -> pd.DataFrame:
    _log.info(f'Loading dataset from {_AGE_PATH}')
    df = pd.read_csv(_AGE_PATH)
    df = df.rename(columns={
        'Code': ISO_COLUMN_NAME,
        'UN Population Division (Median Age) (2017) (years)': 'median_age'
    })
    # 2015 is the last year of confirmed historical data, after which they use projections
    df = df.query('Year == 2015').dropna(how='any')
    return df


class OWIDCovid19:
    """
    Data from Our World in Data: https://ourworldindata.org/coronavirus
    """

    _data = None

    def __init__(self, force_load: bool = False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data
        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if OWIDCovid19._data is None or force_load:
            OWIDCovid19._data = _load_covid19_dataset()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the dataset as Pandas dataframe
        """
        return OWIDCovid19._data.rename(columns=COLUMN_NAMES)


class OWIDMedianAges:
    """
    Median age by country data from the UN via Our World in Data https://ourworldindata.org/age-structure
    """

    _data = None

    def __init__(self, force_load: bool = False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data
        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if OWIDMedianAges._data is None or force_load:
            OWIDMedianAges._data = _load_age_dataset()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the dataset as Pandas dataframe
        """
        return OWIDMedianAges._data
