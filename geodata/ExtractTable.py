'''
ExtractTable
============

Provides
    1. A python class used to extract subtables from given tabular data. 
       Can manage filetypes: csv, xlsx, geojson, shp
    2. A command-line script to run the class' extract function

Metadata
--------
filename:       ExtractTable.py
author:         @KeiferC
date:           23 June 2020
version:        0.0.1
description:    Script and module to extract subtables from given tabular data
dependencies:   geopandas
                numpy
                pandas

Documentation
-------------
Documentation for the ExtractTable module can be found as docstrings in the
source code. Run `help(ExtractTable)` to view documentation.

Usage
-----
usage: ExtractTable.py [-h] [-o OUTFILE] [-c COLUMN] [-v VALUE [VALUE ...]] 
                       INFILE

Script to extract tabular data to a csv. If no column is specified, 
returns the infile as a csv. If no value is specified, returns the 
infile as a csv where required specified column is the output's index. 
If both value and column are specified, returns a csv containing a 
subtable where the column is the index in which every row is equal to
the specified value.

positional arguments:
  INFILE                path to file from which to extract data

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --output OUTFILE
                        path to output extracted table
  -c COLUMN, --column COLUMN
                        column label to use as extracted index
  -v VALUE [VALUE ...], --value VALUE [VALUE ...]
                        value(s) in column to use as filter for extraction

examples:
    
    python ExtractTable.py input.xlsx -c ID > output.csv
    python ExtractTable.py foo.csv -o bar.csv -c "state fips" -v 01
    python ExtractTable.py input.csv -o ../output.csv -c Name -v "Rick Astley"
    python ExtractTable.py in.csv -o out.csv -c NUM -v 0 1 2 3
'''

import argparse
import geopandas as gpd
import numpy as np
import pandas as pd
import sys
from typing import List, NoReturn, Optional, Union

import warnings; warnings.filterwarnings(
    'ignore', 'GeoSeries.isna', UserWarning)



#########################################
# Class Definition                      #
#########################################
class ExtractTable:
    '''
    Class for extracting tabular data. Run `help(ExtractTable)` to view docs
    '''


    #--------------------------------
    # Constructors                  
    #--------------------------------
    def __init__(self, 
                infile:     Optional[str] = None, 
                outfile:    Optional[str] = None, 
                column:     Optional[str] = None, 
                value:      Union[str, List[str], None] = None):
        # Encapsulated attributes
        self.__infile =     None
        self.__outfile =    None
        self.__column =     None
        self.__value =      None

        # Protected attributes
        self.__table =      None
        self.__coldata =    None
        self.__foundval =   False
        self.__extracted =  None

        self.__sanitize_init(infile, outfile, column, value)


    @classmethod
    def read_file(self, 
                  filename: str, 
                  column:   Optional[str] = None, 
                  value:    Union[str, List[str], None] = None):
        '''
        Returns an ExtractTable instance with a specified input filename

        Parameters
        ----------
        filename : str
            Input file to read
        column : str | None
            Label of column to use as index for extracted table
        value : str | None
            Value to use as filter for extracted table

        Returns
        -------
        ExtractTable
        '''
        return self(filename, None, column, value)
    

    # Constructor input sanitation
    def __sanitize_init(self, 
                        infile:     Optional[str], 
                        outfile:    Optional[str], 
                        column:     Optional[str], 
                        value:      Union[str, List[str], None]):
        try:
            self.infile = infile
            self.outfile = outfile
            self.column = column
            self.value = value
        except Exception as e:
            raise AttributeError("Initialization failed. {}".format(e))


    #--------------------------------
    # Getters and Setters                 
    #--------------------------------
    @property
    def infile(self) -> str:
        '''
        {str} 
            Path to tabular data file containing tables to extract
        '''
        return self.__infile
    @infile.setter
    def infile(self, filename: Optional[str]) -> NoReturn:
        if filename:
            self.__table = gpd.read_file(filename)
            self.__infile = filename


    @property
    def outfile(self) -> Optional[str]:
        '''
        {str | None}
            Path to output csv file containing extracted table. 
            Defaults to stdout
        '''
        return self.__outfile
    @outfile.setter
    def outfile(self, filename: Optional[str] = None) -> NoReturn:
        self.__outfile = filename


    @property
    def column(self) -> str:
        '''
        {str}
            Name of column in source table to use as index for extracted table
        '''
        return self.__column
    @column.setter
    def column(self, column: Optional[str]) -> NoReturn:
        if column:
            try:
                self.__coldata = self.__table[column]
            except Exception as e:
                raise KeyError("Column not found: {}".format(e))
            self.__column = column


    @property
    def value(self) -> Union[str, List[str], None]:
        '''
        {str | List[str] | None}
            Value in column in source table to use as filter for extracting 
            subtable. If not specified, output file is a reindexed table
        '''
        return self.__value
    @value.setter
    def value(self, value: Union[str, List[str], None]) -> NoReturn:
        if value and (self.__table is None):
            raise KeyError("Cannot set value without specifying tabular data")
        elif value and (not self.column):
            raise KeyError("Cannot set value without specifying column")
        elif value:
            try: # value is a singleton
                self.__extracted = self.__table[
                                        self.__table[self.column] == value]
            except: # value is a list
                self.__extracted = self.__table[
                                        self.__table[self.column].isin(value)]

            if self.__extracted.empty:
                raise KeyError("Column '{}' has no value '{}'".format(
                                    self.column, value))
            else:
                self.__value = value
            

    #--------------------------------
    # Instance Methods               
    #--------------------------------
    def extract(self) -> gpd.GeoDataFrame:
        '''
        Returns a GeoPandas GeoDataFrame containing extracted subtable.

        Returns
        -------
        GeoDataFrame
        '''
        if self.__table is None:
            raise RuntimeError("Unable to find tabular data to extract")
        elif self.column:
            return self.__reindex()
        else:
            return self.__table
            

    def to_file(self, gdf: gpd.GeoDataFrame, filename: str) -> NoReturn:
        '''
        Given a GeoDataFrame and a filename string, writes the tabular
        data to a csv with the given filename.

        Parameters
        ----------
        gdf : gpd.GeoDataFrame
            Tabular data to write to file
        filename : str
            Path to which file is to be written
        '''
        pass # TODO

    # TODO: Column listing

    # TODO: unique value listing

    #--------------------------------
    # Helper Methods              
    #--------------------------------
    def __reindex(self) -> gpd.GeoDataFrame:
        if self.value:
            return self.__extracted.set_index(self.column)
        else:
            return self.__table.set_index(self.column)



