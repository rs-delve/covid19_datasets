import pandas as pd
import numpy as np
from .constants import DATE_COLUMN_NAME

import logging
_log = logging.getLogger(__name__)


ENGLAND_CASES_PATH = 'https://c19downloads.azureedge.net/downloads/csv/coronavirus-cases_latest.csv'
ENGLAND_DEATHS_PATH = 'https://c19downloads.azureedge.net/downloads/csv/coronavirus-deaths_latest.csv'

WALES_PATH = 'http://www2.nphs.wales.nhs.uk:8080/CommunitySurveillanceDocs.nsf/61c1e930f9121fd080256f2a004937ed/77fdb9a33544aee88025855100300cab/$FILE/Rapid%20COVID-19%20surveillance%20data.xlsx'


def _backfill_missing_data(df):
    """
    Datasets might have some dates missing if there were no cases reported on these dates
    Backfill them with 0
    """
    # if there are NaNs, replace them with 0
    df = df.fillna(0.0)

    # Some dates are missing as there were no numbers reported
    # backfill them with 0
    all_days = pd.date_range(df.columns.min(), df.columns.max(), freq='D')
    missing_days = np.setdiff1d(all_days, df.columns)
    for missing_day in missing_days:
        df[missing_day] = 0.0

    df = df[np.sort(df.columns)]

    return df


def _load_england_cases_dataset():
    _log.info("Loading dataset from " + ENGLAND_CASES_PATH)
    df = pd.read_csv(ENGLAND_CASES_PATH)
    _log.info("Loaded")

    df[DATE_COLUMN_NAME] = pd.to_datetime(df["Specimen date"].astype(str))

    # Convert so that
    # Each row corresponds to an area
    # Each column corresponds to a date
    df['Daily lab-confirmed cases'] = df['Daily lab-confirmed cases'].astype('float')
    df = df[df['Area type'] != 'Region']
    df['Country'] = 'England'

    df = df.pivot_table(index=['Country', 'Area name'], columns=DATE_COLUMN_NAME,
                        values='Cumulative lab-confirmed cases')
    df = _backfill_missing_data(df)

    return df


def _load_wales_datasets():
    _log.info("Loading dataset from " + WALES_PATH)
    xlsx = pd.ExcelFile(WALES_PATH)
    _log.info("Loaded")

    df_cases_tests = pd.read_excel(xlsx, 'Tests by specimen date')
    df['Cases (new)'] = df['Cases (new)'].astype('float')
    df['Testing episodes (new)'] = df['Testing episodes (new)'].astype('float')
    df[DATE_COLUMN_NAME] = pd.to_datetime(df["Specimen date"].astype(str))
    df['Country'] = 'Wales'
    df = df.rename(columns={"Local Authority": "Area name"})

    df_cases = df.pivot_table(index=['Country', 'Area name'], columns=DATE_COLUMN_NAME,
                              values='Cases (new)')
    df_cases = _backfill_missing_data(df_cases)
    df_cases.loc["Wales", "Wales"] = df_cases.sum()

    df_tests = df.pivot_table(index=['Country', 'Area name'], columns=DATE_COLUMN_NAME,
                              values='Testing episodes (new)')
    df_tests = _backfill_missing_data(df_tests)
    df_tests.loc["Wales", "Wales"] = df_tests.sum()

    return df_cases, df_tests


class UKCovid19Data:
    """
    Provides COVID-19 data for various parts of the UK
    """
    
    england_cases_data = None
    wales_cases_data = None
    wales_tests_data = None

    def __init__(self, force_load=False):
        """
        Loads datasets and store them in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        if UKCovid19Data.england_cases_data is None or force_load:
            UKCovid19Data.england_cases_data = _load_england_cases_dataset()

        if UKCovid19Data.wales_cases_data is None or UKCovid19Data.wales_tests_data is None or force_load:
            UKCovid19Data.wales_cases_data, UKCovid19Data.wales_tests_data = _load_wales_datasets()

    def get_england_wales_cases_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return pd.concat([UKCovid19Data.england_cases_data, UKCovid19Data.wales_cases_data])
