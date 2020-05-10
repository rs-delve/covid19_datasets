# DELVE COVID19 Dataset Access

This repository provides a data set for COVID19 research consolidated from multiple sources. The dataset is available as CSV which can be loaded into most environments.
Python code is provided for easily accessing both the combined and underlying data sets.

Usage examples are given in this [Jupyter notebook](./usage_example.ipynb).

## Reading the dataset
### Generic Option
Download the CSV from the [Dataset](https://github.com/rs-delve/covid19_datasets/tree/master/dataset) directory

### Python
Install this package using
```pip install git+https://github.com/rs-delve/covid19_datasets.git```
Then load the dataset in Python using
```python
from covid19_datasets import Combined
data_df = Combined().get_data()
```

## Combined Dataset Columns
The combined dataset provides the following columns for each ISO (the 3 letter ISO country code) and DATE.

Note that in this table a "Y" in "Is Daily" indicates that value comes from a time series for every day. "N" indicates that the value is country-level and is the same for all dates for a country.

<table class="table table-bordered table-hover table-condensed">
<thead><tr><th title="Field #1">Column Name</th>
<th title="Field #2">Description</th>
<th title="Field #3">Data Type/Measurement</th>
<th title="Field #4">Source</th>
<th title="Field #5">Is Daily</th>
</tr></thead>
<tbody><tr>
<td style="font-weight:bold">CountryName</td>
<td>Name of country</td>
<td>Text</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">School closing</td>
<td>Closing of schools and universities. <br/></td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend; 2 - Require closing (only some levels or categories,
eg just high school, or just public schools); 3 - Require closing all levels <br/>+ binary for geographic scope <br/>0 - Targeted;  1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Workplace closing</td>
<td>Closing of work places</td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend; 2 - require closing (or work from home) for some sectors or categories of workers; 3 - require closing (or work from home) all but essential workplaces (eg grocery stores, doctors) <br/>+ binary for geographic scope <br/>0 - Targeted;  1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Cancel public events</td>
<td>Cancellation of public events<br/></td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend; 2 - Required <br/>+ binary for geographic scope <br/>0 - Targeted;  1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
 
<tr>
<td style="font-weight:bold">Restrictions on gatherings</td>
<td>Cancellation of public events<br/></td>
<td>Ordinal scale <br/>0 - No restrictions
1 - Restrictions on very large gatherings (the limit is above 1000 people); 2 - Restrictions on gatherings between 100-1000 people; 3 - Restrictions on gatherings between 10-100 people; 4 - Restrictions on gatherings of less than 10 people <br/>+ binary for geographic scope <br/>0 - Targeted;  1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
  
<tr>
<td style="font-weight:bold">Close public transport</td>
<td>Closing of public transport<br/></td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend closing (or significantly reduce volume/route/means of transport available); 2 - Require closing (or prohibit most citizens from using it) <br/>+ binary for geographic scope <br/>0 - Targeted;  1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Public information campaigns</td>
<td>Presence of public info campaigns</td>
<td>Ordinal<br/>0 -No COVID-19 public information campaign; 1 - public officials urging caution about COVID-19; 2 - coordinated public information campaign<br/>+ binary for geographic scope<br/>0 - Targeted; 1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>

<tr>
<td style="font-weight:bold">Stay at home requirements</td>
<td>Recommendations or requirements for citizens to remain in their homes</td>
<td>0 - No measures; 1 - recommend not leaving house; 2 - require not leaving house with exceptions for daily exercise, grocery shopping, and ‘essential’ trips; 3 - Require not leaving house with minimal exceptions (e.g. allowed to leave only once every
few days, or only one person can leave at a time, etc.)
<br/>+ binary for geographic scope<br/>0 - Targeted; 1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>

<tr>
<td style="font-weight:bold">Restrictions on internal movement</td>
<td>Restrictions on internal movement</td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend closing (or significantly reduce volume/route/means of transport); 2 - Require closing (or prohibit most people from using it) <br/>+ binary for geographic scope <br/>0 - Targeted;  1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">International travel controls</td>
<td>Restrictions on international travel</td>
<td>Ordinal Scale:<br/>0 - No measures; 1 - Screening; 2 - Quarantine on high-risk regions; 3 - Ban on high-risk regions; 4 - Total border closure</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>

<tr>
<td style="font-weight:bold">Income Support</td>
<td>Record if the government is covering the salaries or providing direct cash payments, universal basic income, or similar, of people who lose their jobs or cannot work. (Includes payments to firms if explicitly linked to payroll/ salaries)</td>
<td>Ordinal Scale: 0 - no income support; 1 - government is replacing less than 50% of lost salary (or if a flat sum, it is less than 50% median salary); 2 - government is replacing more than 50% of lost salary (or if a flat sum, it is greater than 50% median salary)<br/>+ binary for scope<br/>0 - formal sector workers only 1 - transfers to informal sector workers too</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Debt / contract relief for households</td>
<td>Record if govt. is freezing financial obligations (eg stopping loan repayments, preventing services like water from stopping, or banning evictions)</td>
<td>Ordinal Scale: 0 - No; 1 - Narrow relief, specific to one kind of contract; 2 - broad debt/contract relief</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Fiscal measures</td>
<td>What economic stimulus policies are adopted?</td>
<td>Value of fiscal stimuli, including spending or tax cuts in USD</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Providing support to other countries</td>
<td>Announced offers of COVID-19 related aid spending to other countries</td>
<td>Record monetary value announced if additional to previously announced spending - 0 if there is none</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Emergency investment in health care</td>
<td>Short-term spending on, e.g, hospitals, masks, etc</td>
<td>Value of new short-term spending on health in USD</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Investment in Vaccines</td>
<td>Announced public spending on vaccine development</td>
<td>Value of investment in USD</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Testing framework</td>
<td>Who can get tested</td>
<td>Ordinal Scale<br/>0 - No testing policy<br/>1 - only testing those who both (a) have symptoms, and (b) meet specific criteria (eg key workers, admitted to hospital, came into contact with a known case, returned from overseas)<br/>2 - testing of anyone showing COVID19 symptoms<br/>3 - open public testing (eg “drive through” testing available to asymptomatic people)</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Contact tracing</td>
<td>Are governments doing contact tracing</td>
<td>Ordinal Scale<br/>0 - no contact tracing<br/>1 - limited contact tracing – not done for all cases<br/>2 - comprehensive contact tracing –done for all cases</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Masks</td>
<td>Mask policy in force in the country. </td>
<td>Ordinal Scale<br/>0 - No mask policy in place<br/>1 - Limited mask policy (eg in stores only) or limited enforcement<br/>2 - Widespread mask policy and/or strict enforcement</td>
<td>ACAPS + Manual</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">total_cases</td>
<td>Total (cumulative) confirmed cases in the country, as published by ECDC</td>
<td>Integer number of cases</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">new_cases</td>
<td>Number of new cases since previous day as published by ECDC</td>
<td>Integer number of cases</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">total_deaths</td>
<td>Total (cumulative) confirmed deaths in the country, as published by ECDC</td>
<td>Integer number of deaths</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">new_deaths</td>
<td>Number of new deaths since previous day as published by ECDC</td>
<td>Integer number of deaths</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">total_cases_per_million</td>
<td>Total cases per mililon people</td>
<td>Float number of cases</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">new_cases_per_million</td>
<td>New cases per million people</td>
<td>Float number of cases</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">total_deaths_per_million</td>
<td>Total deaths per million people</td>
<td>Float number of deaths</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">new_deaths_per_million</td>
<td>New detahs per million people</td>
<td>Float number of deaths</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">total_tests</td>
<td>Total (cumulative) number of COVID-19 tests performed in the country </td>
<td>Integer number of tests</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">new_tests</td>
<td>Number of new COVID-19 tests performed in the country </td>
<td>Integer number of tests</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">total_tests_per_thousand</td>
<td>Total (cumulative) number of COVID-19 tests performed per 1000 people</td>
<td>Float number of tests</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">new_tests_per_thousand</td>
<td>Number of new COVID-19 tests performned per 1000 people</td>
<td>Float number of tests</td>
<td>Our World in Data</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">days_since_first_case</td>
<td>Days since the first recorded case in the country</td>
<td>0 until the first case is recoded, then DATE - first_case_date in days</td>
<td>Derived</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">days_since_first_death</td>
<td>Days since the first recorded death in the country</td>
<td>0 until the first death is recoded, then DATE - first_death_date in days</td>
<td>Derived</td>
<td>Y</td>
</tr>

<tr>
<td style="font-weight:bold">Retail and Recreation</td>
<td>Mobility trends for places like restaurants, cafes, shopping centers, theme parks, museums, libraries, and movie theaters.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Grocery and Pharmacy</td>
<td>Mobility trends for places like grocery markets, food warehouses, farmers markets, specialty food shops, drug stores, and pharmacies.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Parks</td>
<td>Mobility trends for places like national parks, public beaches, marinas, dog parks, plazas, and public gardens</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Transit Stations</td>
<td>Mobility trends for places like public transport hubs such as subway, bus, and train stations.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Workplaces</td>
<td>Mobility trends for places of work.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Residential</td>
<td>Mobility trends for places of residence</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">median_age</td>
<td>Median age of population</td>
<td>Float age</td>
<td>Our World in Data</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">hospital_beds (per 1000)</td>
<td>Number of hospital beds per 1000 people</td>
<td>Float</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">physicians (per 1000)</td>
<td>Number of physicians per 1000 people</td>
<td>Float</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">nurses (per 1000)</td>
<td>Number of nurses per 1000 people</td>
<td>Float</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">Smoking prevalence, total, ages 15+</td>
<td>Percent of people over 15 who smoke</td>
<td>Percentage</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">Mortality rate, adult, female (per 1,000 female adults)</td>
<td>Average mortality rate per 1000 female adults</td>
<td>Number of people per 1000 females</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">Mortality rate, adult, male (per 1,000 male adults)</td>
<td>Average mortality rate per 1000 male adults</td>
<td>Number of people per 1000 males</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">Population Density</td>
<td>Average Density of population over entire country</td>
<td>Number of people per square kilometre of land area</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">Population in Urban Agglomerations</td>
<td>Population living in urban areas</td>
<td>Number of people living in agglomerations consisting of over 1 million people</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">Population Female</td>
<td>Female population</td>
<td>Number of people</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">Population Male</td>
<td>Male population</td>
<td>Number of people</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">Population</td>
<td>Total population</td>
<td>Number of people</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
<tr>
<td style="font-weight:bold">Population of Compulsory School Age</td>
<td>Population that is of the age where school attendance is compulsory</td>
<td>Number of people</td>
<td>World Bank Data Bank</td>
<td>N</td>
</tr>
</tbody></table>

