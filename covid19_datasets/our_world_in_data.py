import pandas as pd
import logging
from .constants import *
_log = logging.getLogger(__name__)


_OWID_PATH = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
_AGE_PATH = 'https://github.com/DELVE-covid19/covid19_datasets/raw/master/data/median-age.csv'


def _load_covid19_dataset() -> pd.DataFrame:
    _log.info(f'Loading dataset from {_OWID_PATH}')
    df = pd.read_csv(_OWID_PATH)
    df = df.rename(columns={
        'iso_code': ISO_COLUMN_NAME,
        'date': DATE_COLUMN_NAME
    })
    df.DATE = pd.to_datetime(df.DATE)
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
            OWIDMedianAges._data = _load_covid19_dataset()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the dataset as Pandas dataframe
        """
        return OWIDMedianAges._data
