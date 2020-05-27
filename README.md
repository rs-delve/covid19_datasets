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
 <td style="font-weight:bold"><b>country_name</b></td>
 <td>Name of country</td>
 <td>English name according to ISO</td>
 <td></td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_school_closing</b></td>
 <td>Closing of schools and universities.</td>
 <td>Ordinal scale <br/>0 - No measures<br/> 1 - Recommend<br/> 2 - Require closing (only some levels or categories,
eg just high school, or just public schools)<br/> 3 - Require closing all levels<br/> Blank - No data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_workplace_closing</b></td>
 <td>Closing of work places</td>
 <td>Ordinal scale <br/>0 - No measures<br/> 1 - Recommend<br/> 2 - require closing (or work from home) for some sectors or categories of workers<br/> 3 - require closing (or work from home) all but essential workplaces (eg grocery stores, doctors)<br/> Blank - no data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_cancel_public_events</b></td>
 <td>Cancellation of public events<br/></td>
 <td>Ordinal scale <br/>0 - No measures<br/> 1 - Recommend<br/> 2 - Required<br/> Blank - no data </td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_gatherings_restrictions</b></td>
 <td>Limits on private gatherings</td>
 <td>Ordinal scale <br/>0 - No restrictions<br/>
1 - Restrictions on very large gatherings (the limit is above 1000 people)<br/> 2 - Restrictions on gatherings between 100-1000 people<br/> 3 - Restrictions on gatherings between 10-100 people<br/> 4 - Restrictions on gatherings of less than 10 people<br/> Blank - No data</td>
 <td>Oxford Government Response Tracker</td>
</tr>  
<tr>
 <td style="font-weight:bold"><b>npi_close_public_transport</b></td>
 <td>Closing of public transport<br/></td>
 <td>Ordinal scale <br/>0 - No measures<br/> 1 - Recommend closing (or significantly reduce volume/route/means of transport available)<br/> 2 - Require closing (or prohibit most citizens from using it)<br/> Blank - No data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_stay_at_home</b></td>
 <td>Recommendations or requirements for citizens to remain in their homes</td>
 <td>0 - No measures<br/> 1 - recommend not leaving house<br/> 2 - require not leaving house with exceptions for daily exercise, grocery shopping, and ‘essential’ trips<br/> 3 - Require not leaving house with minimal exceptions (e.g. allowed to leave only once every few days, or only one person can leave at a time, etc.)<br/> Blank - No data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_internal_movement_restrictions</b></td>
 <td>Restrictions on internal movement between cities/regions</td>
 <td>Ordinal scale <br/>0 - No measures<br/> 1 - Recommend closing (or significantly reduce volume/route/means of transport)<br/> 2 - Require closing (or prohibit most people from using it)<br/> Blank - No data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_international_travel_controls</b></td>
 <td>Restrictions on international travel. Note: this records policy for foreign travellers, not citizens</td>
 <td>Ordinal Scale:<br/>0 - No restrictions<br/> 1 - Screening arrivals<br/> 2 - Quarantine on arrival from some or all regions<br/> 3 - Ban on arrival from some regions<br/> 4 - Total border closure<br/> Blank - No data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_income_support</b></td>
 <td>If the government is covering the salaries or providing direct cash payments, universal basic income, or similar, of people who lose their jobs or cannot work. (Includes payments to firms if explicitly linked to payroll/ salaries)</td>
 <td>Ordinal Scale: <br/>0 - no income support<br/> 1 - government is replacing less than 50% of lost salary (or if a flat sum, it is less than 50% median salary)<br/> 2 - government is replacing more than 50% of lost salary (or if a flat sum, it is greater than 50% median salary)<br/> Blank - No data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_debt_relief</b></td>
 <td>If government. is freezing financial obligations (eg stopping loan repayments, preventing services like water from stopping, or banning evictions)</td>
 <td>Ordinal Scale:<br/> 0 - No<br/> 1 - Narrow relief, specific to one kind of contract<br/> 2 - broad debt/contract relief</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_fiscal_measures</b></td>
 <td>Announced economic stimulus spending. Note: this column only records amount additional to previously announced spending</td>
 <td>Monetary value in USD of fiscal stimuli, includes any spending or tax cuts NOT included in <i>npi_international_support</i>, <i>npi_healthcase_investment</i> or <i>npi_vaccine_investment</i><br/> 0 - no new spending that day; Blank - no data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_international_support</b></td>
 <td>Announced offers of Covid-19 related aid spending to other countries. Note: only record amount additional to previously announced spending</td>
 <td>Monetary value in USD<br/> 0 - no new spending that day<br/> Blank - no data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_public_information</b></td>
 <td>Presence of public info campaigns</td>
 <td>Ordinal<br/>0 -No COVID-19 public information campaign<br/> 1 - public officials urging caution about COVID-19<br/> 2 - coordinated public information campaign<br/> Blank - No data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_testing_policy</b></td>
 <td>Who can get tested; Note: this records policies about testing for current infection (PCR tests) not testing for immunity (antibody test)</td>
 <td>Ordinal Scale<br/>0 - No testing policy<br/>1 - only testing those who both (a) have symptoms, and (b) meet specific criteria (eg key workers, admitted to hospital, came into contact with a known case, returned from overseas)<br/>2 - testing of anyone showing COVID19 symptoms<br/>3 - open public testing (eg “drive through” testing available to asymptomatic people)<br/>Blank - No data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_contact_tracing</b></td>
 <td>Government policy on contact tracing after a positive diagnosis. Note: we are looking for policies that would identify all people potentially exposed to Covid-19; voluntary bluetooth apps are unlikely to achieve this</td>
 <td>Ordinal Scale<br/>0 - No contact tracing<br/>1 - Limited contact tracing – not done for all cases<br/>2 - Comprehensive contact tracing –done for all cases</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_healthcare_investment</b></td>
 <td>Announced short term spending on healthcare system, eg hospitals, masks, etc. Note: only record amount additional to previously announced spending</td>
 <td>Monetary value of new short-term spending on health in USD<br/> 0 - No new investment on that day<br/> Blank - No data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
