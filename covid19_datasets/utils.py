import pycountry

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
