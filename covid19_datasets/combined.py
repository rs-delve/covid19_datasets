"""Combined dataset for DELVE research"""

import pandas as pd
import pycountry
import logging

from .our_world_in_data import OWIDCovid19, OWIDMedianAges
from .oxford_government_policy import OxfordGovernmentPolicyDataset
from .mask_policies import MaskPolicies
from .world_bank import WorldBankDataBank
from .mobility import Mobility
from .apple import AppleMobility
from .excess_mortality import ExcessMortality
from .utils import country_name_from_iso

from .weather import Weather
from .constants import ISO_COLUMN_NAME, DATE_COLUMN_NAME


_POLICIES_COLUMNS = [
    'npi_school_closing', 
    'npi_workplace_closing',
    'npi_cancel_public_events', 
    'npi_gatherings_restrictions',
    'npi_close_public_transport', 
    'npi_stay_at_home',
    'npi_internal_movement_restrictions',
    'npi_international_travel_controls', 
    'npi_income_support',
    'npi_debt_relief', 
    'npi_fiscal_measures', 
    'npi_international_support',
    'npi_public_information', 
    'npi_testing_policy', 
    'npi_contact_tracing',
    'npi_healthcare_investment', 
    'npi_vaccine_investment', 
    'npi_stringency_index']


_MASKS_COLUMNS = [
    'npi_masks'
]


_CASES_COLUMNS = [
    'cases_total', 
    'cases_new', 
    'deaths_total',
    'deaths_new', 
    'cases_total_per_million', 
    'cases_new_per_million',
    'deaths_total_per_million', 
    'deaths_new_per_million', 
    'tests_total',
    'tests_new', 
    'tests_total_per_thousand', 
    'tests_new_per_thousand',
    'tests_new_smoothed', 
    'tests_new_smoothed_per_thousand', 
    'stats_population', 
    'stats_population_density',
    'stats_median_age', 
    'stats_gdp_per_capita', 
    'cases_days_since_first', 
    'deaths_days_since_first'
]


_REFERENCE_COLUMNS = [
    'stats_hospital_beds_per_1000', 
    'stats_smoking',
    'stats_population_urban', 
    'stats_population_school_age'
]

_WEATHER_COLUMNS = [
    'weather_precipitation_mean',
    'weather_humidity_mean', 
    'weather_sw_radiation_mean',
    'weather_temperature_mean',
    'weather_wind_speed_mean'
]


def _policies_data() -> pd.DataFrame:
    oxford = OxfordGovernmentPolicyDataset()
    return oxford.get_data()[[ISO_COLUMN_NAME, DATE_COLUMN_NAME] + _POLICIES_COLUMNS]


def _mask_data() -> pd.DataFrame:
    masks = MaskPolicies()
    return masks.get_data()[[ISO_COLUMN_NAME, DATE_COLUMN_NAME] + _MASKS_COLUMNS]


def _cases_data() -> pd.DataFrame:
    owid_covid19 = OWIDCovid19()
    return owid_covid19.get_data()[[ISO_COLUMN_NAME, DATE_COLUMN_NAME] + _CASES_COLUMNS]


def _reference_data() -> pd.DataFrame:
    wb = WorldBankDataBank()
    return wb.get_data()[[ISO_COLUMN_NAME] + _REFERENCE_COLUMNS]


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
    return weather.get_data()[[ISO_COLUMN_NAME, DATE_COLUMN_NAME] + _WEATHER_COLUMNS]


def _create_interventions_data() -> pd.DataFrame:
    interventions_data = (_policies_data()
                          .merge(_mask_data(), on=[ISO_COLUMN_NAME, DATE_COLUMN_NAME], how='left')
                          .set_index([ISO_COLUMN_NAME, DATE_COLUMN_NAME]))
    interventions_data['npi_masks'] = (interventions_data['npi_masks']
                                       .groupby(level=0)
                                       .ffill()
                                       .fillna(0.))
    interventions_data = interventions_data.reset_index()

    country_name_map = {
        iso: country_name_from_iso(iso)
        for iso in interventions_data[ISO_COLUMN_NAME].unique()
    }

    interventions_data.insert(
        0,
        'country_name', 
        interventions_data[ISO_COLUMN_NAME].replace(country_name_map))

    return interventions_data


def _create_data() -> pd.DataFrame:
    interventions_data = _create_interventions_data()
    interventions_cases = interventions_data.merge(
        _cases_data(), on=[ISO_COLUMN_NAME, DATE_COLUMN_NAME], how='left').fillna(0)

    combined = (interventions_cases
                .merge(_mobility_data(), on=[ISO_COLUMN_NAME, DATE_COLUMN_NAME], how='left')
                .merge(_transport_mobility_data(), on=[ISO_COLUMN_NAME, DATE_COLUMN_NAME], how='left')
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
