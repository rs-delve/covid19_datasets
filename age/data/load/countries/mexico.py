import pandas as pd
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils
from age.data.load import ined
import logging
import datetime
from urllib.request import urlopen

_log = logging.getLogger(__name__)

_DATA_PATH = 'https://raw.githubusercontent.com/carranco-sga/Mexico-COVID-19/master/Open_data/COVID-19/{}/{}.zip'

_COLUMN_NAMES = {
    'FECHA_ACTUALIZACION': 'update_date',
    'SEXO': 'Sex',  # 1 = Female, 2 = Male, 99 = Not specified
    'FECHA_INGRESO': 'admission_date',
    'FECHA_SINTOMAS': 'symptom_date',
    'FECHA_DEF': 'death_date',
    'EDAD': 'Age',
    'ID_REGISTRO': 'Id',
    'RESULTADO': 'covid_test_result'  # 1 = tested positive, 2 = tested negative, 3 = pending result
}

_SEX_MAPPING = {1: 'f', 2: 'm', 99: 'Unknown'}
_MAX_ATTEMPTS = 10

ISO = 'MEX'

def _try_get_raw_data() -> pd.DataFrame:
    current_date = pd.to_datetime(datetime.date.today())
    
    for _ in range(_MAX_ATTEMPTS):
        url = _DATA_PATH.format(current_date.strftime('%Y%m'), current_date.strftime('%Y%m%d'))
        _log.info(f'Trying {url}')
        try:
            with urlopen(url) as f:
                _log.info(f'Found data at {url}')
                return pd.read_csv(url, compression='zip', encoding='cp1252')
        except: 
            pass
        current_date -= pd.offsets.Day(1)

    raise ValueError('Could not find data!')


def _load_raw_data() -> pd.DataFrame:
    df = _try_get_raw_data()
    df = df.rename(columns=_COLUMN_NAMES)[_COLUMN_NAMES.values()]
    df.admission_date = pd.to_datetime(df.admission_date)
    df.symptom_date = pd.to_datetime(df.symptom_date)
    df.Age = df.Age.apply(utils.map_age)
    df.Sex = df.Sex.replace(_SEX_MAPPING)
    return df


class Mexico(base.LoaderBase):
    def __init__(self, reference_data):
        self._raw_data = None
        self._reference_data = reference_data

    def _cutoff_date(self):
        cutoff_date = self._raw_data.symptom_date.max() - pd.offsets.Day(10)
        return cutoff_date

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_data is None:
            self._raw_data = _load_raw_data()
        # Remove last 10 days of data which are not reliable
        
        cases = (self._raw_data
                .query(f'covid_test_result == 1 and symptom_date < "{self._cutoff_date()}"')
                .groupby(['symptom_date', 'Age', 'Sex']).Id
                .count()
                .reset_index().rename(columns={
                    'symptom_date': 'Date',
                    'Id': 'cases_new'
                }))
        return cases

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_data is None:
            self._raw_data = _load_raw_data()
        deaths = self._raw_data.query(f'death_date != "9999-99-99" and covid_test_result == 1 and death_date < "{self._cutoff_date()}"')
        deaths.death_date = pd.to_datetime(deaths.death_date)
        deaths = deaths.groupby(['death_date', 'Age', 'Sex']).Id.count().reset_index().rename(columns={'death_date': 'Date', 'Id': 'deaths_new'})
        return deaths

    def cases(self) -> pd.DataFrame:
        raw_cases = self.raw_cases()
        cases = transformations.add_both_sexes(raw_cases)
        cases = transformations.rescale(cases, self._reference_data.query(f'ISO == "{ISO}"'), 'cases_new')
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        raw_deaths = self.raw_deaths()
        deaths = transformations.add_both_sexes(raw_deaths)
        deaths = transformations.rescale(deaths, self._reference_data.query(f'ISO == "{ISO}"'), 'deaths_new')
        deaths['ISO'] = ISO
        return deaths
