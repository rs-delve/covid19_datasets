import pandas as pd
import re
import matplotlib.pyplot as plt

import logging
_log = logging.getLogger(__name__)

OXFORD_PATH = 'https://ocgptweb.azurewebsites.net/CSVDownload'


def _load_dataset():
    _log.info("Loading dataset from " + OXFORD_PATH)
    oxford_df = pd.read_csv(OXFORD_PATH)
    oxford_df['date'] = pd.to_datetime(oxford_df.Date.astype(str))
    df = oxford_df[[c for c in oxford_df.columns if 'Notes' not in c and 'IsGeneral' not in c]].drop(['Date', 'CountryCode', 'StringencyIndex', 'StringencyIndexForDisplay', 'Unnamed: 39'], axis='columns')
    df = df.set_index(['CountryName', 'date'])
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

    def get_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return OxfordGovernmentPolicyDataset.data

    def get_country_data(self, country):
        """
        Returns the dataset for a country as Pandas dataframe

        :param country: Name of the country
        """
        return self.data.loc[country]


    def get_country_policy_changes(self, country):
        """
        Policy changes for a given country

        :param country: Name of the country
        :returns: Pandas dataframe of policy changes
        """
        country_df = self.get_country_data(country)
        regex = re.compile(r"S(\d)*_")

        country_df = country_df.drop(['ConfirmedCases', 'ConfirmedDeaths'], axis='columns')
        country_df = country_df.rename(columns={c: regex.sub('', c) for c in country_df.columns})

        policy_changes = ((country_df != country_df.shift(1)) & ~country_df.isna()).iloc[1:]
        
        return policy_changes
