import pycountry
import pandas as pd
import logging
from .constants import *
_log = logging.getLogger(__name__)


_MOBILITY_PATH = 'https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv'

_COLUMN_NAME_MAP = {
    'retail_and_recreation_percent_change_from_baseline': 'mobility_retail_recreation',
    'grocery_and_pharmacy_percent_change_from_baseline': 'mobility_grocery_pharmacy',
    'parks_percent_change_from_baseline': 'mobility_parks',
    'transit_stations_percent_change_from_baseline': 'mobility_transit_stations',
    'workplaces_percent_change_from_baseline': 'mobility_workplaces',
    'residential_percent_change_from_baseline': 'mobility_residential'
}

_NORMALISE_COLUMNS = _COLUMN_NAME_MAP.values()


def _load_dataset():
    _log.info(f'Loading data from {_MOBILITY_PATH}')
    raw = pd.read_csv(_MOBILITY_PATH)
    mob_rep_data = raw.rename(columns={'date': DATE_COLUMN_NAME})
    mob_rep_data[DATE_COLUMN_NAME] = pd.to_datetime(mob_rep_data[DATE_COLUMN_NAME])
    mob_rep_data = mob_rep_data[mob_rep_data["sub_region_1"].isnull()]
    mob_rep_data = mob_rep_data.rename(columns=_COLUMN_NAME_MAP)
    mob_rep_data = mob_rep_data.drop(['sub_region_1', 'sub_region_2', 'country_region'], axis=1)
    mob_rep_data = mob_rep_data.dropna(subset=['country_region_code'])

    mob_rep_data[ISO_COLUMN_NAME] = mob_rep_data.country_region_code.apply(lambda c: pycountry.countries.get(alpha_2=c).alpha_3)

    mob_rep_data = mob_rep_data.drop('country_region_code', axis='columns')
    _log.info('Loaded')
    return mob_rep_data


def _normalise(df, column_names):
    result = df.copy()
    for feature_name in column_names:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


class Mobility:
    """
    Data from Google Mobility Report: https://www.google.com/covid19/mobility/
    """

    _data = None

    def __init__(self, force_load: bool = False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data.

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if Mobility._data is None or force_load:
            Mobility._data = _load_dataset()

    def get_data(self, normalise=False) -> pd.DataFrame:
        """
        Returns the dataset as Pandas dataframe.

        :param normalise: If true, will normalise data to lie in the range 0 to 1.
        """

        if normalise:
            return _normalise(Mobility._data, _NORMALISE_COLUMNS)
        else:
            return Mobility._data
