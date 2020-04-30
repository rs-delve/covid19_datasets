import pandas as pd
import re
from .constants import *

import logging
_log = logging.getLogger(__name__)

OXFORD_PATH = 'https://oxcgrtportal.azurewebsites.net/api/CSVDownload'


def _load_dataset() -> pd.DataFrame:
    _log.info(f'Loading dataset from {OXFORD_PATH}')
    oxford_df = pd.read_csv(OXFORD_PATH)
    oxford_df[DATE_COLUMN_NAME] = pd.to_datetime(oxford_df.Date.astype(str))
    df = oxford_df[[c for c in oxford_df.columns if 'Notes' not in c and 'IsGeneral' not in c]].drop(['Date', 'StringencyIndex', 'StringencyIndexForDisplay', 'Unnamed: 39'], axis='columns')
    df = df.rename(columns={'CountryCode': ISO_COLUMN_NAME})

    regex = re.compile(r"S(\d)*_")
    df = df.rename(columns={c: regex.sub('', c) for c in df.columns})

    _log.info("Loaded")
    return df

class OxfordGovernmentPolicyDataset:
    """
    Oxford COVID-19 government policy dataset
    """
    
    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if OxfordGovernmentPolicyDataset.data is None or force_load:
            OxfordGovernmentPolicyDataset.data = _load_dataset()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the dataset as Pandas dataframe
        """
        return OxfordGovernmentPolicyDataset.data


    def get_country_data(self, country_or_iso) -> pd.DataFrame:
        """
        Returns the dataset for a country as Pandas dataframe

        :param country_or_iso: Name or ISO code of the country
        """
        return self.data.query(f'CountryName == "{country_or_iso}" or ISO == "{country_or_iso}"')


    def get_country_policy_changes(self, country_or_iso) -> pd.DataFrame:
        """
        Policy changes for a given country

        :param country_or_iso: Name or ISO code of the country

        :returns: Pandas dataframe of policy changes
        """
        country_df = self.get_country_data(country_or_iso)
        country_df = country_df.set_index(DATE_COLUMN_NAME)
        country_df = country_df.drop(['ConfirmedCases', 'ConfirmedDeaths'], axis='columns')

        policy_changes = ((country_df != country_df.shift(1)) & ~country_df.isna()).iloc[1:]
        
        return policy_changes
