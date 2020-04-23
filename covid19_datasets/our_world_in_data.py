from typing import Callable
import pandas as pd
import logging
from .constants import *
_log = logging.getLogger(__name__)


_OWID_PATH = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
_AGE_PATH = 'https://github.com/DELVE-covid19/covid19_datasets/raw/master/data/median-age.csv'


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
    fill_cols = [ISO_COLUMN_NAME, 'total_cases', 'total_deaths', 'total_cases_per_million', 'total_deaths_per_million', 'total_tests', 'total_tests_per_thousand']
    rows.loc[:, fill_cols] = rows.loc[:, fill_cols].ffill()
    rows = rows.fillna(0)
    return rows.drop(ISO_COLUMN_NAME, axis='columns')


def _load_covid19_dataset() -> pd.DataFrame:
    _log.info(f'Loading dataset from {_OWID_PATH}')
    df = pd.read_csv(_OWID_PATH)
    df = df.rename(columns={
        'iso_code': ISO_COLUMN_NAME,
        'date': DATE_COLUMN_NAME
    })
    df.DATE = pd.to_datetime(df.DATE)
    df = df.groupby(ISO_COLUMN_NAME).apply(_fill_dates).reset_index()
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
        return OWIDCovid19._data


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
