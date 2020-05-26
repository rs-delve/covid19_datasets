# DELVE COVID-19 Dataset

This repository provides a data set for COVID-19 research consolidated from multiple sources. The dataset is available as CSV which can be loaded into most environments.

## Reading the dataset
Download the CSV from the [dataset](https://github.com/rs-delve/covid19_datasets/tree/master/dataset) directory and load it in your favourite analysis tool. 

In Python you can load the CSV directly using [Pandas](https://pandas.pydata.org/):
```python
import pandas as pd
data_df = pd.read_csv('https://raw.githubusercontent.com/rs-delve/covid19_datasets/master/dataset/combined_dataset_latest.csv')
```

## Examples
We provide two Jupyter notebooks with examples:
- [Basic exploratory data analysis of the combined international dataset](./Data_Exploration.ipynb)
- [Usage of the underlying datasets](./usage_example.ipynb).


## Combined Dataset Columns
The combined dataset provides the following columns

<table class="table table-bordered table-hover table-condensed">
<thead><tr><th title="Field #1">Column Name</th>
<th title="Field #2">Description</th>
<th title="Field #3">Data Type/Measurement</th>
<th title="Field #4">Source</th>
</tr></thead>
<tbody>
<tr>
 <td style="font-weight:bold"><b>ISO</b></td>
 <td>The country code. Together with DATE forms a unique identifier for a row.</td>
 <td>[ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)</td>
 <td></td>
</tr>
<tr>
 <td style="font-weight:bold"><b>DATE</b></td>
 <td>The date associated with the entry. Together with ISO, forms a unique identifier for the row.</td>
 <td>ISO 8601 Date format (YYYY-MM-DD)</td>
 <td></td>
</tr>
<tr>
<td style="font-weight:bold">`country_name`</td>
<td>Name of country</td>
<td>English name according to ISO</td>
<td></td>
</tr>
<tr>
<td style="font-weight:bold">`npi_school_closing`</td>
<td>Closing of schools and universities.</td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend; 2 - Require closing (only some levels or categories,
eg just high school, or just public schools); 3 - Require closing all levels; Blank - No data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_workplace_closing`</td>
<td>Closing of work places</td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend; 2 - require closing (or work from home) for some sectors or categories of workers; 3 - require closing (or work from home) all but essential workplaces (eg grocery stores, doctors); Blank - no data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_cancel_public_events`</td>
<td>Cancellation of public events<br/></td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend; 2 - Required; Blank - no data </td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_gatherings_restrictions`</td>
<td>Limits on private gatherings</td>
<td>Ordinal scale <br/>0 - No restrictions
1 - Restrictions on very large gatherings (the limit is above 1000 people); 2 - Restrictions on gatherings between 100-1000 people; 3 - Restrictions on gatherings between 10-100 people; 4 - Restrictions on gatherings of less than 10 people; Blank - No data</td>
<td>Oxford Government Response Tracker</td>
</tr>  
<tr>
<td style="font-weight:bold">`npi_close_public_transport`</td>
<td>Closing of public transport<br/></td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend closing (or significantly reduce volume/route/means of transport available); 2 - Require closing (or prohibit most citizens from using it); Blank - No data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_stay_at_home`</td>
<td>Recommendations or requirements for citizens to remain in their homes</td>
<td>0 - No measures; 1 - recommend not leaving house; 2 - require not leaving house with exceptions for daily exercise, grocery shopping, and ‘essential’ trips; 3 - Require not leaving house with minimal exceptions (e.g. allowed to leave only once every
few days, or only one person can leave at a time, etc.); Blank - No data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_internal_movement_restrictions`</td>
<td>Restrictions on internal movement between cities/regions</td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend closing (or significantly reduce volume/route/means of transport); 2 - Require closing (or prohibit most people from using it); Blank - No data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_international_travel_controls`</td>
<td>Restrictions on international travel. Note: this records policy for foreign travellers, not citizens</td>
<td>Ordinal Scale:<br/>0 - No restrictions; 1 - Screening arrivals; 2 - Quarantine on arrival from some or all regions; 3 - Ban on arrival from some regions; 4 - Total border closure; Blank - No data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_income_support`</td>
<td>If the government is covering the salaries or providing direct cash payments, universal basic income, or similar, of people who lose their jobs or cannot work. (Includes payments to firms if explicitly linked to payroll/ salaries)</td>
<td>Ordinal Scale: 0 - no income support; 1 - government is replacing less than 50% of lost salary (or if a flat sum, it is less than 50% median salary); 2 - government is replacing more than 50% of lost salary (or if a flat sum, it is greater than 50% median salary); Blank - No data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_debt_relief`</td>
<td>If government. is freezing financial obligations (eg stopping loan repayments, preventing services like water from stopping, or banning evictions)</td>
<td>Ordinal Scale: 0 - No; 1 - Narrow relief, specific to one kind of contract; 2 - broad debt/contract relief</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_fiscal_measures`</td>
<td>Announced economic stimulus spending. Note: this column only records amount additional to previously announced spending</td>
<td>Monetary value in USD of fiscal stimuli, includes any spending or tax cuts NOT included in `npi_international_support`, `npi_healthcase_investment` or `npi_vaccine_investment`; 0 - no new spending that day; Blank - no data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_international_support`</td>
<td>Announced offers of Covid-19 related aid spending to other countries. Note: only record amount additional to previously announced spending</td>
<td>Monetary value in USD; 0 - no new spending that day; Blank - no data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_public_information`</td>
<td>Presence of public info campaigns</td>
<td>Ordinal<br/>0 -No COVID-19 public information campaign; 1 - public officials urging caution about COVID-19; 2 - coordinated public information campaign; Blank - No data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_testing_policy`</td>
<td>Who can get tested; Note: this records policies about testing for current infection (PCR tests) not testing for immunity (antibody test)</td>
<td>Ordinal Scale<br/>0 - No testing policy<br/>1 - only testing those who both (a) have symptoms, and (b) meet specific criteria (eg key workers, admitted to hospital, came into contact with a known case, returned from overseas)<br/>2 - testing of anyone showing COVID19 symptoms<br/>3 - open public testing (eg “drive through” testing available to asymptomatic people)<br/>Blank - No data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_contact_tracing`</td>
<td>Government policy on contact tracing after a positive diagnosis. Note: we are looking for policies that would identify all people potentially exposed to Covid-19; voluntary bluetooth apps are unlikely to achieve this</td>
<td>Ordinal Scale<br/>0 - No contact tracing<br/>1 - Limited contact tracing – not done for all cases<br/>2 - Comprehensive contact tracing –done for all cases</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_healthcare_investment`</td>
<td>Announced short term spending on healthcare system, eg hospitals, masks, etc. Note: only record amount additional to previously announced spending</td>
<td>Monetary value of new short-term spending on health in USD; 0 - No new investment on that day; Blank - No data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_vaccine_investment`</td>
<td>Announced public spending on Covid-19 vaccine development. Note: only record amount additional to previously announced spending</td>
<td>Monetary value in USD<br/>
0 - no new spending that day<br/>
Blank - no data</td>
<td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold">`npi_masks`</td>
<td>Mask policy in force in the country. </td>
<td>Ordinal Scale<br/>0 - No mask policy in place<br/>1 - Limited mask policy (eg in stores only) or limited enforcement<br/>2 - Widespread mask policy and/or strict enforcement<br/>Blank - No data</td>
<td>ACAPS + Manual</td>
</tr>
 
<tr>
<td style="font-weight:bold">total_cases</td>
<td>Total (cumulative) confirmed cases in the country, as published by ECDC</td>
<td>Integer number of cases</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">new_cases</td>
<td>Number of new cases since previous day as published by ECDC</td>
<td>Integer number of cases</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">total_deaths</td>
<td>Total (cumulative) confirmed deaths in the country, as published by ECDC</td>
<td>Integer number of deaths</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">new_deaths</td>
<td>Number of new deaths since previous day as published by ECDC</td>
<td>Integer number of deaths</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">total_cases_per_million</td>
<td>Total cases per mililon people</td>
<td>Float number of cases</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">new_cases_per_million</td>
<td>New cases per million people</td>
<td>Float number of cases</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">total_deaths_per_million</td>
<td>Total deaths per million people</td>
<td>Float number of deaths</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">new_deaths_per_million</td>
<td>New detahs per million people</td>
<td>Float number of deaths</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">total_tests</td>
<td>Total (cumulative) number of COVID-19 tests performed in the country </td>
<td>Integer number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">new_tests</td>
<td>Number of new COVID-19 tests performed in the country </td>
<td>Integer number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">total_tests_per_thousand</td>
<td>Total (cumulative) number of COVID-19 tests performed per 1000 people</td>
<td>Float number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">new_tests_per_thousand</td>
<td>Number of new COVID-19 tests performned per 1000 people</td>
<td>Float number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">days_since_first_case</td>
<td>Days since the first recorded case in the country</td>
<td>0 until the first case is recoded, then DATE - first_case_date in days</td>
<td>Derived</td>
</tr>
<tr>
<td style="font-weight:bold">days_since_first_death</td>
<td>Days since the first recorded death in the country</td>
<td>0 until the first death is recoded, then DATE - first_death_date in days</td>
<td>Derived</td>
</tr>

<tr>
<td style="font-weight:bold">Retail and Recreation</td>
<td>Mobility trends for places like restaurants, cafes, shopping centers, theme parks, museums, libraries, and movie theaters.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>
<tr>
<td style="font-weight:bold">Grocery and Pharmacy</td>
<td>Mobility trends for places like grocery markets, food warehouses, farmers markets, specialty food shops, drug stores, and pharmacies.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>
<tr>
<td style="font-weight:bold">Parks</td>
<td>Mobility trends for places like national parks, public beaches, marinas, dog parks, plazas, and public gardens</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>
<tr>
<td style="font-weight:bold">Transit Stations</td>
<td>Mobility trends for places like public transport hubs such as subway, bus, and train stations.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>
<tr>
<td style="font-weight:bold">Workplaces</td>
<td>Mobility trends for places of work.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>
<tr>
<td style="font-weight:bold">Residential</td>
<td>Mobility trends for places of residence</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>

<tr>
<td style="font-weight:bold">driving_mobility</td>
<td>Transport mobility trends for driving</td>
<td>% Change in routing requests since 13 January 2020</td>
<td>Apple Maps Mobility Trends Report</td>
</tr>
<tr>
<td style="font-weight:bold">transit_mobility</td>
<td>Mobility trends for places of residence</td>
<td>% Change in routing requests since 13 January 2020</td>
<td>Apple Maps Mobility Trends Report</td>
</tr>
<tr>
<td style="font-weight:bold">walking_mobility</td>
<td>Mobility trends for places of residence</td>
<td>% Change in routing requests since 13 January 2020</td>
<td>Apple Maps Mobility Trends Report</td>
</tr>

<tr>
<td style="font-weight:bold">excess_death_daily_avg</td>
<td>Daily average number of excess deaths</td>
<td>Float<br/> Original dataset provides weekly figure, we divide it by 7 to obtain daily average.<br/>Final caulculation is <i>((number of deaths in 2020) - (average number of deaths in past few years))/7</i> </td>
<td>The Economist excess mortality tracker / EuroStats</td>
</tr>
<tr>
<td style="font-weight:bold">weekly_excess_death</td>
<td>Number of excess deaths for the past week. Generally this is calculated as the number of deaths in a week in 2020 
 minus the average number of deaths that occured in the same week in the previous 5 years. There are, however, cases where the underlying data provider uses a slightly different calculation (for example fewer than 5 years for the baseline)</td>
<td>Taken as is from the source</td>
<td>The Economist excess mortality tracker / EuroStats</td>
</tr>

<tr>
<td style="font-weight:bold">Precipitation_Weighted_Daily_Average_mean</td>
<td>Average daily precipitation across the country, sampled in major cities and weighted by population</td>
<td>Precipitation flux in kg/m^2s (multiply by 3600 to get mm / hr)</td>
<td>UK Met Office + SimpleMaps</td>
</tr>
<tr>
<td style="font-weight:bold">Temperature_Weighted_Daily_Average_mean</td>
<td>Average daily temperature across the country, sampled in major cities and weighted by population</td>
<td>&deg; C (Degrees celcius)</td>
<td>UK Met Office + SimpleMaps</td>
</tr>
<tr>
<td style="font-weight:bold">Humidity_Weighted_Daily_Average_mean</td>
<td>Average daily humidify across the country, sampled in major cities and weighted by population</td>
<td>kg/kg (Kilograms of water vapour per kilogram of air)</td>
<td>UK Met Office + SimpleMaps</td>
</tr>
<tr>
<td style="font-weight:bold">SW_Weighted_Daily_Average_mean</td>
<td>Average daily short-wave radiation across the country, sampled in major cities and weighted by population</td>
<td>W/m^2 (Watts per square metre)</td>
<td>UK Met Office + SimpleMaps</td>
</tr>
<tr>
<td style="font-weight:bold">Wind_Speed_Weighted_Daily_Average_mean</td>
<td>Average daily wind speed across the country, sampled in major cities and weighted by population</td>
<td>m/s (Metres per second)</td>
<td>UK Met Office + SimpleMaps</td>
</tr>

<tr>
<td style="font-weight:bold">median_age</td>
<td>Median age of population</td>
<td>Float age</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold">hospital_beds (per 1000)</td>
<td>Number of hospital beds per 1000 people</td>
<td>Float</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">physicians (per 1000)</td>
<td>Number of physicians per 1000 people</td>
<td>Float</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">nurses (per 1000)</td>
<td>Number of nurses per 1000 people</td>
<td>Float</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">Smoking prevalence, total, ages 15+</td>
<td>Percent of people over 15 who smoke</td>
<td>Percentage</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">Mortality rate, adult, female (per 1,000 female adults)</td>
<td>Average mortality rate per 1000 female adults</td>
<td>Number of people per 1000 females</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">Mortality rate, adult, male (per 1,000 male adults)</td>
<td>Average mortality rate per 1000 male adults</td>
<td>Number of people per 1000 males</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">Population Density</td>
<td>Average Density of population over entire country</td>
<td>Number of people per square kilometre of land area</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">Population in Urban Agglomerations</td>
<td>Population living in urban areas</td>
<td>Number of people living in agglomerations consisting of over 1 million people</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">Population Female</td>
<td>Female population</td>
<td>Number of people</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">Population Male</td>
<td>Male population</td>
<td>Number of people</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">Population</td>
<td>Total population</td>
<td>Number of people</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold">Population of Compulsory School Age</td>
<td>Population that is of the age where school attendance is compulsory</td>
<td>Number of people</td>
<td>World Bank Data Bank</td>
</tr>

</tbody></table>

## Data sources
* [Oxford Government Response Tracker](https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker)
* [ACAPS #COVID19 Government Measures](https://www.acaps.org/covid19-government-measures-dataset)
* [Our World in Data](https://ourworldindata.org/coronavirus)
* [Google Mobility Report](https://www.google.com/covid19/mobility/data_documentation.html)
* [World Bank Data Bank](https://data.worldbank.org/)
* [The Economist excess mortality tracker](https://github.com/TheEconomist/covid-19-excess-deaths-tracker)
* [EUROSTAT](https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=demo_r_mweek3&lang=en)
* [Apple Maps Mobility Trends Reports](https://www.apple.com/covid19/mobility)
* [UK Met Office](https://www.metoffice.gov.uk/)
* [Simplemaps](https://simplemaps.com/world)
