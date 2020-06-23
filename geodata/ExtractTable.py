__doc__ = '''
ExtractTable
============

Provides
    1. A python class used to extract tabular data by column and value
    2. Table rotation (if `VALUE` is not specified)
    3. A command-line script to run the class' extract function

Metadata
--------
filename:       ExtractTable.py
author:         @KeiferC
date:           23 June 2020
version:        0.0.1
description:    Script to extract tabular data by column to a CSV
dependencies:   geopandas
                matplotlib
                maup
                numpy
                pandas

Documentation
-------------
Documentation for the ExtractTable module can be found as docstrings in the
source code. 

Usage
-----
```
ExtractTable.py [-h] [-v VALUE] [-o OUTFILE] -c COLUMN INFILE

script to extract tabular data by column to a CSV

positional arguments:
    INFILE                path to file from which to extract data

optional arguments:
-h, --help            show this help message and exit
-v VALUE, --value VALUE
                        value to use as filter for extraction
-o OUTFILE, --output OUTFILE
                        path to output extracted table

required arguments:
-c COLUMN, --column COLUMN
                        column name with value to extract and to become new
                        index

examples:

    python ExtractTable.py input.xlsx -c ID > output.csv
    python ExtractTable.py foo.csv -o bar.csv -c "state fips" -v 01
    python Extract.py input.csv -o ../output.csv -c Name -v "Rick Astley"

```
'''

import argparse
import geopandas as gpd
import matplotlib.pyplot as plt
import maup
import numpy as np
import os.path
import pandas as pd
import sys
import zipfile

import warnings; warnings.filterwarnings(
    'ignore', 'GeoSeries.isna', UserWarning)



#########################################
# Class Definition                      #
#########################################
class ExtractTable:
    '''
    Class for extracting tabular data 

    Attributes
    ----------
    infile : str
        Path to tabular data file containing tables to extract
    outfile : str | None
        Path to output csv file containing extracted table. Defaults to stdout
    colname : str
        Name of column in source table to use as index for extracted table
    filterval : str | None
        Value in column in source table to use as filter for extracting 
        subtable. If not specified, output file is a rotated table
    
    Class Methods
    -------------
    read_file(self, filename, colname=None, filterval=None)
        Returns an ExtractTable instance with a specified input filename

    Instance Methods
    ----------------
    infile()
        Returns a string representing the input file's path
    infile(filename)
        Given a string representing the input file's path, sets the `infile` 
        attribute of the instance
    outfile()
        Returns a string representing the output file's path
    outfile(filename=None)
        Given a string representing the output file's path, sets the `outfile`
        attribute of the instance
    colname()
        Returns a string representing the name of the column to use as the 
        extracted table's index
    colname(colname)
        Given a string representing the name of the column to use as the 
        extracted table's index, sets the `colname` attribute of the instance
    filterval()
        Returns a string representing the value to use for filtering the 
        extracted table data
    filterval(filterval)
        Given a string representing the value to use for filtering the 
        extracted table data, sets the `filterval` attribute of the instance
    '''


    #--------------------------------
    # Constructors                  
    #--------------------------------
    def __init__(self, 
                infile=None, 
                outfile=None, 
                colname=None, 
                filterval=None):
        self.__infile = None
        self.__outfile = None
        self.__colname = None
        self.__filterval = None
        
        # Input sanitation
        self.infile(infile)
        self.outfile(outfile)
        self.colname(colname)
        self.filterval(filterval)
    
    @classmethod
    def read_file(self, filename, colname=None, filterval=None):
        '''
        Returns an ExtractTable instance with a specified input filename

        Parameters
        ----------
        filename : str
            Input file to read
        colname : str | None
            Column to use as index for extracted table
        filterval : str | None
            Value to use as filter for extracted table

        Returns
        -------
        ExtractTable
        '''

        return self(filename, None, colname, filterval)
    

    #--------------------------------
    # Getters and Setters                 
    #--------------------------------
    @property
    def infile(self):
        '''
        `infile` getter

        Parameters
        ----------
        None

        Returns
        -------
        str | None
        '''

        return self.__infile


    @infile.setter
    def infile(self, filename):
        '''
        `infile` setter

        Parameters
        ----------
        filename : str
            input file path
        
        Returns
        -------
        None
        '''

        filename_clean = filename

        # TODO

        self.__infile = filename_clean


    @property
    def outfile(self):
        '''
        `outfile` getter

        Parameters
        ----------
        None

        Returns
        -------
        str | None
        '''

        return self.__outfile


    @outfile.setter
    def outfile(self, filename=None):
        '''
        `outfile` setter. Defaults to stdout with null filename

        Parameters
        ----------
        filename : str
            output file path
        
        Returns
        -------
        None
        ''' 

        filename_clean = filename

        # TODO

        self.__outfile = filename_clean


    @property
    def colname(self):
        '''
        `colname` getter

        Parameters
        ----------
        None

        Returns
        -------
        str | None
        '''

        return self.__colname


    @colname.setter
    def colname(self, colname):
        '''
        `colname` setter

        Parameters
        ----------
        colname : str
            name of column to use as index for extracted table
        
        Returns
        -------
        None
        ''' 
        colname_clean = colname

        # TODO

        self.__colname = colname_clean
    

    @property
    def filterval(self):
        '''
        `filterval` getter

        Parameters
        ----------
        None

        Returns
        -------
        str | None
        '''

        return self.__filterval


    @filterval.setter
    def filterval(self, filterval):
        '''
        `colname` setter

        Parameters
        ----------
        filterval : str
            value to use as filter for extracted table
        
        Returns
        -------
        None
        ''' 

        filterval_clean = filterval

        # TODO

        self.__filterval = filterval_clean


    #--------------------------------
    # Method Definitions                
    #--------------------------------
    #### File Reading



#########################################
# Command-Line Parsing                  #
#########################################
def parse_arguments():
    '''
    Parses command-line arguments and returns a dictionary of argument objects

    Parameters
    ----------
    None

    Returns
    -------
    An argparse Namespace object
    '''

    description = 'script to extract tabular data by column as a CSV'
    infile_help = 'path to file from which to extract data'
    colname_help = 'column name with value to extract and to become new index'
    filterval_help = 'value to use as filter for extraction'
    outfile_help = 'path to output extracted table'
    
    examples = \
'''
examples:
    
    python ExtractTable.py input.xlsx -c ID > output.csv
    python ExtractTable.py foo.csv -o bar.csv -c "state fips" -v 01
    python ExtractTable.py input.csv -o ../output.csv -c Name -v "Rick Astley"
    
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
            '-v', 
            '--value', 
            dest='filterval',
            metavar='VALUE', 
            type=str, 
            help=filterval_help)
    parser.add_argument(
            '-o', 
            '--output', 
            dest='outfile',
            metavar='OUTFILE', 
            type=str, 
            help=outfile_help)
    
    required = parser.add_argument_group('required arguments')
    required.add_argument(
                '-c', 
                '--column', 
                dest='colname', 
                metavar='COLUMN', 
                type=str, 
                required=True,
                help=colname_help)

    return parser.parse_args()


#########################################
# Main                                  #
#########################################
def main():
    '''
    Validates input, parses command-line arguments, runs program.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    args = parse_arguments()

    # TODO

    sys.exit()


#########################################
# Function Calls                        #
#########################################
if __name__ == "__main__":
        main()