#########################################
# Command-Line Parsing                  #
#########################################
def parse_arguments() -> argparse.Namespace:
    '''
    Parses command-line arguments and returns a dictionary of argument objects

    Returns
    -------
    An argparse Namespace object
    '''
    infile_help = 'path to file from which to extract data'
    column_help = 'column label to use as extracted index'
    value_help = 'value(s) in column to use as filter for extraction'
    outfile_help = 'path to output extracted table'

    description = \
'''
Script to extract tabular data to a csv. If no column is specified, 
returns the infile as a csv. If no value is specified, returns the 
infile as a csv where required specified column is the output's index. 
If both value and column are specified, returns a csv containing a 
subtable where the column is the index in which every row is equal to
the specified value.
'''
    
    examples = \
'''
examples:
    
    python ExtractTable.py input.xlsx -c ID > output.csv
    python ExtractTable.py foo.csv -o bar.csv -c "state fips" -v 01
    python ExtractTable.py input.csv -o ../output.csv -c Name -v "Rick Astley"
    python ExtractTable.py in.csv -o out.csv -c NUM -v 0 1 2 3
    
'''

    parser = argparse.ArgumentParser(
                description=description,
                epilog=examples,
                formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
                'infile',
                metavar='INFILE', 
                help=infile_help)
    parser.add_argument(
                '-o', 
                '--output', 
                dest='outfile',
                metavar='OUTFILE', 
                type=str, 
                help=outfile_help)
    parser.add_argument(
                '-c', 
                '--column', 
                dest='column', 
                metavar='COLUMN', 
                type=str, 
                help=column_help)
    parser.add_argument(
                '-v', 
                '--value', 
                dest='value',
                metavar='VALUE', 
                type=str,
                nargs='+',
                help=value_help)

    return parser.parse_args()



#########################################
# Main                                  #
#########################################
def main() -> NoReturn:
    '''
    Validates input, parses command-line arguments, runs program.
    '''
    args = parse_arguments()

    # TODO

    sys.exit()



#########################################
# Function Calls                        #
#########################################
if __name__ == "__main__":
    main()

