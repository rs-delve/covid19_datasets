# DELVE COVID-19 Dataset

> :warning: **This dataset is no longer being maintained.** Please see our data sources instead.

This repository provides a data set for COVID-19 research consolidated from multiple sources. The dataset is available as CSV which can be loaded into most environments. We also provide Python code for accessing underlying datasets which in some cases provide more detail or finer resolution.

## Reading the dataset
Download the CSV from the [dataset](https://github.com/rs-delve/covid19_datasets/tree/master/dataset) directory and load it in your favourite analysis tool. 

In Python you can load the CSV directly using [Pandas](https://pandas.pydata.org/):
```python
import pandas as pd
data_df = pd.read_csv('https://raw.githubusercontent.com/rs-delve/covid19_datasets/master/dataset/combined_dataset_latest.csv', parse_dates=['DATE'])
```

Or in R:
```R
X = read.csv(url("https://raw.githubusercontent.com/rs-delve/covid19_datasets/master/dataset/combined_dataset_latest.csv")) 
```

## Examples
We provide two Jupyter notebooks with examples:
- [Basic exploratory data analysis of the combined international dataset](./Data_Exploration.ipynb)
- [Usage of the underlying datasets](./usage_example.ipynb).

## Codebook
View the [Codebook](https://github.com/rs-delve/covid19_datasets/blob/master/docs/codebook.md) for details of the fields available in the dataset.

## Licence
This software is published under the MIT licence. The data generated are available under the Creative Commons Attribution 4.0 International License.

## Citation
We recommend citing the combined dataset as follows, noting the importance of including an access date, since the data may be retroactively updated over time.

```bibtex
@misc{DelveCovidDataset,
    title = {DELVE Global COVID-19 Dataset},
    howpublished= {\url{https://github.com/rs-delve/covid19_datasets/blob/master/dataset/combined_dataset_latest.csv}},
    note = {Accessed: <DATE ACCESSED>}
} 
```
  
We also recommend citing the original sources of any fields you use, these sources can be found in the [Codebook](https://github.com/rs-delve/covid19_datasets/blob/master/docs/codebook.md).

## Data sources
A full description of data sources, links to their documentation and update frequencies is available [here](https://github.com/rs-delve/covid19_datasets/blob/master/docs/data_sources.md).

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
