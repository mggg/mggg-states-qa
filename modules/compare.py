"""
compare.py
==========

Provides
    - A python class, ``CompareTables`` for comparing geodata. Main use case
      is Data QA through comparing processed geodata with those from other
      sources (e.g. MEDSL)

Metadata
--------

:Filename:      `compare.py <https://github.com/keiferc/gdutils/>`_
:Author:        `@KeiferC <https://github.com/keiferc>`_
:Date:          06 July 2020
:Version:       0.0.1
:Description:   Module for comparing geodata
:Dependencies:  

                - ``geopandas``
                - ``numpy``

Documentation
-------------

Documentation for the ``compare`` module can be found as docstrings. 
Run ``import modules.compare; help(modules.compare)`` to view documentation.
::

    $ python
    >>> import modules.compare; help(modules.compare)

Additionally, documentation can be found on `Read the Docs 
<https://gdutils.readthedocs.io>`_.

"""
import argparse
import geopandas as gpd
import numpy as np
import os.path
import pandas as pd
import pathlib
import shapely.wkt
import sys
import zipfile

from typing import List, NoReturn, Optional, Tuple, Union
import warnings; warnings.filterwarnings(
    'ignore', 'GeoSeries.isna', UserWarning)



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
    outfile : Optional[str, pathlib.Path]
        Name/path of output file for writing comparison results. Defaults
        to ``None``
    
    """

    #===========================================+
    # Constructors                              |
    #===========================================+

    def __init__(table1:    Union[str, pd.DataFrame, gpd.GeoDataFrame],
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
        pass


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
    

    def __sanitize_init():
        """
        Safely initializes attributes using setters.

        Parameters
        ----------
        TODO
        
        Raises
        ------
        AttributeError
            Raised if setter throws an error

        """
        try:
            pass # TODO

        except Exception as e:
            raise AttributeError("Initialization failed. {}".format(e))


    #===========================================+
    # Public Instance Methods                   |
    #===========================================+
    

    #===========================================+
    # Getters and Setters                       |
    #===========================================+



#########################################
#                                       #
#        Testing Function Calls         #
#                                       #
#########################################


