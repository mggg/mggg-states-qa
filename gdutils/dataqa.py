"""
gdutils.dataqa
==============

Provides
    - A ``python`` module containing data quality assurance functions.

Metadata
--------
:Module:        ``gdutils.dataqa``
:Filename:      `dataqa.py <https://github.com/keiferc/gdutils/>`_
:Author:        `@KeiferC <https://github.com/keiferc>`_
:Date:          17 July 2020
:Version:       0.0.1
:Description:   Module for data QA
:Dependencies:  

                - ``geopandas``
                - ``gdutils.extract``
                - ``pandas``

Documentation
-------------
Documentation for the ``dataqa`` module can be found as docstrings. 
Run ``import gdutils.dataqa; help(gdutils.dataqa)`` to view documentation.
::

    $ python
    >>> import gdutils.dataqa; help(gdutils.dataqa)

Additionally, documentation can be found on `Read the Docs 
<https://gdutils.readthedocs.io>`_.

"""
import geopandas as gpd
import json
import os
import pandas as pd 
import pathlib
import requests
import subprocess
import sys
import urllib.parse

import gdutils.extract as et
from typing import (Any, Dict, Hashable, Iterable, List, 
                    NoReturn, Optional, Set, Tuple, Union)



#########################################
#                                       #
#       Function Definitions            #
#                                       #
#########################################

def compare_column_names(table: Union[pd.DataFrame, gpd.GeoDataFrame],
                         standards: Union[List[str], Set[str]]
                         ) -> Tuple[Set[str], Set[str]]:
    """
    Given either a pandas DataFrame or a geopandas GeoDataFrame and a list
    of standardized column names, returns a tuple containing the intersection
    between standardized column names and columns in the table and the set of
    columns names in the table that are not in the standards.

    Parameters
    ----------
    table : pd.DataFrame | gpd.GeoDataFrame
        Tabular data whose column names are to be compared against the 
        standards.
    standards : List[str] | Set[str]
        List/set of standardized column names to be compared against the given
        tabular data.
    
    Returns
    -------
    Tuple[Set[str], Set[str]]
        The first set in the tuple contains the intersection of column names
        between the table and the standards list. The second set in the tuple
        contains the column name in the difference between the table and the
        standards list.


    Examples
    --------
    >>> standards = ['COL1', 'COL2', 'COL3']
    >>> df = pd.DataFrame(data=[[1, 2, 3], [4, 5, 6]],
    ...                   columns=['COL1', 'col2', 'COL3'])
    >>> print(df)
       COL1  col2  COL3
    0     1     2     3
    1     4     5     6
    >>> (matches, discrepancies) = dataqa.compare_column_names(df, standards)
    >>> print(matches)
    {'COL1', 'COL3'}
    >>> print(discrepancies)
    {'col2'}

    """
    intersection = set(standards).intersection(set(table.columns))
    difference = set(table.columns) - intersection
    return (intersection, difference)


def sum_column_values(table: Union[pd.DataFrame, gpd.GeoDataFrame],
                      columns: Union[List[str], Set[str]]
                      ) -> List[Tuple[str, int]]:
    """
    Given a pandas DataFrame of a geopandas GeoDataFrame, and given a list of 
    column names, returns a list of tuples (key-value pairs) of column names 
    and the sum of their values. It is an unchecked runtime error if a column
    containing non-numerical values is passed into the function.

    Parameters
    ----------
    table : pd.DataFrame, gpd.GeoDataFrame
        Tabular data containing columns whose values are to be summed.
    columns: List[str] | Set[str]
        A list/set of column names whose values are to be summed.
    
    Returns
    -------
    List[Tuple[str, int]]
        A list of key-value pairs of column names associated with the sum
        of their values. E.g. ``[('column 1', 100), ('column 2', 53)]``.
    
    Raises
    ------
    KeyError
        Raised if given column name does not exist in table.
    
    Examples
    --------
    >>> cols = ['COL1', 'COL3']
    >>> df = pd.DataFrame(data=[[1, 2, 3], [4, 5, 6]],
    ...                   columns=['COL1', 'COL2', 'COL3'])
    >>> print(df)
       COL1  COL2  COL3
    0     1     2     3
    1     4     5     6
    >>> totals = dataqa.sum_column_values(df, cols)
    >>> for column, sum in totals:
    ...     print("{}: {}".format(column, sum))
    COL1: 5
    COL3: 9 

    """
    totals = [(col, table[col].sum()) for col in list(columns)]
    totals.sort(key = lambda tuple : tuple[0])
    return totals


