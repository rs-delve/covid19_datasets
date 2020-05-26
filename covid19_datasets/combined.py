"""Combined dataset for DELVE research"""

import pandas as pd
import logging

from .our_world_in_data import OWIDCovid19, OWIDMedianAges
from .oxford_government_policy import OxfordGovernmentPolicyDataset
from .mask_policies import MaskPolicies
from .world_bank import WorldBankDataBank
from .mobility import Mobility
from .apple import AppleMobility
from .excess_mortality import ExcessMortality

from .weather import Weather
from .constants import ISO_COLUMN_NAME, DATE_COLUMN_NAME


_OXFORD_DROP_COLUMNS = ['ConfirmedCases',	'ConfirmedDeaths']
_OWID_COVID19_DROP_COLUMNS = ['tests_units', 'location']
_OWID_AGE_DROP_COLUMNS = ['Entity', 'Year']
_MASKS_DROP_COLUMNS = ['Country', 'Source']
_WORLD_BANK_DROP_COLUMNS = [
    'country', 'Smoking prevalence, females (% of adults)', 'Smoking prevalence, males (% of adults)', 'Diabetes (% of population ages 20 to 79)']
_WEATHER_DROP_COLUMNS = [
    'weather_precipitation_max',
    'weather_humidity_max',
    'weather_humidity_min',
    'weather_sw_radiation_max',
    'weather_temperature_max',
    'weather_temperature_min',
    'weather_wind_speed_max',
    'weather_wind_speed_min'
]


def _policies_data() -> pd.DataFrame:
    oxford = OxfordGovernmentPolicyDataset()
    return oxford.get_data().drop(_OXFORD_DROP_COLUMNS, axis='columns')


def _mask_data() -> pd.DataFrame:
    masks = MaskPolicies()
    return masks.get_data().drop(_MASKS_DROP_COLUMNS, axis='columns').rename(columns={'Stringency': 'Masks'})


def _cases_data() -> pd.DataFrame:
    owid_covid19 = OWIDCovid19()
    return owid_covid19.get_data().drop(_OWID_COVID19_DROP_COLUMNS, axis='columns')


def _age_data() -> pd.DataFrame:
    owid_ages = OWIDMedianAges()
    return owid_ages.get_data().drop(_OWID_AGE_DROP_COLUMNS, axis='columns')


def _reference_data() -> pd.DataFrame:
    wb = WorldBankDataBank()
    return wb.get_data().drop(_WORLD_BANK_DROP_COLUMNS, axis='columns')


def _mobility_data() -> pd.DataFrame:
    mobility = Mobility()
    return mobility.get_data()


def _transport_mobility_data() -> pd.DataFrame:
    apple_mobility = AppleMobility()
    return apple_mobility.get_country_data()


def _excess_mortality_data() -> pd.DataFrame:
    excess_mortality = ExcessMortality()
    return excess_mortality.get_data()


def _weather_data() -> pd.DataFrame:
    weather = Weather()
    return weather.get_data().drop(_WEATHER_DROP_COLUMNS, axis='columns')


def _create_interventions_data() -> pd.DataFrame:
    interventions_data = (_policies_data()
                          .merge(_mask_data(), on=[ISO_COLUMN_NAME, DATE_COLUMN_NAME], how='left')
                          .set_index([ISO_COLUMN_NAME, DATE_COLUMN_NAME, 'CountryName']))
    interventions_data = interventions_data.groupby(
        level=0).ffill().fillna(0.).reset_index()
    return interventions_data


def _create_data() -> pd.DataFrame:
    interventions_data = _create_interventions_data()
    interventions_cases = interventions_data.merge(
        _cases_data(), on=[ISO_COLUMN_NAME, DATE_COLUMN_NAME], how='left').fillna(0)

    combined = (interventions_cases
                .merge(_mobility_data(), on=[ISO_COLUMN_NAME, DATE_COLUMN_NAME], how='left')
                .merge(_transport_mobility_data(), on=[ISO_COLUMN_NAME, DATE_COLUMN_NAME], how='left')
                .merge(_age_data(), on=ISO_COLUMN_NAME, how='left')
                .merge(_reference_data(), on=ISO_COLUMN_NAME, how='left')
                .merge(_excess_mortality_data(), on=[ISO_COLUMN_NAME, DATE_COLUMN_NAME], how='left')
                .merge(_weather_data(), on=[ISO_COLUMN_NAME, DATE_COLUMN_NAME], how='left')
                .set_index([ISO_COLUMN_NAME, DATE_COLUMN_NAME]))

    return combined


class Combined:
    """
    Standardised dataset from multiple sources for DELVE research.
    """

    _data = None

    def __init__(self, force_load: bool = False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data
        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if Combined._data is None or force_load:
            Combined._data = _create_data()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the dataset as Pandas dataframe
        """
        return Combined._data