<td style="font-weight:bold"><b>npi_vaccine_investment</b></td>
 <td>Announced public spending on Covid-19 vaccine development. Note: only record amount additional to previously announced spending</td>
 <td>Monetary value in USD<br/>
0 - no new spending that day<br/>
Blank - no data</td>
 <td>Oxford Government Response Tracker</td>
</tr>
<tr>
 <td style="font-weight:bold"><b>npi_masks</b></td>
 <td>Mask policy in force in the country. </td>
 <td>Ordinal Scale<br/>0 - No mask policy in place<br/>1 - Limited mask policy (eg in stores only) or limited enforcement<br/>2 - Widespread mask policy and/or strict enforcement<br/>Blank - No data</td>
 <td>ACAPS + Manual</td>
</tr>
 
<tr>
<td style="font-weight:bold"><b>cases_total</b></td>
<td>Total (cumulative) confirmed cases in the country, as published by ECDC.</td>
<td>Integer number of cases</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>cases_new</b></td>
<td>Number of new cases since previous day as published by ECDC</td>
<td>Integer number of cases</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>deaths_total</b></td>
<td>Total (cumulative) confirmed deaths in the country, as published by ECDC</td>
<td>Integer number of deaths</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>deaths_new</b></td>
<td>Number of new deaths since previous day as published by ECDC</td>
<td>Integer number of deaths</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>cases_total_per_million</b></td>
<td>Total cases per mililon people</td>
<td>Float number of cases</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>cases_new_per_million</b></td>
<td>New cases per million people</td>
<td>Float number of cases</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>deaths_total_per_million</b></td>
<td>Total deaths per million people</td>
<td>Float number of deaths</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>deaths_new_per_million</b></td>
<td>New deaths per million people</td>
<td>Float number of deaths</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>tests_total</b></td>
<td>Total (cumulative) number of COVID-19 tests performed in the country </td>
<td>Integer number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>tests_new</b></td>
<td>Number of new COVID-19 tests performed in the country </td>
<td>Integer number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>tests_total_per_thousand</b></td>
<td>Total (cumulative) number of COVID-19 tests performed per 1000 people</td>
<td>Float number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>tests_new_per_thousand</b></td>
<td>Number of new COVID-19 tests performned per 1000 people</td>
<td>Float number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>tests_new_smoothed</b></td>
<td>New tests for COVID-19 (7-day smoothed). For countries that don't report testing data on a daily basis, we assume that testing changed equally on a daily basis over any periods in which no data was reported. This produces a complete series of daily figures, which is then averaged over a rolling 7-day window</td>
<td>Float number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>tests_new_smoothed_per_thousand</b></td>
<td><i>tests_new_smoothed</i> per 1000 people</td>
<td>Float number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>stats_population</b></td>
<td>Population in 2020 as per United Nations, Department of Economic and Social Affairs, Population Division, World Population Prospects: The 2019 Revision</td>
<td>Float number of tests</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>stats_population_density</b></td>
<td>Population Density as estimated by World Bank</td>
<td>Number of people divided by land area, measured in square kilometers, most recent year available</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>stats_median_age</b></td>
<td>Median age of the population, UN projection for 2020</td>
<td>Float, median age in country</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>stats_gdp_per_capita</b></td>
<td>Gross domestic product at purchasing power parity as estimated by World Bank International Comparison Program database</td>
<td>GDP using constant 2011 international dollars, most recent year available</td>
<td>Our World in Data</td>
</tr>
<tr>
<td style="font-weight:bold"><b>cases_days_since_first</b></td>
<td>Days since the first recorded case in the country</td>
<td>0 until the first case is recoded, then DATE - first_case_date in days</td>
<td>Derived</td>
</tr>
<tr>
<td style="font-weight:bold"><b>deaths_days_since_first</b></td>
<td>Days since the first recorded death in the country</td>
<td>0 until the first death is recoded, then DATE - first_death_date in days</td>
<td>Derived</td>
</tr>
<tr>
<td style="font-weight:bold"><b>mobility_retail_recreation</b></td>
<td>Mobility trends for places like restaurants, cafes, shopping centers, theme parks, museums, libraries, and movie theaters.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>
<tr>
<td style="font-weight:bold"><b>mobility_grocery_pharmacy</b></td>
<td>Mobility trends for places like grocery markets, food warehouses, farmers markets, specialty food shops, drug stores, and pharmacies.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>
<tr>
<td style="font-weight:bold"><b>mobility_parks</b></td>
<td>Mobility trends for places like national parks, public beaches, marinas, dog parks, plazas, and public gardens</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>
<tr>
<td style="font-weight:bold"><b>mobility_transit_stations</b></td>
<td>Mobility trends for places like public transport hubs such as subway, bus, and train stations.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>
<tr>
<td style="font-weight:bold"><b>mobility_workplaces</b></td>
<td>Mobility trends for places of work.</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>
<tr>
<td style="font-weight:bold"><b>mobility_residential</b></td>
<td>Mobility trends for places of residence</td>
<td>% Relative to baseline (median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020.)</td>
<td>Google Mobility Report</td>
</tr>

