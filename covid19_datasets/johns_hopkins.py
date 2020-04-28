from typing import Callable
import pandas as pd
import logging
from .constants import *
_log = logging.getLogger(__name__)


_JH_GLOBAL_CASES_PATH = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
_JH_US_CASES_PATH = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
_JH_GLOBAL_DEATHS_PATH = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
_JH_US_DEATHS_PATH = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
_JH_LOOKUP_PATH = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv'

_LOOKUP_COLUMNS = ['iso3', 'Lat', 'Long_', 'Population']
_RENAME_COLS = {
    'Country/Region': 'Country_Region',
    'Province/State': 'Province_State'    
}

_DROP_GLOBAL_COLUMNS = ['Lat', 'Long']
_DROP_US_COLUMNS = ['iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Combined_Key', 'UID', 'Lat', 'Long_', 'Population']
_KEY_COLUMNS = ['Country_Region', 'Province_State']


def _standardise(ts_df: pd.DataFrame, label: str) -> pd.DataFrame:
  """Convert wide format dataframe into long format."""
  long_df = (ts_df
             .rename(columns=_RENAME_COLS)
             .melt(id_vars=_KEY_COLUMNS, var_name=DATE_COLUMN_NAME, value_name=f'total_{label}'))

  long_df.DATE = pd.to_datetime(long_df.DATE, format='%m/%d/%y')
  long_df = long_df.rename(columns={'iso3': ISO_COLUMN_NAME})

  return long_df 


def _convert_us_data(us_df: pd.DataFrame) -> pd.DataFrame:
  """Convert US data to match global data."""
  return (us_df
         .drop(_DROP_US_COLUMNS, axis='columns', errors='ignore')
         .groupby(_KEY_COLUMNS, as_index=False).sum())


def _load_dataset() -> pd.DataFrame:
    jh_global_cases = pd.read_csv(_JH_GLOBAL_CASES_PATH)
    jh_us_cases = pd.read_csv(_JH_US_CASES_PATH)
    jh_global_deaths = pd.read_csv(_JH_GLOBAL_DEATHS_PATH)
    jh_us_deaths = pd.read_csv(_JH_US_DEATHS_PATH)
    jh_lookup = pd.read_csv(_JH_LOOKUP_PATH)

    jh_lookup = jh_lookup[jh_lookup.Admin2.isna()]

    jh_cases = _standardise(
        jh_global_cases.drop(_DROP_GLOBAL_COLUMNS, axis='columns'), 'cases')
    jh_deaths = _standardise(
        jh_global_deaths.drop(_DROP_GLOBAL_COLUMNS, axis='columns'), 'deaths')

    us_cases = _standardise(_convert_us_data(jh_us_cases), 'cases')
    us_deaths = _standardise(_convert_us_data(jh_us_deaths), 'deaths')
    us_data = us_cases.merge(us_deaths, on=_KEY_COLUMNS + [DATE_COLUMN_NAME])

    jh_data = jh_cases.merge(jh_deaths, on=_KEY_COLUMNS + [DATE_COLUMN_NAME])
    # Drop global US numbers to use state-level from the US dataset instead
    jh_data = jh_data.query('Country_Region != "US"')  
    jh_data = pd.concat([jh_data, us_data], axis=0)
    jh_data = jh_data.merge(jh_lookup[_LOOKUP_COLUMNS + _KEY_COLUMNS], on=_KEY_COLUMNS, how='inner')

    return jh_data


class JohnsHopkins:
    """
    Data from Johns Hopkins: https://coronavirus.jhu.edu/
    Provides cases and death data at provice/state level for many countries.
    """

    _data = None

    def __init__(self, force_load: bool = False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data
        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if JohnsHopkins._data is None or force_load:
            JohnsHopkins._data = _load_dataset()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the dataset as Pandas dataframe
        """
        return JohnsHopkins._data
