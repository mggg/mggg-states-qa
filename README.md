# California Precincts GeoData
Contains shapefiles and tabular election and demographics data of California
precincts.



# Contents
[Repo Structure](#repo-structure)

[Sources](#sources)

  - [Geographic Data](#geographic-data-/census/shp/)

  - [Demographics Data](#demographics-data-/census/tab/)
  
  - [Election Data](#election-data-/election/)


[Data Processing](#data-processing)

[Results](#results)

[Analysis](#analysis)

[Naming Reference](#naming-reference)



# Repo Structure 
```
.
├── README.md
├── analyses
├── counties
│   ├── alameda
│   |   ├── processed
│   |   │   ├── georeferenced
│   |   │   ├── shp
│   |   │   └── tab
│   |   ├── raw
│   |   │   ├── jpg
│   |   │   └── shp
│   |   └── results
|   ├── alpine
|   |   ├── processed
|   |   |   ├── georeferenced
|   ... ... ...
└── geodata
    ├── acs
    │   ├── shp
    │   └── tab
    ├── census
    │   ├── shp
    │   │   └── 2010
    │   └── tab
    │       └── 2010
    └── election
        └── 2016
            ├── federal
            └── state
```



# Sources
## Geographic Data `geodata/census/shp/`
### 2010 Decennial Census `/2010/` 
__`blocks.zip`:__ Shapefile of 2010 California census blocks

  - Retrieved June 2020 from the [National Historical Geographic Information System (NHGIS) database](https://data2.nhgis.org/)

__`bgs.zip`:__ Shapefile of 2010 California census block groups

  - Retrieved June 2020 from the [NHGIS database](https://data2.nhgis.org/)

__`counties.zip`:__ Shapefile of 2010 California counties

  - Retrieved June 2020 from the [NHGIS database](https://data2.nhgis.org/)

__`state.zip`:__ Shapefile of 2010 California state. 

  - Retrieved June 2020 from the [NHGIS database](https://data2.nhgis.org/)

### 2000 Decennial Census `/2000/`
Coming soon...


## Demographics Data `geodata/census/tab/`
### 2010 Decennial Census `/2010/`
__`blocks.zip`:__ Tabular demographics and VAP data of 2010 California census blocks

  - Retrieved June 2020 from the [National Historical Geographic Information System (NHGIS) database](https://data2.nhgis.org/)

__`bgs.zip`:__ Tabular CVAP data of 2010 California census block groups

  - Retrieved June 2020 from the [National Historical Geographic Information System (NHGIS) database](https://data2.nhgis.org/)


## Election Data `geodata/election/`
### 2016 United States Elections `/2016/`
__`/federal/president.zip`:__ Tabular California precinct-level data for the 2016 United States Presidential election

  - Retrieved June 20 from the [MIT Election Data and Science Lab (MEDSL) database](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LYWX3D)

  - California-specific data extracted with `‘state_postal = ND’` query

__`/federal/senate.zip`:__ Tabular California precinct-level data for the 2016 Senate elections

  - Retrieved June 20 from the [MEDSL database](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/NLTQAD)

  - California-specific data extracted with `‘state_postal = ND’` query

__`/federal/house.zip`:__ Tabular California precinct-level data for the 2016 House elections

  - Retrieved June 20 from the [MEDSL database](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PSKDUJ)

  - California-specific data extracted with `‘state_postal = ND’` query

__`/state/state.zip`:__ Tabular California precinct-level data for 2016 state elections

  - Retrieved June 20 from the [MEDSL database](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GSZG1O)

  - California-specific data extracted with `‘state_postal = ND’` query






# Data Processing 
### County Metadata
Number of precincts and precinct names were retrieved June 2020 from...

### Digitization of Precinct Maps
Raster maps from the county's website were georeferenced in QGIS and then
used to outline precinct boundaries around which census blocks were geographically merged. All maps were projected in `EPSG:...` (NAD83/UTM zone __)

### Data Joining
Shapefile and tabular data joins were done using python. The documented script can be found in the Jupyter Notebook `...`

### GeoData Aggregation
Census-block-level demographics geodata were aggregated into precinct-level election geodata using the python `maup` package. The documented script can be found in the Jupyter Notebook `...`



# Results
### Alameda County (`counties/alameda/results/`)
- `alameda_precincts.zip`

- `alameda_blocks.zip`



# Analysis
More detailed analyses can be found in `analyses/`.

> Note: Because of the immigration history and the election requirements of the United States, not all in the Hispanic voting age population (HVAP) nor all in the Asian voting age population (ASIANVAP) are citizens. Consequentially, not all in the HVAP nor in the ASIANVAP are permitted to vote in United States federal elections. Therefore, any ecological regression (ER) or ecological inference (EI) analyses using HVAP or ASIANVAP lack statistical accuracy. It is better to use HCVAP and ASIANCVAP for analysis purposes.



# Naming Reference
The columns names used in the geodata follow the [Metric Geometry and Gerrymandering Group (MGGG)](https://mggg.org) naming conventions.

## Election Data
### Presidential Election
- `PRES16C`: Votes for the Constitution candidate in the 2016 United States Presidential Election

- `PRES16D`: Votes for the Democratic candidate in the 2016 United States Presidential Election

- `PRES16R`: Votes for the Republican candidate in the 2016 United States Presidential  Election

- `PRES16L`: Votes for the Libertarian candidate in the 2016 United States Presidential Election

- `PRES16G`: Votes for the Green candidate in the 2016 United States Presidential Election

### Senate Election
Coming soon...

### House Election
Coming soon...

### Gubernatorial Election
Coming soon...


## Demographics Data
### Population Data 
- `TOTPOP` (H7Z001): Total population

- `NH_WHITE` (H7Z003): White, non-Hispanic alone population

- `NH_BLACK` (H7Z004): Black, non-Hispanic alone population

- `NH_AMIN` (H7Z005): American Indian and Alaska Native, non-Hispanic alone population

- `NH_ASIAN` (H7Z006): Asian, non-Hispanic alone population

- `NH_NHPI` (H7Z007): Native Hawaiian and Pacific Islander, non-Hispanic alone population

- `NH_OTHER` (H7Z008): Other race, non-Hispanic alone population

- `NH_2MORE` (H7Z009): Non-Hispanic population of two or more races

- `HISP` (H7Z010): Total Hispanic/Latino population

- `H_WHITE` (H7Z011): White, Hispanic alone population

- `H_BLACK` (H7Z012): Black, Hispanic alone population

- `H_AMIN` (H7Z013): American Indian and Alaska Native, Hispanic alone population

- `H_ASIAN` (H7Z014): Asian, Hispanic alone population

- `H_NHPI` (H7Z015): Native Hawaiian and Pacific Islander, Hispanic alone population

- `H_OTHER` (H7Z016): Other race, Hispanic alone population

- `H_2MORE` (H7Z017): Hispanic population of two or more races

### Voting Age Population (VAP) Data
- `VAP` (H75001): Total voting age population

- `HVAP` (H75002): Hispanic voting age population

- `WVAP` (H75005): White, non-Hispanic voting age population

- `BVAP` (H75006): Black, non-Hispanic voting age population

- `AMINVAP` (H75007): American Indian and Alaska Native, non-Hispanic voting age population

- `ASIANVAP` (H75008): Asian, non-Hispanic voting age population

- `NHPIVAP` (H75009): Native Hawaiian and Pacific Islander, non-Hispanic voting age population

- `OTHERVAP` (H75010): Other race, non-Hispanic voting age population

- `2MOREVAP` (H75011): Voting age population of two or more races

### Citizen Voting Age Population (CVAP) Data
Coming soon...
