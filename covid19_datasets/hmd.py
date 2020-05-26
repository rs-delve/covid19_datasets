"""
Compute excess mortality from the Human Mortality Database
https://www.mortality.org/
"""

import pandas as pd
import logging
from .constants import *
from .utils import last_day_of_calenderweek

_log = logging.getLogger(__name__)

_PATH = 'https://www.mortality.org/Public/STMF/Outputs/stmf.csv'
COLUMN_NAMES = {
    'D0_14': 'deaths_excess_age_0_to_14',
    'D15_64': 'deaths_excess_age_15_to_64',
    'D65_74': 'deaths_excess_age_65_to_74',
    'D75_84': 'deaths_excess_age_75_to_84',
    'D85p': 'deaths_excess_age_85_plus',
    'DTotal': 'deaths_excess_total'
}


def _load_dataset():
    df = pd.read_csv(_PATH, skiprows=2)
    df = df.drop([
        'R0_14',	
        'R15_64',	
        'R65_74',	
        'R75_84',	
        'R85p',	
        'RTotal',	
        'Split',	
        'SplitSex',	
        'Forecast'], axis='columns')
    df = df.rename(columns={'CountryCode': ISO_COLUMN_NAME})
    return df


class HMDExcessMortality:
    """
    Excess mortality using data from the Human Mortality Database.
    """

    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if HMDExcessMortality.data is None or force_load:
            HMDExcessMortality.data = _load_dataset()

    def get_raw_data(self) -> pd.DataFrame:
        """
        Returns the raw dataset as Pandas dataframe
        """
        return HMDExcessMortality.data

    def get_data(self, daily=False) -> pd.DataFrame:
        """
        Returns the compute excess mortality dataset as Pandas dataframe.
        """
        df = self.get_raw_data()
        key_cols = [ISO_COLUMN_NAME, 'Sex', 'Week']
        baseline = (df.query('Year < 2020 and Year >= 2015')
                    .groupby(key_cols)
                    .mean()
                    .drop(['Year'], axis='columns'))
        current = (df.query('Year == 2020')
                   .drop(['Year'], axis='columns')
                   .set_index(key_cols))

        excess = (current - baseline).dropna(how='all').reset_index()
        excess[DATE_COLUMN_NAME] = excess['Week'].apply(lambda w: last_day_of_calenderweek(2020, w))
        excess['Sex'] = excess['Sex'].replace({'b': 'Total', 'm': 'Male', 'f': 'Female'})   
        return excess.rename(columns=COLUMN_NAMES)