<tr>
<td style="font-weight:bold"><b>mobility_travel_driving</b></td>
<td>Transport mobility trends for driving</td>
<td>% Change in routing requests since 13 January 2020</td>
<td>Apple Maps Mobility Trends Report</td>
</tr>
<tr>
<td style="font-weight:bold"><b>mobility_travel_transit</b></td>
<td>Mobility trends for places of residence</td>
<td>% Change in routing requests since 13 January 2020</td>
<td>Apple Maps Mobility Trends Report</td>
</tr>
<tr>
<td style="font-weight:bold"><b>mobility_travel_walking</b></td>
<td>Mobility trends for places of residence</td>
<td>% Change in routing requests since 13 January 2020</td>
<td>Apple Maps Mobility Trends Report</td>
</tr>

<tr>
<td style="font-weight:bold"><b>stats_hospital_beds_per_1000</b></td>
<td>Number of hospital beds per 1000 people</td>
<td>Float</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold"><b>stats_smoking</b></td>
<td>Percent of people over 15 who smoke</td>
<td>Float</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold"><b>stats_population_urban</b></td>
<td>Population living in urban areas</td>
<td>Number of people living in agglomerations consisting of over 1 million people, latest date available. Note that the source is different from <i>population</i> (which is a UN projection) and so this value may not be directly comparable to <i>population</i></td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold"><b>stats_population_school_age</b></td>
<td>Population that is of the age where school attendance is compulsory, latest date available. Note that the source is different from <i>population</i> (which is a UN projection) and so this value may not be directly comparable to <i>population</i></td>
<td>Number of people</td>
<td>World Bank Data Bank</td>
</tr>
<tr>
<td style="font-weight:bold"><b>deaths_excess_daily_avg</b></td>
<td>Daily average number of excess deaths</td>
<td>Float<br/>Weekly excess deaths divided by 7 to obtain daily average.<br/>Final caulculation is <i>((number of deaths in 2020) - (average number of deaths in past 5 years))/7</i> </td>
<td>Derived from Human Mortality Database / The Economist excess mortality tracker / EuroStats</td>
</tr>
<tr>
<td style="font-weight:bold"><b>deaths_excess_weekly</b></td>
<td>Number of excess deaths for the past week.</td>
<td> Number of deaths in a week in 2020 minus the average number of deaths that occured in the same week in the previous 5 years. We perform this calculation ourselves for consistency where weekly mortality data are available. There are, however, cases where the underlying mortality data is not available and the excess deaths is calculated by the provider using a different method (for example fewer than 5 years for the baseline)</td>
<td>Derived from Human Mortality Database / The Economist excess mortality tracker / EuroStats</td>
</tr>