def compare_column_values(
        table1: Union[pd.DataFrame, gpd.GeoDataFrame],
        table2: Union[pd.DataFrame, gpd.GeoDataFrame],
        column1: Union[str, List[str]], 
        column2: Union[str, List[str]],
        row1: Optional[Union[Hashable, List[Hashable]]] = None,
        row2: Optional[Union[Hashable, List[Hashable]]] = None
        ) -> Dict[str, List[Tuple[Hashable, Any]]]:
    """
    Given two tables and their corresponding columns and rows to compare,
    returns a dictionary containing the compared columns and a corresponding 
    list of tuples containing row names and absolute differences of values.

    *Note:* The comparison is a one-to-one and onto function. I.e. If lists
    are passed into ``column`` and ``row`` parameters, each element in one
    list must correspond to another element in the other list.

    Parameters
    ----------
    table1: pd.DataFrame | gpd.GeoDataFrame
        Tabular data containing column values to compare.
    table2: pd.DataFrame | gpd.GeoDataFrame
        Tabular data containing column values to compare.
    column1: str | List[str]
        Column(s) in table1 to compare/
    column2: str | List[str]
        Column(s) in table2 to compare.
    row1: Hashable | List[Hashable], optional, default = ``None``
        Row(s) in table1 to compare. AKA value(s) of table's index.
        If ``None``, function compares all rows.
    row2: Hashable | List[Hashable], optional, default = ``None``
        Row(s) in table2 to compare. AKA value(s) of table's index.
        If ``None``, function compares all rows.

    Returns
    -------
    Dict[str, List[Tuple[Hashable, Any]]]
        A dictionary with string keys corresponding to names of compared
        columns and with List values of tuples corresponding to names of 
        compared rows and absolute differences of their values. E.g.
        ::
        
            {'col1-col2': [('row1-row1', 2), ('row2-row2', 0)],
             'colA-colB': [('rowA1-rowB1', 5)]}

    Raises
    ------
    KeyError
        Raised if unable to find column or row in tables.
    TypeError
        Raised if unable to calculate the absolute difference between
        two values.
    RuntimeError
        Raised if given lists cannot be compared.
    
    Examples
    --------
    >>> df1 = pd.DataFrame(data=[[1, 2, 3], [4, 5, 6]],
    ...                    columns=['COL1', 'COL2', 'COL3'])
    >>> df2 = pd.DataFrame(data=[[4, 5], [1, 2]],
    ...                    columns=['col2', 'col1'])
    >>> results = dataqa.compare_column_values(df1, df2, 'COL3', 'col2')
    >>> print(results)
    {'COL3-col2': [('0-0', 1), ('1-1', 5)]}

    >>> results = dataqa.compare_column_values(df1, df2, ['COL1', 'COL2'], 
    ...                                        ['col1', 'col2'])
    >>> print(results['COL2-col2'][0])
    ('0-0', 2)
    >>> for column in results:
    ...     print('{} ----'.format(column))
    ...     for row, difference in results[column]:
    ...         print('{} : {}'.format(row, difference))
    COL1-col1 ---
    0-0 4
    1-1 2
    COL2-col2 ---
    0-0 2
    1-1 4

    >>> results = dataqa.compare_column_values(df1, df2, 'COL1', 'col1', 0, 1)
    >>> print(results['COL1-col1'][0])
    ('0-1', 1)

    >>> results = dataqa.compare_column_values(df1, df2, 'COL1', 'col1', 
    ...                                        [0, 1], [1, 0])
    >>> print(results['COL1-col1'])
    [('0-1', 1), ('1-0', 1)]

    """
    if not __can_compare(column1, column2):
        raise ValueError(
            'Cannot compare columns {} and {}.'.format(column1, column2))
    
    if row1 is None and row2 is None:
        return compare_column_values(table1, table2, column1, column2, 
                                     table1.index.tolist(), 
                                     table2.index.tolist())
    elif (row1 is not None and row2 is not None and 
         not __can_compare(row1, row2)):
        raise ValueError('Cannot compare rows {} and {}.'.format(row1, row2))

    if isinstance(column1, Hashable) and isinstance(row1, Hashable):
        return {'{}-{}'.format(column1, column2): 
                [('{}-{}'.format(row1, row2), 
                 abs(table1.at[row1, column1] - table2.at[row2, column2]))]}

    elif isinstance(column1, Hashable) and not isinstance(row1, Hashable):
        return {'{}-{}'.format(column1, column2): 
                [('{}-{}'.format(row1[i], row2[i]), 
                 abs(table1.at[row1[i], column1] - 
                     table2.at[row2[i], column2]))
                 for i in range(len(row1))]}

    elif not isinstance(column1, Hashable) and isinstance(row1, Hashable):
        return {'{}-{}'.format(column1[i], column2[i]): 
                [('{}-{}'.format(row1, row2), 
                 abs(table1.at[row1, column1[i]] - 
                     table2.at[row2, column2[i]]))]
                 for i in range(len(column1))}

    else:
        results = {}
        for i in range(0, len(column1)):
            diff = [('{}-{}'.format(row1[j], row2[j]), 
                    abs(table1.at[row1[j], column1[i]] -
                        table2.at[row2[j], column2[i]]))
                    for j in range(len(row1))]
            results['{}-{}'.format(column1[i], column2[i])] = diff
        
        return results


def compare_column_sums(
        table1: Union[pd.DataFrame, gpd.GeoDataFrame],
        table2: Union[pd.DataFrame, gpd.GeoDataFrame],
        column1: Optional[Union[str, List[str]]] = None,
        column2: Optional[Union[str, List[str]]] = None
        ) -> List[Tuple[str, Union[int, float]]]:
    """
    

    """
    pass # TODO



#########################################
#                                       #
#           Helper Definitions          #
#                                       #
#########################################

def __can_compare(item1: Union[Hashable, List[Hashable]], 
                  item2: Union[Hashable, List[Hashable]]) -> bool:
    """
    Returns True is items are both lists of equal length or are both
    Hashable

    """
    return ((item1 is not None and item2 is not None and
             isinstance(item1, type(item2))) 
            and
            (isinstance(item1, Hashable) or
             (not isinstance(item1, Hashable) and len(item1) > 0 and 
              len(item1) == len(item2))))

