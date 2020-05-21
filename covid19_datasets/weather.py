import pandas as pd
import numpy as np
import datetime
import logging

from .constants import *
import requests
from .utils import get_country_iso
_log = logging.getLogger(__name__)

_PATH = 'https://raw.githubusercontent.com/rs-delve/covid19_datasets/master/data/countries_daily_weighted_averages_merged.csv'

_COLUMN_NAMES = {
    'Precipitation_Weighted_Daily_Average_maximum': 'weather_precipitation_max',
    'Precipitation_Weighted_Daily_Average_mean': 'weather_precipitation_mean',
    'Humidity_Weighted_Daily_Average_maximum': 'weather_humidity_max',
    'Humidity_Weighted_Daily_Average_mean': 'weather_humidity_mean',
    'Humidity_Weighted_Daily_Average_minimum': 'weather_humidity_min',
    'SW_Weighted_Daily_Average_maximum': 'weather_sw_radiation_max', 
    'SW_Weighted_Daily_Average_mean': 'weather_sw_radiation_mean',
    'Temperature_Weighted_Daily_Average_maximum': 'weather_temperature_max',
    'Temperature_Weighted_Daily_Average_mean': 'weather_temperature_mean',
    'Temperature_Weighted_Daily_Average_minimum': 'weather_temperature_min',
    'Wind_Speed_Weighted_Daily_Average_maximum': 'weather_wind_speed_max',
    'Wind_Speed_Weighted_Daily_Average_minimum': 'weather_wind_speed_min',
    'Wind_Speed_Weighted_Daily_Average_mean': 'weather_wind_speed_mean'
}

def _load_dataset() -> pd.DataFrame:
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

    def get_raw_data(self) -> pd.DataFrame:
        """
        Returns the raw dataset as Pandas dataframe
        """
        return Weather.data

    def get_data(self) -> pd.DataFrame:
        """
        Return the dataset in a standardised format.
        """
        return get_raw_data().rename(columns=_COLUMN_NAMES)
