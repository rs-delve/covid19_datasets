"""Read data from COVerAGE DB.

Available from: https://github.com/timriffe/covid_age
"""
from io import BytesIO
import osfclient
import logging
import numpy as np
import os
import pandas as pd

_log = logging.getLogger(__name__)

CACHE_LOCATION = './cache/'


def _field_to_source_field(field: str) -> str:
    if field == 'cases_new':
        source_field = 'Cases'
    elif field == 'deaths_new':
        source_field = 'Deaths'
    else:
        raise ValueError(
            f'Invalid field: {field}; should be "cases_new" or "deaths_new"')
    return source_field


def _ensure_non_decreasing(df):
    df[df < df.shift(1)] = np.nan
    return df.ffill()


def _ensure_contiguous_days(data):
    # data should be in tidy format
    fixed = _ensure_non_decreasing(data.set_index(
        ['Date', 'Sex', 'Age']).unstack().unstack().resample('D').ffill())
    return fixed.stack().stack().reset_index()


def _split_sex_by_fractions(combined_data, fractions, field):
    # combined data should be for both sexes ("b") and fractions for male ("m") and female ("f")
    joined = (pd.merge(
        combined_data,
        fractions.set_index(['Date', 'Sex'])['Value'].unstack().reset_index(),
        on='Date')
        .set_index(['Date', 'Age']))

    female = np.round(joined[field] * joined.f).to_frame()
    female['Sex'] = 'f'
    male = np.round(joined[field] * joined.m).to_frame()
    male['Sex'] = 'm'

    final = pd.concat(
        [combined_data,
         female.reset_index().rename(columns={0: field}),
         male.reset_index().rename(columns={0: field})], axis=0)
    return final


class CoverageDB():
    _cache = {}

    def _populate_cache(self, filename):
        osf = osfclient.api.OSF()
        proj = osf.project('mpwjq')

        storage = proj.storage()
        for file in storage.files:
            if file.name != filename:
                continue

            with open('temp.b', 'wb') as f:
                file.write_to(f)
            _log.info(f'Downloaded {file.name}')
            with open('temp.b', 'r') as f:
                df = pd.read_csv('temp.b', skiprows=1, compression='zip' if filename.endswith('zip') else 'infer')
            df = df[df.Date != 'NA.NA.NA']
            df.Date = pd.to_datetime(df.Date, format='%d.%m.%Y', errors='coerce')
            df = df[df.Date.notna()]
            self._cache[file.name] = df

    def _get_data_from_file(self, filename: str) -> pd.DataFrame:
        if filename not in CoverageDB._cache:
            self._populate_cache(filename)

        if filename not in CoverageDB._cache:
            raise ValueError(f'{filename} does not exist')

        return CoverageDB._cache[filename]

    def get_counts_from_input_db(self, country, field, region=None):
        source_field = _field_to_source_field(field)
        query = f'Country == "{country}" and Metric == "Count" and Measure == "{source_field}"'
        if region:
            query = query + f' and Region=="{region}"'
        input_df = self._get_data_from_file('inputDB.zip')
        counts = input_df.query(query)[['Date', 'Age', 'Sex', 'Value']].rename(
            columns={'Value': field})
        return counts

    def get_sex_fractions_from_input_db(self, country, field):
        source_field = _field_to_source_field(field)
        input_df = self._get_data_from_file('inputDB.zip')
        sex_fractions = input_df.query(
            f'Country == "{country}" and Measure == "{source_field}" and Metric=="Fraction" and Age == "TOT" and (Sex == "m" or Sex == "f")')
        return sex_fractions

    def get_data_from_input_db(self, country, field, region=None):
        """Get CUMULATIVE counts from the CoverAGE input database."""
        country_data = self.get_counts_from_input_db(country, field, region)
        country_data = _ensure_contiguous_days(country_data)

        # Contains total only, so split by sex using fractions
        if len(country_data.Sex.unique()) == 1:
            country_data_sex_fraction = self.get_sex_fractions_from_input_db(
                country, field)
            country_data = _split_sex_by_fractions(
                country_data, country_data_sex_fraction, field)

        # Remove the "total" age
        country_data = country_data.query('Age != "TOT"')
        return country_data
