# DELVE COVID19 Dataset Access

This repository provides a data set for COVID19 research consolidated from multiple sources.
Code is provided for easily accessing both the combined and underlying data sets.

Usage examples are given in this [Jupyter notebook](./usage_examples.ipynb).

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
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend; 2 - Required <br/>+ binary for geographic scope <br/>0 - Targeted;  1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Workplace closing</td>
<td>Closing of work places</td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend; 2 - Required <br/>+ binary for geographic scope <br/>0 - Targeted;  1- General</td>
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
<td style="font-weight:bold">Close public transport</td>
<td>Closing of public transport<br/></td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend; 2 - Required <br/>+ binary for geographic scope <br/>0 - Targeted;  1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Public information campaigns</td>
<td>Presence of public info campaigns</td>
<td>Binary<br/>0 -No COVID-19 public information campaign; 1 - COVID-19 public information campaign<br/>+ binary for geographic scope<br/>0 - Targeted; 1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">Restrictions on internal movement</td>
<td>Restrictions on internal movement</td>
<td>Ordinal scale <br/>0 - No measures; 1 - Recommend; 2 - Required <br/>+ binary for geographic scope <br/>0 - Targeted;  1- General</td>
<td>Oxford Government Response Tracker</td>
<td>Y</td>
</tr>
<tr>
<td style="font-weight:bold">International travel controls</td>
<td>Restrictions on international travel</td>
<td>Ordinal Scale:<br/>0 - No measures; 1 - Screening; 2 - Quarantine on high-risk regions; 3 - Ban on high-risk regions</td>
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
<td style="font-weight:bold">Monetary measures</td>
<td>What monetary policy interventions are in place?</td>
<td>Value of interest rate in %</td>
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
<td>Percent of total population living in agglomerations consisting of over 1 million people</td>
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
</tbody></table>

