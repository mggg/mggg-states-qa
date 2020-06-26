# ExtractTable

A combined script and `python` module for extracting tabular data for data 
science purposes. A user-friendly, lite wrapper of `geopandas`.

## Documentation
Documentation for the ExtractTable module can be found as docstrings. 
Run `import ExtractTable; help(ExtractTable)` to view documentation.

## Installation
```
$ git clone https://github.com/KeiferC/ExtractTable.git
$ cd ExtractTable
$ pip install -r requirements.txt
```

## Usage
### As a Script
```
usage: ExtractTable.py [-h] [-o OUTFILE] [-c COLUMN] [-v VALUE [VALUE ...]]
                       INFILE

Script to extract tabular data. 

If no outfile is specified, outputs plaintext to stdout.
If no column is specified, outputs filetype converted input. 
If no value is specified, outputs table indexed with given column (required).
If value and column are specified, outputs subtable indexed with given column
and containing only rows equal to given value(s).

supported input filetypes:
    .csv .geojson .shp .xlsx .zip

supported output filetypes:
    .bz2 .csv .geojson .gpkg .gzip .html .json .md .pkl .tex .xlsx .zip 
    all other extensions will contain output in plaintext

positional arguments:
  INFILE                name/path of input file of tabular data to read

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --output OUTFILE
                        name/path of output file for writing
  -c COLUMN, --column COLUMN
                        label of column to use as index for extracted table
  -v VALUE [VALUE ...], --value VALUE [VALUE ...]
                        value(s) of specified column in rows to extract

examples:
    
    python ExtractTable.py input.xlsx -c ID > output.csv; ls
    python ExtractTable.py foo.csv -o bar.csv -c "state fips" -v 01
    python ExtractTable.py input.csv -o ../output.csv -c Name -v "Rick Astley"
    python ExtractTable.py in.csv -o out.csv -c NUM -v 0 1 2 3
```

### As a Module
```
>>> import ExtractTable
>>> help(ExtractTable) # To display module documentation
```
