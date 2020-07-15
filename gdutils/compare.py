"""
compare.py
==========

Provides
    - A python class, ``CompareTables`` for comparing geodata. Main use case
      is for data QA through comparing processed geodata with those from other
      sources (e.g. MEDSL)

Metadata
--------

:Filename:      `compare.py <https://github.com/keiferc/gdutils/>`_
:Author:        `@KeiferC <https://github.com/keiferc>`_
:Date:          15 July 2020
:Version:       0.0.1
:Description:   Module for comparing geodata tables for data QA purposes
:Dependencies:  

                - ``geopandas``
                - ``numpy``
                - ``gdutils.extract`

Documentation
-------------

Documentation for the ``compare`` module can be found as docstrings. 
Run ``import gdutils.compare; help(gdutils.compare)`` to view documentation.
::

    $ python
    >>> import gdutils.compare; help(gdutils.compare)

Additionally, documentation can be found on `Read the Docs 
<https://gdutils.readthedocs.io>`_.

"""
import geopandas as gpd
import numpy as np
import os.path
import pandas as pd
import pathlib
import sys

from typing import List, NoReturn, Optional, Tuple, Union
import warnings; warnings.filterwarnings(
    'ignore', 'GeoSeries.isna', UserWarning)

from gdutils.extract import ExtractTable as et



#########################################
#                                       #
#       Class Definition                #
#                                       #
#########################################

class CompareTables:
    """
    For comparing tabular data for data QA purposes. 
    Run ``help(CompareTables)`` to view docs.

    Attributes
    ----------
    table1 : Union[str, pd.DataFrame, gpd.GeoDataFrame]
        Name/path of input tabular data file or a pandas DataFrame or a 
        geopandas GeoDataFrame to compare
    table2 : Union[str, pd.DataFrame, gpd.GeoDataFrame]
        Name/path of input tabular data file or a pandas DataFrame or a 
        geopandas GeoDataFrame to compare
    columns1 : 
    columns2 :
    outfile : Optional[str, pathlib.Path]
        Name/path of output file for writing comparison results. Defaults
        to ``None``
    
    """

    #===========================================+
    # Constructors                              |
    #===========================================+

    def __init__(self,
                 table1:    Union[str, pd.DataFrame, gpd.GeoDataFrame],
                 table2:    Union[str, pd.DataFrame, gpd.GeoDataFrame],
                 outfile:   Optional[Union[str, pathlib.Path]] = None):
        """
        CompareTables initializer.

        Parameters
        ----------
        table1 : str | pd.DataFrame | gpd.GeoDataFrame
            Name/path of input tabular data file or a pandas DataFrame or a 
            geopandas GeoDataFrame to compare
        table2 : str | pd.DataFrame | gpd.GeoDataFrame
            Name/path of input tabular data file or a pandas DataFrame or a 
            geopandas GeoDataFrame to compare
        outfile : str | pathlib.Path | None, optional
            Name/path of output file for writing comparison results. Defaults
            to ``None``
        
        Returns
        -------
        compare.CompareTables

        Examples
        --------
        TODO

        """
        # Encapsulated attributes
        table1 = None
        table2 = None
        outfile = None

        # Protected attributes
        # TODO: add if necessary

        self.__sanitize_init(table1, table1, outfile)


    @classmethod
    def read_files(self, filename1: str, filename2: str):
        """
        Returns an CompareTables instance with the given filenames.

        Parameters
        ----------
        filename1 : str
            Name/path of first input file of tabular data to read
        filename2 : str
            Name/path of second input file of tabular data to read

        Returns
        -------
        compare.CompareTables

        Examples
        --------
        TODO

        """
        pass
    

    @classmethod
    def read_tables(self, 
                    table1: Union[pd.DataFrame, gpd.GeoDataFrame], 
                    table2: Union[pd.DataFrame, gpd.GeoDataFrame]):
        """
        Returns a CompareTables instance with the given GeoDataFrames.

        Parameters
        ----------
        table1 : pd.DataFrame | gpd.GeoDataFrame
            pandas DataFrame or geopandas GeoDataFrame containing table to compare
        table2 : pd.DataFrame | gpd.GeoDataFrame
            pandas DataFrame or geopandas GeoDataFrame containing table to compare
        
        Returns
        -------
        compare.CompareTables

        Examples
        --------
        TODO

        """
        pass
    

    def __sanitize_init(self,
                        table1:    Union[str, pd.DataFrame, gpd.GeoDataFrame],
                        table2:    Union[str, pd.DataFrame, gpd.GeoDataFrame],
                        outfile:   Optional[Union[str, pathlib.Path]]):
        """
        Safely initializes attributes using setters.

        Parameters
        ----------
        table1 : str | pd.DataFrame | gpd.GeoDataFrame
            Name/path of input tabular data file or a pandas DataFrame or a 
            geopandas GeoDataFrame to compare
        table2 : str | pd.DataFrame | gpd.GeoDataFrame
            Name/path of input tabular data file or a pandas DataFrame or a 
            geopandas GeoDataFrame to compare
        outfile : str | pathlib.Path | None, optional
            Name/path of output file for writing comparison results
        
        Raises
        ------
        AttributeError
            Raised if setter throws an error

        """
        try:
            self.table1 = table1
            self.table2 = table2
            self.outfile = outfile

        except Exception as e:
            raise AttributeError("Initialization failed. {}".format(e))


    #===========================================+
    # Public Instance Methods                   |
    #===========================================+
    
    # TODO
    def compare(self) -> NoReturn:
        pass
    

    #===========================================+
    # Private Helper Methods                    |
    #===========================================+

    def __get_table(self, table: Union[str, pd.DataFrame, 
                                       gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
        try:
            return et(table).extract()
        except Exception as e:
            raise FileNotFoundError('Could not set table. {}'.format(e))


    #===========================================+
    # Getters and Setters                       |
    #===========================================+

    @property
    def table1(self) -> gpd.GeoDataFrame:
        """
        {gpd.GeoDataFrame}
            Table to compare
        
        """
        return self.__table1
    
    @table1.setter
    def table1(self, table: Union[str, pd.DataFrame, 
                                  gpd.GeoDataFrame]) -> NoReturn:
        self.__table1 = self.__get_table(table)
    

    def table2(self) -> gpd.GeoDataFrame:
        """
        {gpd.GeoDataFrame}
            Table to compare
        
        """
        return self.__table2
    
    @table1.setter
    def table2(self, table: Union[str, pd.DataFrame, 
                                  gpd.GeoDataFrame]) -> NoReturn:
        self.__table2 = self.__get_table(table)
    

    @property
    def outfile(self) -> Optional[pathlib.Path]:
        """
        {pathlib.Path | None}
            Path of output file for writing. Defaults to stdout

        """
        return self.__outfile

    @outfile.setter
    def outfile(self, filename: Optional[str] = None) -> NoReturn:
        try:
            self.__outfile = pathlib.Path(filename)
        except:
            self.__outfile = None



#########################################
#                                       #
#        Testing Function Calls         #
#                                       #
#########################################


