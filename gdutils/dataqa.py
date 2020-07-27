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
                - ``numpy``
                - ``gdutils.extract``

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
import numpy as np 
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

def clone_repos(account: str,
                account_type: str,
                outpath: Optional[Union[str, pathlib.Path]] = None) \
        -> NoReturn:
    """
    Clones public GitHub repositories into the given directory. If
    directory path is not provided, clones repos into the current
    working directory.

    Parameters
    ----------
    account : str
        Github account whose public repos are to be cloned.
    account_type: str
        Type of github account whose public repos are to be cloned.
        Valid options: ``'users'``, ``'orgs'``.
    outpath: str | pathlib.Path, optional
        Path to which repos are to be cloned. If not specified, clones
        repos into current working directory.
    
    Raises
    ------
    ValueError
        Raised if provided an account type other than ``'users'`` or 
        ``'orgs'``.

    Examples
    --------
    >>> dataqa.clone_repos('mggg-states', 'orgs')

    >>> dataqa.clone_repos('octocat', 'users', 'cloned-repos')

    """
    try:
        cmds = __get_clone_cmds(account, account_type, outpath)
        responses = list(map(lambda cmd : subprocess.run(cmd), cmds))

        for res in responses:
            if res.returncode != 0:
                sys.stderr.write("Failed to clone {}.\n".format(res.args[2]))

    except Exception as e:
        raise RuntimeError("Unable to clone repos. {}".format(e))


def remove_repos(dirpath: Union[str, pathlib.Path]) \
        -> NoReturn:
    """
    Given a name/path of a directory, recursively removes all git repositories
    starting from the given directory. This action cannot be undone.

    Warning: this function will remove the given directory if the given directory 
    itself is a git repo.

    Parameters
    ----------
    dirpath: str | pathlib.Path
        Name/path of directory from which recursive removal of repos begins.
    
    Raises
    ------
    FileNotFoundError
        Raised if unable to find the given directory.

    """
    try:
        repos = __list_repos(dirpath)
        cmds = [['rm', '-r', repo] for repo in repos]
        
        responses = list(map(lambda cmd : subprocess.run(cmd), cmds))

        for res in responses:
            if res.returncode != 0:
                sys.stderr.write("Failed to remove repo {}.\n".format(res.args[2]))

    except Exception as e:
        raise RuntimeError("Unable to remove repo. {}".format(e)) 


def list_files_of_type(filetype: Union[str, List[str]], 
                       dirpath: Optional[Union[str, pathlib.Path]] = '.',
                       exclude_hidden: Optional[bool] = True) \
        -> List[str]:
    """
    Given a file extension and an optional directory path, returns a list of
    file paths of files containing the extension. If the directory path is not
    specified, function defaults to listing files from the current 
    working directory.

    Parameters
    ----------
    filetype: str | List[str]
        File extension of files to list (e.g. ``'.zip'``). Can be a list of
        extensions (e.g. ``['.zip', '.shp', '.csv']``).
    dirpath: str | pathlib.Path, optional, default = ``'.'``.
        Path to directory from which file listing begins. Defaults to
        current working directory if not specified.
    exclude_hidden: bool, option, default = ``True``
        If false, function includes hidden files in the search.
    
    Returns
    -------
    List[str]

    Raises
    ------
    FileNotFoundError
        Raised if unable to find given directory.

    Examples
    --------
    >>> list_of_zips = dataqa.list_files_of_type('.zip')
    >>> print(list_of_zips)
    ['./zipfile1.zip', './zipfile2.zip', './shapefiles/shape1.zip', 
    './shapefiles/shape2.zip']

    >>> list_of_shps = dataqa.list_files_of_type('.shp', 'shapefiles/')
    >>> print(list_of_shps)
    ['./shapefiles/shape1/shape1.shp', './shapefiles/shape2/shape2.shp']

    >>> list_of_csvs = dataqa.list_files_of_type('.csv', exclude_hidden=False)
    >>> print(list_of_csvs)
    ['./csv1.csv', './.hidden-dir/csv_hidden.csv']

    >>> list_of_mix = dataqa.list_files_of_type(['.shp', '.zip'])
    >>> print(list_of_mix)
    ['./shapefiles/shape1/shape1.shp', './shapefiles/shape2/shape2.shp',
     './zipfile1.zip', './zipfile2.zip', './shapefiles/shape1.zip', 
     './shapefiles/shape2.zip']

    """
    root_path = __get_validated_path(dirpath)

    if isinstance(filetype, str):
        filetype = [filetype]

    all_files = []
    for path, _, files in os.walk(root_path):
        [all_files.append(os.path.join(path, file)) for file in files
                if not (exclude_hidden and file[0] == '.')]
    
    return [file for file in all_files 
                 if any([file.endswith(ftype) for ftype in filetype])]


