"""Calculate excess mortality from weekly EuroStats mortality data."""

import pycountry
import pandas as pd
import numpy as np
import datetime
import logging

from .constants import *
from .utils import get_country_iso

_log = logging.getLogger(__name__)

_PATH = 'https://raw.githubusercontent.com/rs-delve/covid19_datasets/master/data/demo_r_mweek3_1_Data.csv'
_KEY_COLUMNS = ['GEO', 'AGE', 'SEX', 'WEEK']


def _last_day_of_calenderweek(year, week):
    first = datetime.date(year, 1, 1)
    base = 1 if first.isocalendar()[1] == 1 else 8
    return first + datetime.timedelta(days=base - first.isocalendar()[2] + 7 * (week - 1) + 6)


def _load_dataset():
    _log.info("Loading EuroStats data")
    df = pd.read_csv(_PATH)
    df = df.replace(':', np.nan)
    df['YEAR'] = df.TIME.str.slice(stop=4).astype(int)
    df['WEEK'] = df.TIME.str.slice(start=5, stop=8).astype(int)
    df = df.drop('TIME', axis='columns')
    df.loc[:, 'Value'] = df.Value.str.replace(',', '').astype(float)

    _log.info('Computing Excess Mortality')
    baseline = df.query('YEAR < 2020').groupby(_KEY_COLUMNS)[
        'Value'].mean().rename('deaths_expected')
    current = df.query('YEAR == 2020').set_index(_KEY_COLUMNS)['Value']

    excess = pd.concat(
        [baseline, (current - baseline).rename('deaths_excess_weekly')], axis=1)
    excess = excess.reset_index().rename(columns={'GEO': 'country'})

    excess[DATE_COLUMN_NAME] = excess['WEEK'].apply(
        lambda w: _last_day_of_calenderweek(2020, w))
    excess[ISO_COLUMN_NAME] = excess.country.apply(get_country_iso)

    return excess


def _resample(grouped_df):
    # Dates are the end of the week, so we move the min date back to the beginning of that week
    min_date = grouped_df.DATE.min() - pd.offsets.Day(6)
    max_date = grouped_df.DATE.max()
    grouped = grouped_df.set_index('DATE').reindex(
        pd.date_range(min_date, max_date, freq='D'))
    grouped.loc[:, 'deaths_excess_daily_avg'] = grouped.loc[:, 'deaths_excess_daily_avg'].bfill(limit=7)
    return grouped


class EuroStatsExcessMortality():
    """
    Excess mortality computed from EuroStats mortality statstics.
    Data from EuroStats: https://ec.europa.eu/eurostat
    """

    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if EuroStatsExcessMortality.data is None or force_load:
            EuroStatsExcessMortality.data = _load_dataset()

    def get_data(self, daily=False):
        """
        Returns the dataset as Pandas dataframe
        """
        if daily:
            df = EuroStatsExcessMortality.data
            df['deaths_excess_daily_avg'] = df['deaths_excess_weekly'] / 7
            key_columns = ['country', 'AGE', 'SEX', 'ISO']
            daily = (df
                     .groupby(key_columns)
                     .apply(_resample)
                     .drop(['country', 'AGE', 'SEX', 'ISO'], axis='columns')
                     .reset_index()
                     .rename(columns={'level_4': DATE_COLUMN_NAME}))
            return daily
        else:
            return EuroStatsExcessMortality.data
