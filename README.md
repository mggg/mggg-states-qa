# Geodata Utility Tools
[![Documentation Status](https://readthedocs.org/projects/gdutils/badge/?version=latest)](https://gdutils.readthedocs.io/en/latest/?badge=latest)

A collection of geodata utility tools. Still in development.

Available modules:

- `gdutils.datamine`: a `python` module for mining and listing data sources.
- `gdutils.dataqa`: a `python` module for comparing analyzing and comparing 
   data for QA purposes. Status: In development.
- `gdutils.extract`: a script and `python` module for extracting tabular 
   data for data science (data wrangling) purposes. A user-friendly, lite 
   wrapper of `geopandas` with the power of `pandas`.

## Installation
```bash
$ pip install git+https://github.com/KeiferC/gdutils.git
```

To uninstall, run `pip uninstall gdutils`.

## Documentation
Documentation can be found on [Read the Docs](https://gdutils.readthedocs.io/).
Additionally, documentation for modules can be found using the `python` 
`help()` function, e.g. `import gdutils.datamine; help(gdutils.datamine)`.



