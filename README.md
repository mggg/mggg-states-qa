# ExtractTable

A combined script and `python` module for extracting tabular data for data 
science purposes. A user-friendly, lite wrapper of `geopandas`.

## Documentation
Documentation for the ExtractTable module can be found as docstrings. 
Run `import ExtractTable; help(ExtractTable)` to view documentation.

## Installation
```bash
$ git clone https://github.com/KeiferC/ExtractTable.git
$ cd ExtractTable
$ pip install -r requirements.txt
```

## Usage
### As a Script
```bash
$ python ExtractTable.py -h
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
```python
$ python
>>> from ExtractTable import ExtractTable
>>> help(ExtractTable) # To display class documentation
Help on class ExtractTable in module ExtractTable:

class ExtractTable(builtins.object)
 |  ExtractTable(infile: Union[str, NoneType] = None, outfile: Union[str, NoneType] = None, column: Union[str, NoneType] = None, value: Union[str, List[str], NoneType] = None)
 |  
 |  For extracting tabular data. Run `help(ExtractTable)` to view docs.
 | 
  
...

>>> help(ExtractTable.list_values) # To display instance method documentation
Help on function list_values in module ExtractTable:

list_values(self, column: Union[str, NoneType] = None, unique: Union[bool, NoneType] = False) -> Union[numpy.ndarray, geopandas.array.GeometryArray]
    Returns a list of values in the initialized column (default).
    
    Returns a list of values in the given column (if specified).
    Returns a list of unique values (if specified)

    Parameters
    ----------
    column : str | NoneType, optional
        Name of the column whose values are to be listed. If None,
        lists the values of the initialized column. Defaults to None
    unique : bool, optional
        If True, function lists only unique values. Defaults to False
    
    Returns
    -------
    np.ndarray | gpd.array.GeometryArray
    
    Raises
    ------
    RuntimeError
        Raised if trying to list values from non-existent tabular data
    KeyError
        Raised if column does not exist in tabular data
    RuntimeError
        Raised if trying to list values from non-existent column
    
    See Also
    --------
    list_columns() -> np.ndarray
    
    Examples
    --------
    >>> et = ExtractTable.read_file('input.csv', 'col2')
    >>> print(et.list_values)
    ['b' 'd' '3' '5' '10']
    >>> print(et.list_values('col1'))
    ['a' 'c' 'c' 'c' 'b']
    >>> print(et.list_values('col1', unique=True))
    ['a' 'c' 'b']
```
