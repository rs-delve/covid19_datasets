"""Excess mortality dataset."""

import pycountry
import pandas as pd
import numpy as np
import datetime
import logging

from .economist_excess_mortality import EconomistExcessMortality
from .eurostats import EuroStatsExcessMortality
from .hmd import HMDExcessMortality

from .constants import *
from .utils import get_country_iso

_log = logging.getLogger(__name__)

_HMD_COUNTRIES = ['AUT', 'BEL', 'DNK', 'FIN', 'ESP', 'ISL', 'NLD', 'NOR', 'PRT', 'SWE', 'USA']
_EUROSTATS_COUNTRIES = ['ARM', 'BGR', 'CZE', 'EST', 'GEO', 'LVA', 'LIE', 'LTU', 'LUX', 'MNE', 'SRB', 'SVK', 'SVN', 'CHE']
_ECONOMIST_COUNTRIES = [
    'GBR',  # Economist dataset combines England, Wales, Scotland and Northern Ireland unlike HMD and EuroStats
    'ECU',
    'FRA',
    'DEU',
    'ITA'
]

assert len(set(_HMD_COUNTRIES + _EUROSTATS_COUNTRIES + _ECONOMIST_COUNTRIES)) == len(_HMD_COUNTRIES + _EUROSTATS_COUNTRIES + _ECONOMIST_COUNTRIES)


def _generate_excess_mortality() -> pd.DataFrame:
    economist_excess_mortality = EconomistExcessMortality()
    economist_data = economist_excess_mortality.get_country_level_data(daily=True)
    economist_data = economist_data[economist_data[ISO_COLUMN_NAME].isin(_ECONOMIST_COUNTRIES)]

    eurostats_mortality = EuroStatsExcessMortality()
    eurostats_data = eurostats_mortality.get_data(daily=True)
    eurostats_data = eurostats_data.query('SEX == "Total" and AGE == "Total"')
    eurostats_data = eurostats_data[eurostats_data[ISO_COLUMN_NAME].isin(_EUROSTATS_COUNTRIES)]

    hmd_mortality = HMDExcessMortality()
    hmd_data = hmd_mortality.get_data(daily=True)
    hmd_data = hmd_data.query('Sex == "Total"')

    columns = [ISO_COLUMN_NAME, DATE_COLUMN_NAME, 'deaths_excess_daily_avg', 'deaths_excess_weekly']

    excess_mortality = pd.concat([
        economist_data[columns],
        eurostats_data[columns],
        hmd_data[columns]
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
