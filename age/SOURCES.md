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
- Cases not available

### Processing Steps
- Convert cumulative counts to daily new counts
- Rescale data to match totals reported by ECDC.
  - This is to address the significant drop in totals in more recent data, likely due to reporting delays. We consider this to be a sample of the total cases and rescale it.
  
# Canada

### Source
[COVID-19 Canada Open Data Working Group](https://github.com/ishaberry/Covid19Canada)
- [Detailed line items on cases including age and sex](https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/cases.csv)
- [Detailed line items on deaths including age and sex](https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/mortality.csv)
We assume this to be an unbiased sample of the total cases and deaths from which we can derive an age and sex distribution

### Processing Steps
- Mapping to age ranges
- Derive "both sex" values by summing male and female
- Smoothing using a centered rolling 5 day window (to reduce the sample variance)
- Rescale to match totals reported by ECDC

# Chile

### Source
[Ministry of Science, Technology, Knowledge and Innovation](http://www.minciencia.gob.cl/COVID19)
Dataset Available on [Github](https://github.com/MinCiencia/Datos-COVID19)
- [Cases by age and sex](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto16/CasosGeneroEtario_std.csv)
- [Deaths by age only](https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario_std.csv)

### Processing Steps
- Convert cumulative counts to daily new counts
- **Cases only**: Derive "both sex" values by summing male and female
- **Cases only**: Convert periodic values to daily using linear interpolation

# Czechia

### Sources
[Minsitry of Health](https://www.mzcr.cz/) provides an [overview of current diseases](https://onemocneni-aktualne.mzcr.cz/)
- [Cases by age and sex](https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv)
- [Deaths by age and sex](https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.csv)

### Processing Steps
- Derive "both sex" values by summing male and female
- Convert periodic values to daily using linear interpolation

# Finland

### Sources
[Finnish Institute for Health and Welfare](https://thl.fi/en/web/thlfi-en) provides a [COVID-19 dashboard](https://experience.arcgis.com/experience/d40b2aaf08be4b9c8ec38de30b714f26)
- [Cases by age group](https://services7.arcgis.com/nuPvVz1HGGfa0Eh7/arcgis/rest/services/korona_tapauksia_jakauma/FeatureServer/0/query?f=json&where=1%3D1&outFields=OBJECTID,alue,date,tapauksia,miehia,naisia,Ika_0_9,ika_10_19,ika_20_29,ika_30_39,ika_40_49,ika_50_59,ika_60_69,ika_70_79,ika_80_,koodi&returnGeometry=false)
- Cases by sex 
- Death data not available

### Processing Steps
- Split cases by age group using total case by sex fractions
- Convert cumulative counts to daily new counts

# France
### Sources
[France Government Data](https://www.data.gouv.fr/fr/)
[Public Health France](https://www.santepubliquefrance.fr/) 
- [Cases by age and sex](https://www.data.gouv.fr/fr/datasets/r/57d44bd6-c9fd-424f-9a72-7834454f9e3c)
- [Deaths by age and sex as collected by INED](https://dc-covid.site.ined.fr/en/data/france/)

### Processing Steps
- **Cases only**: Map to age ranges

# Germany

### Sources
[Robert Koch Institute](https://www.rki.de/EN/Home/homepage_node.html) provides a [dashboard](https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4/page/page_0/) inluding cases and deaths by age and sex

### Processing Steps
- Derive "both sex" values by summing male and female

# India

### Sources
[COVID-19 India](https://www.covid19india.org/)
- [Detailed line items including cases and deaths with age and sex](https://api.covid19india.org/documentation/csv/)
We assume this to be an unbiased sample of the total cases and deaths from which we can derive an age and sex distribution

### Processing Steps
- Mapping to age ranges
- Derive "both sex" values by summing male and female
- Smoothing using a centered rolling 5 day window (to reduce the sample variance)
- Rescale to match totals reported by ECDC

# Italy

### Sources
[EpiCentro: Higher Institute of Health Epidemiology for public health](https://www.epicentro.iss.it/)
- [Cases by age and sex scraped from PDF reports](https://www.epicentro.iss.it/coronavirus/bollettino/Bollettino-sorveglianza-integrata-COVID-19_18-agosto-2020.pdf)
- [Deaths by age and sex as collected by INED](https://dc-covid.site.ined.fr/en/data/italy/)

### Processing Steps
- **Cases only**: Convert cumulative counts to daily new counts
- **Cases only**: Derive "both sex" values by summing male and female

# Korea

### Sources
[KCDC](http://www.cdc.go.kr/cdc_eng/)
- [Cases by age and sex provided in HTML reports](https://www.cdc.go.kr/board/board.es?mid=a30402000000&bid=0030)
- [Deaths by age and sex as collected by INED](https://dc-covid.site.ined.fr/en/data/korea/)

### Processing Steps
- **Cases only**: Convert cumulative counts to daily new counts. Note: The source has a mix of cumulative and new reporting before the 15th of April and is consistently new afterwards

# Mexico

### Sources





