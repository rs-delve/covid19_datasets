from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from urllib.request import Request, urlopen
import pandas as pd
import datetime
import logging

_log = logging.getLogger(__name__)


def find_ined_data_link(ined_url, page_language='en'):
    with urlopen(ined_url) as f:
        soup = BeautifulSoup(f, 'html.parser')

    language_texts = {
        'fr': 'Fichier des données (.xlsx)',
        'en': 'Data file (.xlsx)'
    }
    data_file_link = [a for a in soup.find_all('a') 
        if a.contents and a.contents[0] == language_texts[page_language]]
    if not data_file_link:
        raise ValueError(
            f'Could not find link with text "{language_texts[page_language]}"')
    return data_file_link[0].attrs['href'].replace(' ', '%20')


def read_ined_table(ined_url, sheet_name, population_column, page_language='en', date_format='%d/%m/%Y', skip_columns=None, num_rows=10):
    skip_columns = skip_columns or []
    deaths_path = find_ined_data_link(ined_url, page_language)
    deaths_raw = pd.read_excel(deaths_path, sheet_name=sheet_name, skiprows=5, header=[0, 1], 
            parse_dates=False).iloc[:num_rows]

    if 'Age Group' in deaths_raw.columns:
        age_group_col = 'Age Group'
    elif 'Age group' in deaths_raw.columns:
        age_group_col = 'Age group'
    else:
        raise ValueError(
            f'Could not find Age Group column in columns: {deaths_raw.columns}')

    deaths = deaths_raw.set_index(
        deaths_raw[age_group_col]['Unnamed: 0_level_1'].rename('Age'))
    deaths = deaths.drop([age_group_col] + skip_columns, axis='columns')

    if population_column not in deaths_raw.columns:
        _log.warn(f'Could not find population column "{population_column}" in columns: {deaths_raw.columns}')
    else:
        deaths = deaths.drop(population_column, axis='columns')

    deaths = deaths.swaplevel(axis=1).stack()[
        ['Both sexes',	'Females',	'Males']]
    deaths = deaths.stack().to_frame().reset_index().rename(columns={
        'level_1': 'Date',
        'level_2': 'Sex',
        0: 'deaths_new'
    })

    deaths.Date = deaths.Date.apply(lambda d: d.replace(
        '**', '').strip() if isinstance(d, str) else d)
    deaths.Date = deaths.Date.apply(lambda d: d if isinstance(d, datetime.datetime) else pd.to_datetime(d, format=date_format))
    deaths.Sex = deaths.Sex.replace(
        {'Both sexes': 'b', 'Females': 'f', 'Males': 'm'})

    deaths = round(deaths.set_index(['Date', 'Age', 'Sex']).unstack(
    ).unstack().resample('d').interpolate().diff().stack().stack())
    deaths[deaths < 0] = 0

    return deaths.reset_index()
