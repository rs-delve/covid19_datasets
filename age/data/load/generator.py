"""Generate age and sex disaggregatred data for multiple countries."""
import pandas as pd
from age.data.load.countries import austria, belgium, brazil, canada, chile, czechia, denmark, finland, france, germany, hongkong, india, italy, korea, mexico, netherlands, portugal, uk, usa

_REFERENCE_DATA_PATH = 'https://raw.githubusercontent.com/rs-delve/covid19_datasets/master/dataset/combined_dataset_latest.csv'


class Generator():

    def __init__(self):
        self._reference_data = pd.read_csv(_REFERENCE_DATA_PATH, parse_dates=['DATE'])
        self._country_loaders = self._create_country_loaders(self._reference_data)

    def _create_country_loaders(self, reference_data):
        country_loaders = [
            austria.Austria(),
            belgium.Belgium(),
            brazil.Brazil(),
            canada.Canada(reference_data),
            chile.Chile(),
            czechia.Czechia(),
            france.France(),
            germany.Germany(reference_data),
            india.India(reference_data),
            korea.Korea(),
            mexico.Mexico(reference_data),
            netherlands.Netherlands(),
            portugal.Portugal(),
            uk.UnitedKingdom(),
            usa.USA(reference_data)
        ]
        return country_loaders

    def generate_dataset(self):
        all_cases = [c.cases() for c in self._country_loaders]
        all_deaths = [c.deaths() for c in self._country_loaders]

        cases = pd.concat(all_cases, axis=0)
        deaths = pd.concat(all_deaths, axis=0)

        return pd.merge(cases, deaths, on=['Date', 'Age', 'Sex'])
