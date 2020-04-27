import pandas as pd
from pandas_datareader import wb


import logging
_log = logging.getLogger(__name__)


WORLD_BANK_INDICATORS = {
  'hospital_beds (per 1000)': 'SH.MED.BEDS.ZS',
  'physicians (per 1000)': 'SH.MED.PHYS.ZS',
  'nurses (per 1000)': 'SH.MED.NUMW.P3',
  'Diabetes (% of population ages 20 to 79)': 'SH.STA.DIAB.ZS',
  'Smoking prevalence, total, ages 15+': 'SH.PRV.SMOK',
  'Smoking prevalence, females (% of adults)': 'SH.PRV.SMOK.FE',
  'Smoking prevalence, males (% of adults)': 'SH.PRV.SMOK.MA',
  'Mortality rate, adult, female (per 1,000 female adults)': 'SP.DYN.AMRT.FE',
  'Mortality rate, adult, male (per 1,000 male adults)': 'SP.DYN.AMRT.MA',
  'Population Density': 'EN.POP.DNST',
  'Population in Urban Agglomerations': 'EN.URB.MCTY',
  'Population Female': 'SP.POP.TOTL.FE.IN',
  'Population Male': 'SP.POP.TOTL.MA.IN',
  'Population': 'SP.POP.TOTL',
  'Population of Compulsory School Age': 'UIS.SAP.CE'
}


AGGREGATES = [
  'Arab World',
  'Caribbean small states',
  'Central Europe and the Baltics',
  'Early-demographic dividend',
  'East Asia & Pacific',
  'East Asia & Pacific (IDA & IBRD countries)',
  'East Asia & Pacific (excluding high income)',
  'Euro area',
  'Europe & Central Asia',
  'Europe & Central Asia (IDA & IBRD countries)',
  'Europe & Central Asia (excluding high income)',
  'European Union',
  'Fragile and conflict affected situations',
  'Heavily indebted poor countries (HIPC)',
  'High income',
  'IBRD only',
  'IDA & IBRD total',
  'IDA blend',
  'IDA only',
  'IDA total',
  'Late-demographic dividend',
  'Latin America & Caribbean (excluding high income)',
  'Latin America & the Caribbean (IDA & IBRD countries)',
  'Least developed countries: UN classification',
  'Low & middle income',
  'Low income',
  'Lower middle income',
  'Middle East & North Africa',
  'Middle East & North Africa (IDA & IBRD countries)',
  'Middle East & North Africa (excluding high income)',
  'Middle income',
  'North America',
  'Not classified',
  'OECD members',
  'Other small states',
  'Pacific island small states',
  'Post-demographic dividend',
  'Pre-demographic dividend',
  'Small states',
  'South Asia (IDA & IBRD)',
  'South Asia',
  'Sub-Saharan Africa (IDA & IBRD countries)',
  'Sub-Saharan Africa (excluding high income)',
  'Upper middle income',
  'World',
  'West Bank and Gaza',
]


def _load_dataset(start=2010, end=2020, extra_indicators={}):
    _log.info("Loading dataset")
    indicators = dict(WORLD_BANK_INDICATORS, **extra_indicators)

    all_data = []
    for name, series in indicators.items():
        data = wb.download(indicator=series, country='all', start=start, end=end)
        all_data.append(data.sort_index().groupby(level=0).last().rename(columns={series: name}))

    country_data = pd.concat(all_data, axis=1)
    country_data.index = country_data.index.set_names(['country'])
    
    # Add ISO
    mapping = wb.get_countries()[['name', 'iso3c']].rename(columns={'iso3c': 'ISO'})
    country_data = (country_data.reset_index()
                    .merge(mapping, left_on='country', right_on='name', how='inner')
                    .drop('name', axis='columns'))

    return country_data


class WorldBankDataBank:
    """
    Data from the World Bank Data Bank
    """
    
    data = None

    def __init__(self, start=2010, end=2020, extra_indicators={}, force_load=False):
        """
        Loads the dataset and stores it in memory.
        Further instances of this class will reuse the same data

        :param start: First year of the data series
        :param end: Last year of the data series (inclusive)
        :param extra_indicators: A dictionary of extra indicators to load. 
                                 Indicators loaded by default are available in WORLD_BANK_INDICATORS
                                 More indicators are available in the Data Bank explorer (https://databank.worldbank.org/)
        :param force_load: If true, forces download of the dataset, even if it was loaded already
        """
        # This is to make sure we only load the dataset once during a single session
        if WorldBankDataBank.data is None or force_load:
            WorldBankDataBank.data = _load_dataset(start=start, end=end, extra_indicators=extra_indicators)

    def get_data(self):
        """
        Returns the dataset as Pandas dataframe
        """
        return WorldBankDataBank.data