def get_keys_by_category(dictionary: Dict[Hashable, List[Iterable]], 
                         category: Union[Hashable, List[Hashable]]) \
        -> List[Hashable]:
    """
    Given a dictionary with categories, returns a list of keys in the
    given category.

    Examples of accepted forms of dictionary input:
    ::

        {category1 : [{key1 : value1}, {key2 : value2}]
         category2 : [{key3 : value3},]}

    ::

        {category1 : [[key1, key2, key3]]}
    
    ::

        {category1 : [[key1]],
         category2 : [[key2], {key3: value3}]}

    Parameters
    ----------
    dictionary : Dict[Hashable, List[Iterable]]
        Dictionary containing categories in which keys are stored.
    category : Hashable | List[Hashable]
        Category containing keys-value pairs.
    
    Returns
    -------
    List[Hashable]
        List of keys of every key-value pair in the given category of the
        given dictionary.
    
    Examples
    --------
    >>> sample_dict = {'category1' : [{'key1': 1}],
                       'category2' : [{'key2' : 2}, {'key3' : 3}]}
    >>> keys = dataqa.get_keys_by_category(sample_dict, 'category2')
    >>> print(keys)
    ['key2', 'key3']

    >>> sample_dict =  {'category1' : [['key1']],
                        'category2' : [['key2'], {'key3': 'value3'}]}
    >>> keys = dataqa.get_keys_by_category(sample_dict, 'category2')
    >>> print(keys)
    ['key2', 'key3']

    >>> keys = dataqa.get_keys_by_category(sample_dict, 
                                           ['category1', 'category2'])
    >>> print(keys)
    ['key1', 'key2', 'key3']

    """
    flatten = lambda xs : [x for sublist in xs for x in sublist]
    try:
        return flatten([list(key) for key in dictionary[category]])
    except: # category is a list
        return flatten([list(key) for item in category 
                                  for key in dictionary[item]])


def compare_column_names(table: Union[pd.DataFrame, gpd.GeoDataFrame],
                         standards: Union[List[str], Set[str]]) \
        -> Tuple[Set[str], Set[str]]:
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
                          columns=['COL1', 'col2', 'COL3'])
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
                      columns: Union[List[str], Set[str]]) \
        -> List[Tuple[str, int]]:
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
                          columns=['COL1', 'COL2', 'COL3'])
    >>> print(df)
       COL1  COL2  COL3
    0     1     2     3
    1     4     5     6
    >>> totals = dataqa.sum_column_values(df, cols)
    >>> for column, sum in totals:
            print("{}: {}".format(column, sum))
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
        row2: Optional[Union[Hashable, List[Hashable]]] = None) \
        -> Dict[str, List[Tuple[Hashable, Any]]]:
    """
    Given two tables and their corresponding columns and rows to compare,
    returns a dictionary containing the compared columns and a corresponding 
    list of tuples containing row names and absolute differences of values.

    Parameters
    ----------
    table1: pd.DataFrame | gpd.GeoDataFrame
        TODO
    table2: pd.DataFrame | gpd.GeoDataFrame
        TODO
    column1: str | List[str]
        TODO
    column2: str | List[str]
        TODO
    row1: Hashable | List[Hashable], optional, default = ``None``
        TODO
    row2: Hashable | List[Hashable], optional, default = ``None``
        TODO

    Returns
    -------
    Dict[str, List[Tuple[Hashable, Any]]]
        A dictionary with string keys corresponding to names of compared
        columns and with List values of tuples corresponding to names of 
        compared rows and absolute differences of their values. E.g.
        ``{'col1-col2': [('val1-val1', 2), ('val2-val2', 0)],
           'colA-colB': [('valA1-valB1', 5)]}``

    Raises
    ------
    KeyError
        Raised if unable to find column or row in tables.
    TypeError
        Raised if unable to calculate the absolute difference between
        two values.
    
    Examples
    --------
    >>> TODO: Coming soon

    """
    pass # TODO


def compare_column_sums():
    pass # TODO



#########################################
#                                       #
#           Helper Definitions          #
#                                       #
#########################################

def __get_clone_cmds(account: str,
                     account_type: str,
                     dirpath: Optional[Union[str, pathlib.Path]] = None) \
        -> List[str]:
    """
    Returns a list of subprocess-valid git clone commands.

    """
    valid_acc_types = ['users', 'orgs']
    gh_api = 'https://api.github.com'
    gh_endpt = 'repos'

    if account_type not in valid_acc_types:
        raise ValueError(
            "Invalid account type. Valid options: {}.".format(valid_acc_types))
    
    gh_api_url = gh_api + '/' + account_type + '/' + account + '/' + gh_endpt

    raw_response = requests.get(gh_api_url)
    response = json.loads(raw_response.text)

    try:
        cmds = [['git', 'clone', repo['clone_url']] for repo in response]
    except Exception as e:
        try:
            raise RuntimeError(response['message'])
        except:
             raise RuntimeError(e)

    if dirpath is not None:
        [cmd.append(os.path.join(dirpath, cmd[2].split('/')[-1])) 
            for cmd in cmds]
    
    return cmds


def __list_repos(dirpath: Optional[Union[str, pathlib.Path]] = '.') \
        -> List[str]:
    """
    Given a starting search directory, returns a list of paths to git repos
    on the local machine.

    """
    root_path = __get_validated_path(dirpath)

    subdirs = []
    for path, dirs, _ in os.walk(root_path):
        [subdirs.append(os.path.join(path, directory)) for directory in dirs]

    return [subdir.rstrip(os.path.basename(subdir)) 
                for subdir in subdirs if pathlib.Path(subdir).name == '.git']


def __get_validated_path(dirpath: Union[str, pathlib.Path]) -> pathlib.Path:
    try:
        root_path = pathlib.Path(dirpath)
        if not os.path.isdir(root_path):
            raise FileNotFoundError(
                    "Unable to find directory '{}'.".format(dirpath))
        return root_path

    except Exception as e:
        raise Exception("Failed to traverse path.".format(e))
        
