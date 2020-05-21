import pandas as pd
import numpy as np
import datetime
import logging

from .constants import *
import requests
from .utils import get_country_iso
_log = logging.getLogger(__name__)


_MOBILITY_INDEX = 'https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/index.json'
_BASE_URL = 'https://covid19-static.cdn-apple.com/'


def _load_dataset():
  json = requests.get(_MOBILITY_INDEX).json()
  base_path = json['basePath']
  filename = json['regions']['en-us']['csvPath']
  path = _BASE_URL + base_path + filename
  _log.info(f'Loading Apple Mobility data from {path}')
  df = pd.read_csv(path)
  return df


class AppleMobility():
    """Load data from Apple Maps Mobility Trends Report. 
    https://www.apple.com/covid19/mobility
    """

    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data
        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if AppleMobility.data is None or force_load:
            AppleMobility.data = _load_dataset()

    def get_raw_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return AppleMobility.data

    def get_country_data(self):
        """
        Return a standardized version of the dataset filtered to country-level 
        data only.
        """

        df = self.get_raw_data()
        df = df.query('geo_type == "country/region"')

        df = (df
              .drop(['geo_type', 'alternative_name', 'sub-region', 'country'], axis='columns')
              .melt(id_vars=['region', 'transportation_type'], var_name=DATE_COLUMN_NAME))

        df[DATE_COLUMN_NAME] = pd.to_datetime(df[DATE_COLUMN_NAME])

        iso_map = {
            country_name: get_country_iso(country_name)
            for country_name in df.region.unique()
        }

        df.region = df.region.replace(iso_map)
        df = df.rename(columns={'region': ISO_COLUMN_NAME})
        df = (df
              .set_index([ISO_COLUMN_NAME, DATE_COLUMN_NAME, 'transportation_type'])
              .unstack()['value']
              .reset_index())
        df = df.rename(columns={
          'driving': 'driving_mobility',
          'transit': 'transit_mobility',
          'walking': 'walking_mobility'
        })
        return df
