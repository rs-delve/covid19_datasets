import datetime
import pycountry


_ISO_OVERRIDE = {
    'RKS': 'Republic of Kosovo'
}


def get_country_iso(country_name):
    # Country names in this dataset is a wondeful mix of official and normal names
    # so we will try looking up by all of that
    # and a fuzzy search on top

    country = pycountry.countries.get(name=country_name)
    if country is not None:
        return country.alpha_3
    
    country = pycountry.countries.get(official_name=country_name)
    if country is not None:
        return country.alpha_3
    
    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        return country.alpha_3
    except LookupError:
        return None


def last_day_of_calenderweek(year, week):
    first = datetime.date(year, 1, 1)
    base = 1 if first.isocalendar()[1] == 1 else 8
    return first + datetime.timedelta(days=base - first.isocalendar()[2] + 7 * (week - 1) + 6)


def country_name_from_iso(iso):
    if iso in _ISO_OVERRIDE:
        return _ISO_OVERRIDE[iso]
    else:
        return pycountry.countries.get(alpha_3=iso).name