<tr>
<td style="font-weight:bold"><b>weather_precipitation_mean</b></td>
<td>Average daily precipitation across the country, sampled in major cities and weighted by population</td>
<td>Precipitation flux in kg/m^2s (multiply by 3600 to get mm / hr)</td>
<td>UK Met Office + SimpleMaps</td>
</tr>
<tr>
<td style="font-weight:bold"><b>weather_humidity_mean</b></td>
<td>Average daily humidify across the country, sampled in major cities and weighted by population</td>
<td>kg/kg (Kilograms of water vapour per kilogram of air)</td>
<td>UK Met Office + SimpleMaps</td>
</tr>
<tr>
<td style="font-weight:bold"><b>weather_sw_radiation_mean</b></td>
<td>Average daily short-wave radiation across the country, sampled in major cities and weighted by population</td>
<td>W/m^2 (Watts per square metre)</td>
<td>UK Met Office + SimpleMaps</td>
</tr>
<tr>
<td style="font-weight:bold"><b>weather_temperature_mean</b></td>
<td>Average daily temperature across the country, sampled in major cities and weighted by population</td>
<td>&deg; C (Degrees celcius)</td>
<td>UK Met Office + SimpleMaps</td>
</tr>
<tr>
<td style="font-weight:bold"><b>weather_wind_speed_mean</b></td>
<td>Average daily wind speed across the country, sampled in major cities and weighted by population</td>
<td>m/s (Metres per second)</td>
<td>UK Met Office + SimpleMaps</td>
</tr>
</tbody></table>

## Data sources
* [Oxford Government Response Tracker](https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker)
* [ACAPS #COVID19 Government Measures](https://www.acaps.org/covid19-government-measures-dataset)
* [Our World in Data](https://ourworldindata.org/coronavirus)
* [Google Mobility Report](https://www.google.com/covid19/mobility/data_documentation.html)
* [World Bank Data Bank](https://data.worldbank.org/)
* [Human Mortality Database](https://www.mortality.org/)
* [The Economist excess mortality tracker](https://github.com/TheEconomist/covid-19-excess-deaths-tracker)
* [EUROSTAT](https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=demo_r_mweek3&lang=en)
* [Apple Maps Mobility Trends Reports](https://www.apple.com/covid19/mobility)
* [UK Met Office](https://www.metoffice.gov.uk/)
* [Simplemaps](https://simplemaps.com/world)
