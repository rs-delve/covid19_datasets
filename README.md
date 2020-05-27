# DELVE COVID-19 Dataset

This repository provides a data set for COVID-19 research consolidated from multiple sources. The dataset is available as CSV which can be loaded into most environments. We also provide Python code for accessing underlying datasets which in some cases provide more detail or finer resolution.

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

## Codebook
View the [Codebook](https://github.com/rs-delve/covid19_datasets/blob/master/dataset/codebook.md) for details of the fields available in the dataset

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
* [International Organization for Standardization](https://www.iso.org/home.html)
