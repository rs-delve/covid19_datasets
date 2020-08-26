This document lists the sources for the various countries contained in the dataset and outlines any processing steps taken in addition to standardisation of formats.

# Austria

### Source 
[COVerAGE-DB](https://github.com/timriffe/covid_age) input database
- Cases and deaths by age group
- Fractions of total cases and deaths by sex

### Processing Steps
- Split cases and deaths by age group using total case by sex fractions
- Standardise age ranges
- Convert cumulative counts to daily new counts

# Belgium

### Source
[Sciensano Epistat](https://epistat.wiv-isp.be/home/)
- [Cases by age and sex](https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv)
- [Deaths by age and sex](https://epistat.sciensano.be/Data/COVID19BE_MORT.csv)

### Processing Steps
- Derive "both sex" values by summing male and female

# Brazil

### Source
[COVerAGE-DB](https://github.com/timriffe/covid_age) input database
- Deaths by age group and sex

### Processing Steps
- Convert cumulative counts to daily new counts
- Rescale data to match totals reported by ECDC.
  - This is to address the significant drop in totals in more recent data, likely due to reporting delays. We consider this to be a sample of the total cases and rescale it.
  
# 

