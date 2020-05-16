import pandas as pd
import numpy as np
import datetime
from .constants import DATE_COLUMN_NAME

import logging
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

    return pd.concat(all_data, axis=0)


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

    def get_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return EconomistExcessMortality.data
    
    def get_country_level_data(self):
        """
        Returns the dataset with country-level data only
        """
        df = EconomistExcessMortality.data

        # filter out region-level rows
        df = df[df['country'] == df['region']]
        # drop region-related columns
        df = df.drop(['region', 'region_code'], axis='columns')

        return df
