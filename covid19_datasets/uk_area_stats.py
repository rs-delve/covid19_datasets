import pandas as pd
import numpy as np
import datetime
from .constants import DATE_COLUMN_NAME

import logging
_log = logging.getLogger(__name__)


ENGLAND_CASES_PATH = 'https://c19downloads.azureedge.net/downloads/csv/coronavirus-cases_latest.csv'
ENGLAND_DEATHS_PATH = 'https://c19downloads.azureedge.net/downloads/csv/coronavirus-deaths_latest.csv'

WALES_PATH = 'http://www2.nphs.wales.nhs.uk:8080/CommunitySurveillanceDocs.nsf/61c1e930f9121fd080256f2a004937ed/77fdb9a33544aee88025855100300cab/$FILE/Rapid%20COVID-19%20surveillance%20data.xlsx'

SCOTLAND_PATH = 'https://raw.githubusercontent.com/DataScienceScotland/COVID-19-Management-Information/master/COVID19%20-%20Daily%20Management%20Information%20-%20Scottish%20Health%20Boards%20-%20Cumulative%20cases.csv'

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


def _load_england_cases_dataset(area_type):
    _log.info("Loading dataset from " + ENGLAND_CASES_PATH)
    df = pd.read_csv(ENGLAND_CASES_PATH)
    _log.info("Loaded")

    df[DATE_COLUMN_NAME] = pd.to_datetime(df["Specimen date"].astype(str))

    # Convert so that
    # Each row corresponds to an area
    # Each column corresponds to a date
    df['Daily lab-confirmed cases'] = df['Daily lab-confirmed cases'].astype('float')
    df = df[df['Area type'] == area_type]
    df['Country'] = 'England'

    df = df.pivot_table(index=['Country', 'Area name'], columns=DATE_COLUMN_NAME,
                        values='Daily lab-confirmed cases')
    df = _backfill_missing_data(df)

    return df


def _load_wales_datasets():
    _log.info("Loading dataset from " + WALES_PATH)
    xlsx = pd.ExcelFile(WALES_PATH)
    _log.info("Loaded")

    df = pd.read_excel(xlsx, 'Tests by specimen date')
    df['Cases (new)'] = df['Cases (new)'].astype('float')
    df['Testing episodes (new)'] = df['Testing episodes (new)'].astype('float')
    df[DATE_COLUMN_NAME] = pd.to_datetime(df["Specimen date"].astype(str))
    df['Country'] = 'Wales'
    df = df.rename(columns={"Local Authority": "Area name"})

    df_cases = df.pivot_table(index=['Country', 'Area name'], columns=DATE_COLUMN_NAME,
                              values='Cases (new)')
    df_cases = _backfill_missing_data(df_cases)

    df_tests = df.pivot_table(index=['Country', 'Area name'], columns=DATE_COLUMN_NAME,
                              values='Testing episodes (new)')
    df_tests = _backfill_missing_data(df_tests)

    return df_cases, df_tests


def _load_scotland_cases_dataset():
    _log.info("Loading dataset from " + SCOTLAND_PATH)
    df = pd.read_csv(SCOTLAND_PATH, error_bad_lines=False)
    _log.info("Loaded")

    # downloaded file is (dates x areas), and we want the opposite
    df = df.transpose()

    # turn first row into a header
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = pd.to_datetime(new_header.astype(str))
    df.columns.name = None

    df = df.replace('*', 0.0).astype(float)

    # original has cumulative data, and we want new cases per day
    for i in range(len(df.columns) - 1, 1, -1):
        df.iloc[:, i] = df.iloc[:, i] - df.iloc[:, i-1]

    # set multi index by country and area
    df['Country'] = 'Scotland'
    df = df.reset_index().rename(columns={'index': 'Area name'}).set_index(['Country', 'Area name'])

    return df


class UKCovid19Data:
    """
    Provides COVID-19 data for various parts of the UK
    """
    
    england_cases_data = None
    wales_cases_data = None
    wales_tests_data = None
    scotland_cases_data = None
    ENGLAND_UPPER_TIER_AUTHORITY = 'Upper tier local authority'
    ENGLAND_LOWER_TIER_AUTHORITY = 'Lower tier local authority'

    def __init__(self, force_load=False, england_area_type=ENGLAND_UPPER_TIER_AUTHORITY):
        """
        Loads datasets and store them in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        if UKCovid19Data.england_cases_data is None or force_load or UKCovid19Data.england_area_type != england_area_type:
            UKCovid19Data.england_area_type = england_area_type
            UKCovid19Data.england_cases_data = _load_england_cases_dataset(england_area_type)

        if UKCovid19Data.wales_cases_data is None or UKCovid19Data.wales_tests_data is None or force_load:
            UKCovid19Data.wales_cases_data, UKCovid19Data.wales_tests_data = _load_wales_datasets()

        if UKCovid19Data.scotland_cases_data is None or force_load:
            UKCovid19Data.scotland_cases_data = _load_scotland_cases_dataset()

    def get_cases_data(self):
        """
        Returns the dataset as Pandas dataframe

        Format:
        - Row index: Country (England, Wales or Scotland), Area name
        - Columns: Dates
        - Each cell value is a number of new cases registered on that day

        Note: Scotland provides data by NHS Board, not by county
        """
        df = pd.concat([UKCovid19Data.england_cases_data, UKCovid19Data.wales_cases_data, UKCovid19Data.scotland_cases_data])
        # in case they have uneven number of columns
        df = df.fillna(0.0)

        return df

