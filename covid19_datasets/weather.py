import pandas as pd
import numpy as np
import datetime
import logging

from .constants import *
import requests
from .utils import get_country_iso
_log = logging.getLogger(__name__)

_PATH = 'https://raw.githubusercontent.com/rs-delve/covid19_datasets/master/data/countries_daily_weighted_averages.csv'


def _load_dataset():
  _log.info(f'Loading weather data from {_PATH}')
  df = pd.read_csv(_PATH, parse_dates=['Date'])
  df = df.rename(columns={'Date': DATE_COLUMN_NAME, 'ISO': ISO_COLUMN_NAME})
  _log.info('Weather data loaded')
  return df


class Weather():
    """
    Daily weighted average temperature, humididy and short-wave-length radiation.

    For each city in the cities dataset, we've taken the area defined by its 
    latitude+- 0.2 degrees, and longitude+- 0.2 degrees and for each day computed 
    the mean value for temperature, humidity, and short-wavelength radiation in that area. 
    To produce the daily population-weighted averages for each country, we compute the 
    convex combination of mean local values for each city, where the coefficients are 
    proportional to their population

    Raw weather data provided by the UK Met Office. City coordinate data and population 
    sizes provided by Simple Maps (https://simplemaps.com/)
    """
    
    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data
        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if Weather.data is None or force_load:
            Weather.data = _load_dataset()

    def get_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return Weather.data
