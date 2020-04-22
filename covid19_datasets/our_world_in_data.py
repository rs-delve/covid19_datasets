import pandas as pd
import logging
from .constants import *
_log = logging.getLogger(__name__)


_OWID_PATH = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
_COLUMNS = [
    'iso_code',
    'location',
    'date',
    'total_cases',
    'new_cases',
    'total_deaths',
    'new_deaths'
]


def _load_dataset() -> pd.DataFrame:
    _log.info('Loading dataset')
    df = pd.read_csv(_OWID_PATH)
    df = df[_COLUMNS].rename(columns={
        'iso_code': ISO_COLUMN_NAME,
        'date': DATE_COLUMN_NAME
    })
    df.DATE = pd.to_datetime(df.DATE)
    _log.info('Loaded')
    return df


class OurWorldInData:
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
        if OurWorldInData._data is None or force_load:
            OurWorldInData._data = _load_dataset()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the dataset as Pandas dataframe
        """
        return OurWorldInData._data
