"""Excess mortality dataset."""

import pycountry
import pandas as pd
import numpy as np
import datetime
import logging

from .economist_excess_mortality import EconomistExcessMortality
from .eurostat import EuroStatExcessMortality
from .hmd import HMDExcessMortality

from .constants import *
from .utils import get_country_iso

_log = logging.getLogger(__name__)

_HMD_COUNTRIES = ['AUT', 'BEL', 'DNK', 'FIN', 'ESP', 'ISL', 'NLD', 'NOR', 'PRT', 'SWE', 'USA', 'DEU']
_EUROSTAT_COUNTRIES = ['ARM', 'BGR', 'CZE', 'EST', 'GEO', 'LVA', 'LIE', 'LTU', 'LUX', 'MNE', 'SRB', 'SVK', 'SVN', 'CHE']
_ECONOMIST_COUNTRIES = [
    'GBR',  # Economist dataset combines England, Wales, Scotland and Northern Ireland unlike HMD and EuroStat
    'ECU',
    'FRA',
    'ITA'
]

assert len(set(_HMD_COUNTRIES + _EUROSTAT_COUNTRIES + _ECONOMIST_COUNTRIES)) == len(_HMD_COUNTRIES + _EUROSTAT_COUNTRIES + _ECONOMIST_COUNTRIES)


def _generate_excess_mortality() -> pd.DataFrame:
    economist_excess_mortality = EconomistExcessMortality()
    economist_data = economist_excess_mortality.get_country_level_data(daily=True)
    economist_data = economist_data[economist_data[ISO_COLUMN_NAME].isin(_ECONOMIST_COUNTRIES)]

    eurostat_mortality = EuroStatExcessMortality()
    eurostat_data = eurostat_mortality.get_data(daily=True)
    eurostat_data = eurostat_data.query('SEX == "Total" and AGE == "Total"')
    eurostat_data = eurostat_data[eurostat_data[ISO_COLUMN_NAME].isin(_EUROSTAT_COUNTRIES)]

    hmd_mortality = HMDExcessMortality()
    hmd_data = hmd_mortality.get_data(daily=True)
    hmd_data = hmd_data.query('Sex == "Total"')
    hmd_data = hmd_data[hmd_data[ISO_COLUMN_NAME].isin(_HMD_COUNTRIES)]

    columns = [ISO_COLUMN_NAME, DATE_COLUMN_NAME, 'deaths_excess_daily_avg', 'deaths_excess_weekly']

    excess_mortality = pd.concat([
        economist_data[columns],
        eurostat_data[columns],
        hmd_data[columns]
    ], axis=0)
    return excess_mortality


class ExcessMortality():
    """
    Excess mortality using data from EuroStat, the Economist and Human Mortality Database.
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
