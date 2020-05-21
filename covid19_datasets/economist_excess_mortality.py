import pandas as pd
import numpy as np
import datetime
import logging

from .constants import *
from .utils import get_country_iso

_log = logging.getLogger(__name__)


COUNTRIES = [
    'austria',
    'belgium',
    'britain',
    'denmark',
    'ecuador',
    'france',
    'germany',
    'indonesia',
    'italy',
    'netherlands',
    'norway',
    'portugal',
    'spain',
    'sweden',
    'switzerland',
    'turkey',
    'united_states'
]


COUNTRY_PATH_FORMAT = 'https://raw.githubusercontent.com/TheEconomist/covid-19-excess-deaths-tracker/master/output-data/excess-deaths/{}_excess_deaths.csv'
_COLUMN_NAMES = {
    'total_deaths': 'deaths_total',
    'covid_deaths': 'deaths_covid',
    'expected_deaths': 'deaths_expected',
    'excess_deaths': 'deaths_excess',
    'non_covid_deaths': 'deaths_non_covid',
    'excess_death_daily_avg': 'deaths_excess_daily_avg'
}


def _load_dataset():
    _log.info("Loading The Economist excess mortality dataset")
    all_data = []
    for country in COUNTRIES:
        path = COUNTRY_PATH_FORMAT.format(country)
        try:
            _log.info(f"Loading {country} from " + path)
            country_df = pd.read_csv(path)
        except:
            _log.error(f'ERROR WITH {country}')

        all_data.append(country_df)
    _log.info("Loaded")

    df = pd.concat(all_data, axis=0)
    df["excess_death_daily_avg"] = df["excess_deaths"] / 7.0
    df["start_date"] = pd.to_datetime(df["start_date"].astype(str))
    df["end_date"] = pd.to_datetime(df["end_date"].astype(str))

    df = df.drop(['year', 'week', 'month'], axis='columns')

    df[ISO_COLUMN_NAME] = df['country'].apply(get_country_iso)

    return df


class EconomistExcessMortality():
    """
    Excess mortality data from The Economist
    Mode details:
        https://www.economist.com/graphic-detail/2020/04/16/tracking-covid-19-excess-deaths-across-countries
        https://github.com/TheEconomist/covid-19-excess-deaths-tracker
    """

    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if EconomistExcessMortality.data is None or force_load:
            EconomistExcessMortality.data = _load_dataset()

    def get_raw_data(self):
        """
        Returns the raw dataset as Pandas dataframe
        """
        return EconomistExcessMortality.data

    def get_country_level_data(self, daily=False):
        """
        Returns the dataset with country-level data only in a standarised format.s
        """
        df = EconomistExcessMortality.data

        # filter out region-level rows
        df = df[df['country'] == df['region']]
        # drop region-related columns
        df = df.drop(['region', 'region_code'], axis='columns')

        if daily:
            df[DATE_COLUMN_NAME] = df['start_date']

            def _resample_start_to_end(country_df):
                # add last week's end
                last_row = pd.DataFrame(
                    country_df[-1:].values, columns=country_df.columns)
                last_row[DATE_COLUMN_NAME] = country_df['end_date'].max()
                country_df = country_df.append(last_row)

                country_df = country_df.set_index(
                    DATE_COLUMN_NAME).resample('D').ffill()

                return country_df

            df = df.set_index('country').groupby('country') \
                   .apply(_resample_start_to_end) \
                   .reset_index()

            df['deaths_excess_weekly'] = df.apply(
                lambda row: row['excess_deaths'] if row['end_date'] == row[DATE_COLUMN_NAME] else np.NaN, axis=1)

            df = df.drop(['start_date', 'end_date'], axis='columns')

        df = df.rename(columns=_COLUMN_NAMES)

        return df
