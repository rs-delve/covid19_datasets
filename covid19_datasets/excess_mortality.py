"""Excess mortality dataset."""

import pycountry
import pandas as pd
import numpy as np
import datetime
import logging

from .economist_excess_mortality import EconomistExcessMortality
from .eurostats import EuroStatsExcessMortality

from .constants import *
from .utils import get_country_iso

_log = logging.getLogger(__name__)

_EUROSTATS_EXCLUDE = ['ESP', 'PRT', 'SWE']
_ECONOMIST_EXCLUDE = ['AUT', 'BEL', 'CHE', 'DNK', 'NOR']


def _generate_excess_mortality() -> pd.DataFrame:
    economist_excess_mortality = EconomistExcessMortality()
    economist_data = economist_excess_mortality.get_country_level_data(
        daily=True)
    economist_data = economist_data[~economist_data[ISO_COLUMN_NAME].isin(
        _ECONOMIST_EXCLUDE)]

    eurostats_mortality = EuroStatsExcessMortality()
    eurostats_data = eurostats_mortality.get_data(daily=True)
    eurostats_data = eurostats_data.query('SEX == "Total" and AGE == "Total"')
    eurostats_data = eurostats_data[~eurostats_data[ISO_COLUMN_NAME].isin(
        _EUROSTATS_EXCLUDE)]

    columns = [ISO_COLUMN_NAME, DATE_COLUMN_NAME,
               'deaths_excess_daily_avg', 'deaths_excess_weekly']

    intersection = set(eurostats_data[ISO_COLUMN_NAME]) & set(
        economist_data[ISO_COLUMN_NAME])
    if intersection:
        raise ValueError(
            'Found duplicated ISOs in Economist and EuroStats excess mortality data: ' + intersection)

    excess_mortality = pd.concat([
        economist_data[columns],
        eurostats_data[columns]
    ], axis=0)
    return excess_mortality

class ExcessMortality():
    """
    Excess mortality using data from EuroStats, the Economist and Human Mortality Database.
    """

    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if ExcessMortality.data is None or force_load:
            ExcessMortality.data = _generate_excess_mortality()

    def get_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return ExcessMortality.data
