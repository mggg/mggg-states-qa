# Geo/Election Data QA: `mggg-states`

Data quality assurance on `mggg-states`. The QA notebook does the following:

- Finds naming discrepancies in the `mggg-states` datasets
- Compares `mggg-states` vote counts with MEDSL vote counts at the State-level
- Compares `mggg-states` vote counts with Wikipedia vote counts at the
  State-level
- Returns State-level summations of the `mggg-states`, MEDSL, and Wikipedia
  datasets for spot checking and column datatype analysis
- Checks the `mggg-states` shapefiles for missing or empty geometries
- Provides next steps recommendations for further QA

The QA is isolated to United States federal elections between 2016 and 2018
(inclusive).


## Wikipedia Election Dataset

The Wikipedia Election Dataset was created through wrangling data scraped from
Wikipedia pages. The scraping and wrangling details can be found in the jupyter
notebook `src/wikipedia-election-data-mining.ipynb`. The dataset contains the
Democrat, Green, Libertarian, and Republican vote counts for the following
elections:

- 2016 United States presidential election
- 2016 United States Senate elections
- 2016 United States House of Representatives elections
- 2017 United States Senate elections (special elections)
- 2018 United States Senate elections
- 2018 United States House of Representatives elections

The data collection is timestamped at 10:00 AM ET, 14 Aug. 2020.

The columns are named according to the MGGG naming convention, which could
be found in `src/naming_convention.json`.

Limitations:

Write-in candidate votes are not counted towards to overall party vote count. In
the cases where elections have competing candidates of the same party, only the
winning candidate's vote is counted.
