import pandas as pd
import datetime
from urllib.error import HTTPError

import logging
_log = logging.getLogger(__name__)


def _load_dataset():
    acaps_path = 'https://www.acaps.org/sites/acaps/files/resources/files/{date}_acaps_-_covid-19_goverment_measures_dataset_v9.xlsx'
    date = datetime.datetime.today().strftime('%Y%m%d')
    path = acaps_path.format(date=date)
    try:
        _log.info("Loading dataset from " + path)
        acaps_df = pd.read_excel(path, sheet_name='Database')
    except HTTPError:
        date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        path = acaps_path.format(date=date)
        _log.info("Failed to load, trying previous day path: " + acaps_path)
        acaps_df = pd.read_excel(path, sheet_name='Database')

    # Clean-up
    acaps_df = acaps_df.drop(['ADMIN_LEVEL_NAME', 'PCODE', 'SOURCE', 'SOURCE_TYPE', 'LINK', 'ENTRY_DATE', 'Alternative source'], axis='columns')
    acaps_df = acaps_df.rename(columns={'DATE_IMPLEMENTED': 'DATE'})
    _log.info("Loaded")
    return acaps_df

class AcapsGovernmentMeasures:
    """
    ACAPS dataset on government measures against the spread of COVID-19
    """
    
    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if AcapsGovernmentMeasures.data is None or force_load:
            AcapsGovernmentMeasures.data = _load_dataset()

            self.country_by_iso = {
                iso: country for iso, country in self.get_data().groupby(['ISO', 'COUNTRY']).first().index
            }

    def get_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return AcapsGovernmentMeasures.data
    
    def get_intervention_categories(self):
        """
        Get all categories of inverventions
        """
        return self.get_data().CATEGORY.unique()
    
    def get_measures(self):
        """
        Get all encountered measures
        """
        return self.get_data().MEASURE.unique()

    def get_interventions_by_country(self, country):
        """
        Get interventions for a specified country as a Pandas dataframe

        :param country: The country name
        """
        return self.get_data().query(f'COUNTRY == "{country}"')
