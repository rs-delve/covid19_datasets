import pandas as pd
import logging
import csv
from calendar import monthrange

from .constants import *
from .utils import get_country_iso

_log = logging.getLogger(__name__)

_DATA_PATH = 'https://raw.githubusercontent.com/rs-delve/covid19_datasets/master/data/un_country_deaths_by_month.csv'

months = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}


def _get_daily_average(row):
    _, days_count = monthrange(row['Year'], months[row['Month']])
    return row['Value'] / days_count

def _load_dataset() -> pd.DataFrame:
    _log.info(f'Loading dataset from {_DATA_PATH}')
    df = pd.read_csv(_DATA_PATH, quotechar='"')

    # drop unused columns
    df = df.drop(['Record Type', 'Reliability', 'Source Year', 'Value Footnotes'], axis='columns')
    # drop unused rows
    df = df[df['Month'] != 'Total']
    df = df[df['Area'] == 'Total']
    # Drop rows that contain invalid months values (Unknown, ranges)
    df = df[df['Month'].map(lambda m: m in months)]

    # convert to numeric types where appropriate
    df['Year'] = pd.to_numeric(df['Year'])
    df['Value'] = pd.to_numeric(df['Value'])
    
    df[ISO_COLUMN_NAME] = df['Country or Area'].apply(get_country_iso)
    # Drop rows that don't represent valid countries (e.g. territories)
    df = df[pd.notnull(df[ISO_COLUMN_NAME])]

    df['Daily Average'] = df.apply(_get_daily_average, axis='columns')

    _log.info('Loaded')
    return df


class UNDeathsByCountry:
    """
    Deaths per country per month. 
    Obtained from UN Data: http://data.un.org/Data.aspx?d=POP&f=tableCode%3A65
    """

    _data = None

    def __init__(self, force_load: bool = False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data
        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if UNDeathsByCountry._data is None or force_load:
            UNDeathsByCountry._data = _load_dataset()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the dataset as Pandas dataframe
        """
        return UNDeathsByCountry._data
