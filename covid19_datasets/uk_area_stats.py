import pandas as pd
import numpy as np
from .constants import DATE_COLUMN_NAME

import logging
_log = logging.getLogger(__name__)


ENGLAND_CASES_PATH = 'https://c19downloads.azureedge.net/downloads/csv/coronavirus-cases_latest.csv'
ENGLAND_DEATHS_PATH = 'https://c19downloads.azureedge.net/downloads/csv/coronavirus-deaths_latest.csv'


def _load_dataset(path):
    _log.info("Loading dataset from " + path)
    df = pd.read_csv(path)
    _log.info("Loaded")

    df[DATE_COLUMN_NAME] = pd.to_datetime(df["Specimen date"].astype(str))

    # Convert so that
    # Each row corresponds to an area
    # Each column corresponds to a date
    df['Daily lab-confirmed cases'] = df['Daily lab-confirmed cases'].astype('float')
    df = df.pivot_table(index=['Area name', 'Area type'], columns='DATE',
                        values='Cumulative lab-confirmed cases').sort_values(by=['Area type'])
    df = df.fillna(0.0)

    # Some dates are missing as there were no number reported
    # backfill them with 0
    all_days = pd.date_range(df.columns.min(), df.columns.max(), freq='D')
    missing_days = np.setdiff1d(all_days, df.columns)
    for missing_day in missing_days:
        df[missing_day] = 0.0

    df = df[np.sort(df.columns)]

    return df


class UKCovid19Cases:
    """
    New COVID-19 cases in each UK area

    Format is:
    - Each row corresponds to an area
    - Each column corresponds to a date
    - Each cell contains daily cases count
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
    New COVID-19 deaths in each UK area
    
    Format is:
    - Each row corresponds to an area
    - Each column corresponds to a date
    - Each cell contains daily deaths count
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
