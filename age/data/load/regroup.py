from age.data.load import utils
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from collections import defaultdict
from typing import List
import numpy as np

# Need to have R package ungroup installed 
# https://cran.rstudio.com/web/packages/ungroup/index.html
importr('ungroup')

def _group_year_counts(counts, new_ages, start_count_age=0):
    new_counts = defaultdict(int)
    for age in new_ages:
        lower, upper = age_string_to_tuple(age)
        for i, count in enumerate(counts, start_count_age):
            if i > upper: # small performance optimization
                break
            if lower <= i <= upper:
                new_counts[age] += count
    return list(new_counts.values())
    
def regroup_counts_pclm(ages: List[str], counts: List[int], new_ages: List[str] = None, 
                       max_age: int = 110) -> (List[str], List[float]):
    '''Regroup histogram count data for new age ranges. Uses the pclm method from the 
    R ungroup package https://cran.rstudio.com/web/packages/ungroup/ungroup.pdf

    Args:
        ages: list of age ranges in string format.
        counts: list of counts (eg deaths) corresponding to age ranges.
        new_ages: If None, the ages are in yearly increments. Otherwise provide a list. (default None)
        max_age -- This is the bound of the final unbounded age range when fitting. (default 110)
    Returns:
    (list of new age ranges, list of counts for new age ranges)
    '''
    ages = sorted([utils.age_string_to_tuple(i)[0] for i in ages])
    # define R functions
    pclm = robjects.r['pclm']
    fitted = robjects.r['fitted']
    # nlast: Length of the last interval
    nlast = max_age - ages[-1]
    # get new counts in year-long intervals
    ages_r = robjects.IntVector(ages)
    counts_r = robjects.IntVector(counts)
    res = pclm(ages_r, counts_r, nlast)
    new_counts = list(fitted(res))
    
    # create new age ranges
    min_age = ages[0]
    if new_ages == None:
        new_ages = [f'{i}-{i}' for i in range(min_age, max_age)]
    else:
        new_counts = _group_year_counts(new_counts, new_ages, start_count_age=min_age)
    
    return (new_ages, new_counts)