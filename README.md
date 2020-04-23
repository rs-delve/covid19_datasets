# DELVE COVID19 Dataset Access

This repository provides a data set for COVID19 research consolidated from multiple sources.
Code is provided for easily accessing both the combined and underlying data sets.

Usage examples are given in this [Jupyter notebook](./usage_examples.ipynb).

## Combined Dataset Columns
The combined dataset provides the following columns for each ISO (the 3 letter ISO country code) and DATE.

Note that in this table a "Y" in "Is Daily" indicates that value comes from a time series for every day. "N" indicates that the value is country-level and is the same for all dates for a country.

| Column Name |	Description | Data Type/Measurement | Source | Is Daily |
| ----------- |	----------- | --------------------- | ------ | -------- |
| CountryName | Name of country | Text | Oxford Government Response Tracker | Y |
| School closing | Closing of schools and universities. 
 | Ordinal scale \ 0 - No measures; 1 - Recommend; 2 - Required \ + binary for geographic scope \ 0 - Targeted;  1- General | Oxford Government Response Tracker | Y |
| Workplace closing | Closing of work places | Ordinal scale 
0 - No measures; 1 - Recommend; 2 - Required 
+ binary for geographic scope 
0 - Targeted;  1- General | Oxford Government Response Tracker | Y |
| Cancel public events | Cancellation of public events
 | Ordinal scale 
0 - No measures; 1 - Recommend; 2 - Required 
+ binary for geographic scope 
0 - Targeted;  1- General | Oxford Government Response Tracker | Y |
| Close public transport | Closing of public transport
 | Ordinal scale 
0 - No measures; 1 - Recommend; 2 - Required 
+ binary for geographic scope 
0 - Targeted;  1- General | Oxford Government Response Tracker | Y |
| Public information campaigns | Presence of public info campaigns | Binary
0 -No COVID-19 public information campaign; 1 - COVID-19 public information campaign
+ binary for geographic scope
0 - Targeted; 1- General | Oxford Government Response Tracker | Y |
| Restrictions on internal movement | Restrictions on internal movement | Ordinal scale 
0 - No measures; 1 - Recommend; 2 - Required 
+ binary for geographic scope 
0 - Targeted;  1- General | Oxford Government Response Tracker | Y |
| International travel controls | Restrictions on international travel | Ordinal Scale:
0 - No measures; 1 - Screening; 2 - Quarantine on high-risk regions; 3 - Ban on high-risk regions | Oxford Government Response Tracker | Y |
| Fiscal measures | What economic stimulus policies are adopted? | Value of fiscal stimuli, including spending or tax cuts in USD | Oxford Government Response Tracker | Y |
| Monetary measures | What monetary policy interventions are in place? | Value of interest rate in % | Oxford Government Response Tracker | Y |
| Emergency investment in health care | Short-term spending on, e.g, hospitals, masks, etc | Value of new short-term spending on health in USD | Oxford Government Response Tracker | Y |
| Investment in Vaccines | Announced public spending on vaccine development | Value of investment in USD | Oxford Government Response Tracker | Y |
| Testing framework | Who can get tested | Ordinal Scale
0 - No testing policy
1 - only testing those who both (a) have symptoms, and (b) meet specific criteria (eg key workers, admitted to hospital, came into contact with a known case, returned from overseas)
2 - testing of anyone showing COVID19 symptoms
3 - open public testing (eg “drive through” testing available to asymptomatic people) | Oxford Government Response Tracker | Y |
| Contact tracing | Are governments doing contact tracing | Ordinal Scale
0 - no contact tracing
1 - limited contact tracing – not done for all cases
2 - comprehensive contact tracing –done for all cases | Oxford Government Response Tracker | Y |
| Masks | Mask policy in force in the country.  | Ordinal Scale
0 - No mask policy in place
1 - Limited mask policy (eg in stores only) or limited enforcement
2 - Widespread mask policy and/or strict enforcement | ACAPS + Manual | Y |
| total_cases | Total (cumulative) confirmed cases in the country, as published by ECDC | Integer number of cases | Our World in Data | Y |
| new_cases | Number of new cases since previous day as published by ECDC | Integer number of cases | Our World in Data | Y |
| total_deaths | Total (cumulative) confirmed deaths in the country, as published by ECDC | Integer number of deaths | Our World in Data | Y |
| new_deaths | Number of new deaths since previous day as published by ECDC | Integer number of deaths | Our World in Data | Y |
| total_cases_per_million | Total cases per mililon people | Float number of cases | Our World in Data | Y |
| new_cases_per_million | New cases per million people | Float number of cases | Our World in Data | Y |
| total_deaths_per_million | Total deaths per million people | Float number of deaths | Our World in Data | Y |
| new_deaths_per_million | New detahs per million people | Float number of deaths | Our World in Data | Y |
| total_tests | Total (cumulative) number of COVID-19 tests performed in the country  | Integer number of tests | Our World in Data | Y |
| new_tests | Number of new COVID-19 tests performed in the country  | Integer number of tests | Our World in Data | Y |
| total_tests_per_thousand | Total (cumulative) number of COVID-19 tests performed per 1000 people | Float number of tests | Our World in Data | Y |
| new_tests_per_thousand | Number of new COVID-19 tests performned per 1000 people | Float number of tests | Our World in Data | Y |
| days_since_first_case | Days since the first recorded case in the country | 0 until the first case is recoded, then DATE - first_case_date in days | Derived | Y |
| days_since_first_death | Days since the first recorded death in the country | 0 until the first death is recoded, then DATE - first_death_date in days | Derived | Y |
| median_age | Median age of population | Float age | Our World in Data | N |
| hospital_beds (per 1000) | Number of hospital beds per 1000 people | Float | World Bank Data Bank | N |
| physicians (per 1000) | Number of physicians per 1000 people | Float | World Bank Data Bank | N |
| nurses (per 1000) | Number of nurses per 1000 people | Float | World Bank Data Bank | N |
| Smoking prevalence, total, ages 15+ | Percent of people over 15 who smoke | Percentage | World Bank Data Bank | N |
| Mortality rate, adult, female (per 1,000 female adults) | Average mortality rate per 1000 female adults | Number of people per 1000 females | World Bank Data Bank | N |
| Mortality rate, adult, male (per 1,000 male adults) | Average mortality rate per 1000 male adults | Number of people per 1000 males | World Bank Data Bank | N |
| Population Density | Average Density of population over entire country | Number of people per square kilometre of land area | World Bank Data Bank | N |
| Population in Urban Agglomerations | Population living in urban areas | Percent of total population living in agglomerations consisting of over 1 million people | World Bank Data Bank | N |
| Population Female | Female population | Number of people | World Bank Data Bank | N |
| Population Male | Male population | Number of people | World Bank Data Bank | N |
| Population | Total population | Number of people | World Bank Data Bank | N |


