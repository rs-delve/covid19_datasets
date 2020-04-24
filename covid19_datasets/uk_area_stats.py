import pandas as pd
from .constants import DATE_COLUMN_NAME

import logging
_log = logging.getLogger(__name__)


ENGLAND_CASES_PATH = 'https://c19downloads.azureedge.net/downloads/csv/coronavirus-cases_latest.csv'
ENGLAND_DEATHS_PATH = 'https://c19downloads.azureedge.net/downloads/csv/coronavirus-deaths_latest.csv'


def _load_dataset(path):
    _log.info("Loading dataset from " + path)
    loaded_df = pd.read_csv(path)
    _log.info("Loaded")

    loaded_df[DATE_COLUMN_NAME] = pd.to_datetime(loaded_df["Specimen date"].astype(str))

    return loaded_df


class UKCovid19Cases:
    """
    New and cumulative COVID-19 cases in each UK area
    """
    
    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if UKCovid19Cases.data is None or force_load:
            UKCovid19Cases.data = _load_dataset(ENGLAND_CASES_PATH)

    def get_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return UKCovid19Cases.data


class UKCovid19Deaths:
    """
    New and cumulative COVID-19 deaths in each UK area
    """
    
    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if UKCovid19Deaths.data is None or force_load:
            UKCovid19Deaths.data = _load_dataset(ENGLAND_DEATHS_PATH)

    def get_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return UKCovid19Deaths.data
