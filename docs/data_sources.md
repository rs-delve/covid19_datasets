# Data Sources

| Provider | Provider's docs | Original Sources | Provider's Update Frequency | Our Update Frequency | Update Mechanism |
|----------|-----------------|------------------|-----------------------------|----------------------|------------------|
| [Oxford Government Response Tracker](https://www.bsg.ox.ac.uk/research/research-projects/coronavirus-government-response-tracker) | [Codebook](https://github.com/OxCGRT/covid-policy-tracker/blob/master/documentation/codebook.md) | "Data is collected from public sources by a team of over one hundred Oxford University students and staff from every part of the world.". The [original dataset](https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv) includes notes with links to these public sources | Updated continuously, with the aim of updating each country at least once a week | Latest Version | [Automatic](https://github.com/rs-delve/covid19_datasets/blob/master/covid19_datasets/oxford_government_policy.py) |
| [Our World in Data](https://ourworldindata.org/coronavirus-data) | [Codebook](https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data-codebook.md) | Cases and deaths come from [European Centre for Disease Prevention and Control](https://www.ecdc.europa.eu/en/covid-19-pandemic). Tests are collected by Our World in Data from [National Government Reports](https://ourworldindata.org/coronavirus-testing) | ECDC does [daily updates](https://www.ecdc.europa.eu/en/covid-19/data-collection) from worldwide health authority reports. They have a cut-off of 10 PM CET. Our World in Data updates their tests dataset twice a week | Latest Version | [Automatic](https://github.com/rs-delve/covid19_datasets/blob/master/covid19_datasets/our_world_in_data.py) |




