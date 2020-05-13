import pandas as pd
import logging
from .constants import *
_log = logging.getLogger(__name__)

_MASK_POLICY_PATH = 'https://raw.githubusercontent.com/rs-delve/covid19_datasets/master/data/mask_policy_dates.csv'

def _load_dataset() -> pd.DataFrame:
    _log.info(f'Loading dataset from {_MASK_POLICY_PATH}')
    df = pd.read_csv(_MASK_POLICY_PATH)
    df.DATE = pd.to_datetime(df.DATE, format='%d/%m/%Y')
    # There are some duplicates in the underlying CSV, remove them:
    df = df.groupby([ISO_COLUMN_NAME, DATE_COLUMN_NAME]).first().reset_index()
    _log.info('Loaded')
    return df

class MaskPolicies:
    """
    Dates of introductions of mask policies, along with severities. 
    Obtained from the ACAPS Government measures dataset which has been manually suplemented.
    """

    _data = None

    def __init__(self, force_load: bool = False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data
        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if MaskPolicies._data is None or force_load:
            MaskPolicies._data = _load_dataset()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the dataset as Pandas dataframe
        """
        return MaskPolicies._data
