"""Generate age and sex disaggregatred data for multiple countries."""
import pandas as pd
from age.data.load.countries import austria, belgium, brazil, canada, chile, czechia, denmark, finland, france, germany, hongkong, india, italy, korea, mexico, netherlands, portugal, uk, usa

import logging
_log = logging.getLogger(__name__)

_REFERENCE_DATA_PATH = 'https://raw.githubusercontent.com/rs-delve/covid19_datasets/master/dataset/combined_dataset_latest.csv'


class Generator():

    def __init__(self):
        self._reference_data = pd.read_csv(_REFERENCE_DATA_PATH, parse_dates=['DATE'])
        self._country_loaders = self._create_country_loaders(self._reference_data)

    def _create_country_loaders(self, reference_data):
        country_loaders = {
            austria.ISO: austria.Austria(),
            belgium.ISO: belgium.Belgium(),
            brazil.ISO: brazil.Brazil(reference_data),
            canada.ISO: canada.Canada(reference_data),
            chile.ISO: chile.Chile(),
            czechia.ISO: czechia.Czechia(),
            france.ISO: france.France(),
            germany.ISO: germany.Germany(reference_data),
            india.ISO: india.India(reference_data),
            korea.ISO: korea.Korea(),
            mexico.ISO: mexico.Mexico(reference_data),
            netherlands.ISO: netherlands.Netherlands(),
            portugal.ISO: portugal.Portugal(),
            uk.ISO: uk.UnitedKingdom(),
            usa.ISO: usa.USA(reference_data)
        }
        return country_loaders

    def generate_dataset(self):
        all_cases = []
        all_deaths = []

        for iso, loader in self._country_loaders.items():
            _log.info(f'Loading {iso}')
            all_cases.append(loader.cases())
            all_deaths.append(loader.deaths())

        cases = pd.concat(all_cases, axis=0)
        deaths = pd.concat(all_deaths, axis=0)

        return pd.merge(cases, deaths, on=['Date', 'Age', 'Sex'])
