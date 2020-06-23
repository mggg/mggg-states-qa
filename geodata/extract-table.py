#
#   filename:       extract-table.py
#   author:         @KeiferC
#   date:           19 June 2020
#   version:        0.0.1
#   description:    Script to extract tabular data by column and value
#   dependencies:   geopandas
#                   matplotlib
#                   maup
#                   numpy
#                   pandas
#
#   usage: extract-table.py [-h] [-v VALUE] [-o OUTFILE] -c NAME INFILE
#
#   script to extract tabular data by column as a CSV
#
#   positional arguments:
#       INFILE                path to file from which to extract data
#
#   optional arguments:
#     -h, --help            show this help message and exit
#     -v VALUE, --value VALUE
#                           value to use as filter for extraction
#     -o OUTFILE, --output OUTFILE
#                           path to output extracted table
#
#   required arguments:
#     -c NAME, --column NAME
#                           column name with value to extract and to become new
#                           index
#
#   examples:
#
#      python extract-table.py input.xlsx -c ID > output.csv
#      python extract-table.py foo.csv -o bar.csv -c "state fips" -v 01
#      python extract-table.py input.csv -o ../output.csv -c Name -v "Rick Astley"
#

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
# Function Definitions                  #
#########################################


#########################################
# Command-Line Parsing                  #
#########################################
def parse_arguments():

    description = 'script to extract tabular data by column as a CSV'
    infile_help = 'path to file from which to extract data'
    colname_help = 'column name with value to extract and to become new index'
    filterval_help = 'value to use as filter for extraction'
    outfile_help = 'path to output extracted table'
    
    examples = \
'''
examples:
    
    python extract-table.py input.xlsx -c ID > output.csv
    python extract-table.py foo.csv -o bar.csv -c "state fips" -v 01
    python extract-table.py input.csv -o ../output.csv -c Name -v "Rick Astley"

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
                metavar='NAME', 
                type=str, 
                required=True,
                help=colname_help)

    return parser.parse_args()


#########################################
# File Reading                          #
#########################################



#########################################
# Function Calls                        #
#########################################
if __name__ == "__main__":
        main()
