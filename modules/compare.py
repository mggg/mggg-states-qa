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
    TODO
    
    """

    #===========================================+
    # Constructors                              |
    #===========================================+

    def __init__():
        """
        CompareTables initializer.

        Parameters
        ----------
        TODO
        
        Returns
        -------
        compare.CompareTables


        Examples
        --------
        TODO

        """
        # Encapsulated attributes

        # Protected attributes
        pass


    @classmethod
    def read_files(self, filename1: str, filename2: str):
        """
        Returns an CompareTables instance with a specified input filenames.

        Parameters
        ----------
        filename : str
            Name/path of first input file of tabular data to read
        filename : str
            Name/path of second input file of tabular data to read

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


