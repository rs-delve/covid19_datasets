import pandas as pd


import logging
_log = logging.getLogger(__name__)

COUNTRIES = [
    'australia',
    'brazil',
    'canada',
    'china',
    'denmark',
    'finland',
    'france',
    'germany',
    'hong kong',
    'india',
    'indonesia',
    'italy',
    'japan',
    'malaysia',
    'mexico',
    'netherlands',
    'norway',
    'philippines',
    'saudi arabia',
    'singapore',
    'south-korea',
    'spain',
    'sweden',
    'taiwan',
    'thailand',
    'united arab emirates',
    'united-kingdom',
    'united-states',
    'vietnam',
]
COUNTRY_PATH_FORMAT = 'https://raw.githubusercontent.com/YouGov-Data/covid-19-tracker/master/data/{}.csv'


def _load_dataset():
    _log.info("Loading dataset")
    all_data = []
    for country in COUNTRIES:
        country_name = country.replace(' ', '-')
        path = COUNTRY_PATH_FORMAT.format(country_name)
        try:
            country_df = pd.read_csv(path)
        except:
            try:
                country_df = pd.read_csv(path, encoding='cp1252')
            except:
                _log.error(f'ERROR WITH {country}')

        country_df['country'] = country
        all_data.append(country_df)
    _log.info("Loaded")

    return pd.concat(all_data, axis=0)


class YouGovBehaviouralTracker:
    """
    Data from the Imperial College London YouGov Covid 19 Behaviour Tracker Data Hub
    """
    
    data = None

    def __init__(self, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data

        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if YouGovBehaviouralTracker.data is None or force_load:
            YouGovBehaviouralTracker.data = _load_dataset()

    def get_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return YouGovBehaviouralTracker.data
