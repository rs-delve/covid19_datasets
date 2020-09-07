import pandas as pd
import datetime
import numpy as np

def map_age(age):
    """Map ages to standard buckets."""
    try:
        age = int(age)
        if age >= 90:
            return '90+'

        lower = (age // 10) * 10
        upper = age+9 if age % 10 == 0 else ((age + 9) // 10) * 10 - 1

        return f'{lower}-{upper}'
    except:
        if 'month' in age.lower():
            return '0-9'
        return age


def last_day_of_calenderweek(year, week):
    first = datetime.date(year, 1, 1)
    base = 1 if first.isocalendar()[1] == 1 else 8
    return first + datetime.timedelta(days=base - first.isocalendar()[2] + 7 * (week - 1) + 6)


def age_string_to_tuple(ages: str) -> (int, int):
    '''Converts string age format to tuple of integers (lower, upper).
    Eg. \'10-14\' becomes (10, 14), or \'85+' to (85, np.float(inf))
    '''
    if '+' in ages:
        return (int(ages[:-1]), np.float('inf'))
    else:
        return tuple([int(i) for i in ages.split('-')]) 