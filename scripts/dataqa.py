"""
dataqa.py
=========

Provides
    - A ``python`` module containing data quality assurance functions.

Metadata
--------
:Filename:      `dataqa.py <https://github.com/keiferc/gdutils/>`_
:Author:        `@KeiferC <https://github.com/keiferc>`_
:Date:          17 July 2020
:Version:       0.0.1
:Description:   Module for data QA
:Dependencies:  

                - ``geopandas``
                - ``numpy``

Documentation
-------------
Documentation for the ``dataqa`` module can be found as docstrings. 
Run ``from gdutils import dataqa; help(dataqa)`` to view documentation.
::

    $ python
    >>> from gdutils import dataqa; help(dataqa)

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

from typing import List, NoReturn, Optional, Set, Tuple, Union


#########################################
#                                       #
#       Function Definitions            #
#                                       #
#########################################

def clone_repos(account: str,
                account_type: str,
                dirpath: Optional[Union[str, pathlib.Path]] = None) \
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
        Valid options: 'users', 'orgs'.
    dirpath: str | pathlib.Path, optional
        Path to which repos are to be cloned. If not specified, clones
        repos into current working directory.
    
    Raises
    ------
    ValueError
        Raised if provided an account type other than 'user' or 'orgs'.

    Examples
    --------
    >>> dataqa.clone_repos('mggg-states', 'orgs')

    >>> dataqa.clone_repos('octocat', 'users', 'cloned-repos')

    """
    try:
        cmds = __get_clone_cmds(account, account_type, dirpath)
        responses = list(map(lambda cmd : subprocess.run(cmd), cmds))

        for res in responses:
            if res.returncode != 0:
                sys.stderr.write("Failed to clone {}.\n".format(res.args[2]))

    except Exception as e:
        raise RuntimeError("Unable to clone repos. {}".format(e))


def remove_repos(dirpath: Optional[Union[str, pathlib.Path]] = '.') \
        -> NoReturn:
    """
    Given a name/path of a directory, recursively removes all git repositories
    starting from the given directory.

    Note: the function only the repos in the given directory; it does not remove
    the given directory if the given directory itself is a repo.

    Parameters
    ----------
    dirpath: str | pathlib.Path, optional, default = '.'
        Name/path of directory from which recursive removal of repos begins.
    
    Raises
    ------
    FileNotFoundError
        Raised if unable to find the given directory.

    """
    repos = __list_repos(dirpath)
    # TODO


def list_files_of_type(filetype: str, 
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
    filetype: str
        File extension of files to list (e.g. '.zip').
    dirpath: str | pathlib.Path, optional, default = '.'.
        Path to directory from which file listing begins. Defaults to
        current working directory if not specified.
    exclude_hidden: bool, option, default = True
        If false, function includes hidden directories in the search.
    
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

    """
    files_to_list = []
    subdirs = []

    try:
        root_path = pathlib.Path(dirpath)
        if not os.path.isdir(root_path):
            raise FileNotFoundError(
                    "Unable to find directory '{}'.".format(dirpath))
    except Exception as e:
        raise Exception("Failed to traverse path.".format(e))

    for path, directories, files in os.walk(root_path):
        for directory in directories: # collect subdirectories
            if exclude_hidden and not directory.startswith('.'):
                subdirs.append(os.path.join(path, directory))

        for file in files: # collect files
            if file.endswith(filetype): 
                files_to_list.append(os.path.join(path, file))

    for directory in subdirs:
        files_to_list += list_files_of_type(filetype, directory)

    return files_to_list


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
    >>> TODO

    """
    pass


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
    cmds = [['git', 'clone', repo['clone_url']] for repo in response]

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
    repos_to_list = []
    subdirs = []

    try:
        root_path = pathlib.Path(dirpath)
        if not os.path.isdir(root_path):
            raise FileNotFoundError(
                    "Unable to find directory '{}'.".format(dirpath))
    except Exception as e:
        raise Exception("Failed to traverse path.".format(e))

    for path, dirs, _ in os.walk(root_path):
        [subdirs.append(os.path.join(path, directory)) for directory in dirs]
    
    repos_to_list = [subdir.rstrip(os.path.basename(subdir)) 
                        for subdir in subdirs 
                        if pathlib.Path(subdir).name == '.git']

    return repos_to_list


##########
print(__list_repos())
