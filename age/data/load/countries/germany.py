import pandas as pd
import re
from age.data.load.countries import base
from age.data.load import transformations
from age.data.load import utils
from age.data.load import ined

_PATH = 'https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv'

_COLUMN_MAP = {
  'IdBundesland': 'State ID',
  'Bundesland': 'Federal State',
  'Landkreis': 'District',
  'Altersgruppe': 'Age',
  'Geschlecht': 'Sex',
  'AnzahlFall': 'cases_new',
  'AnzahlTodesfall': 'deaths_new',
  'Meldedatum': 'Date',
  'IdLandkreis': 'District ID',
  'Datenstand': 'Data Status',
  'NeuerFall': 'New Cases',
  'NeuerTodesfall': 'New Deaths',
  'Refdatum': 'Ref Date',
  'NeuGenesen': 'New Recoveries',
  'AnzahlGenesen': 'Recoveries',
  'IstErkrankungsbeginn': 'Onset of Illness',
  'Altersgruppe2': 'Age Group 2'
}

_NOT_APPLICABLE = 'Nicht übermittelt'

ISO = 'DEU'

class Germany(base.LoaderBase):
    def __init__(self, reference_data):
        self._raw_data = None
        self._reference_data = reference_data

    def _load_raw_data(self):
        raw_data = pd.read_csv(_PATH).rename(columns=_COLUMN_MAP).replace(_NOT_APPLICABLE, 'N/A')
        raw_data['Date'] = pd.to_datetime(raw_data['Date'])
        raw_data['Date'] = raw_data['Date'].dt.tz_localize(None)
        raw_data = (raw_data
                    .groupby(['Date', 'Age', 'Sex'])[['cases_new', 'deaths_new']]
                    .sum()
                    .unstack().unstack()
                    .fillna(0)
                    .resample('d').ffill()
                    .stack().stack()
                    .reset_index())
        raw_data.Age = raw_data.Age.apply(lambda s: re.sub('A0?', '', s))
        raw_data.Sex = raw_data.Sex.replace({'M': 'm', 'W': 'f'})
        self._raw_data = raw_data

    def raw_cases(self) -> pd.DataFrame:
        if self._raw_data is None:
            self._load_raw_data()
        return self._raw_data[['Date', 'Age', 'Sex', 'cases_new']].query('Age != "unbekannt" and Sex != "unbekannt"')

    def raw_deaths(self) -> pd.DataFrame:
        if self._raw_data is None:
            self._load_raw_data()
        return self._raw_data[['Date', 'Age',	'Sex', 'deaths_new']].query('Age != "unbekannt" and Sex != "unbekannt"')

    def cases(self) -> pd.DataFrame:
        cases = self.raw_cases()
        cases = transformations.add_both_sexes(cases)
        cases['ISO'] = ISO
        return cases

    def deaths(self) -> pd.DataFrame:
        deaths = self.raw_deaths()
        deaths = transformations.add_both_sexes(deaths)
        deaths['ISO'] = ISO
        return deaths
