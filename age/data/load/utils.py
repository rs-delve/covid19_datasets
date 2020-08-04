import pandas as pd


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
