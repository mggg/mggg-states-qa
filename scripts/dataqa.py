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

from typing import List, NoReturn, Optional, Tuple, Union


#########################################
#                                       #
#       Function Definitions            #
#                                       #
#########################################

def clone_repos(account: str,
                account_type: str,
                dirpath: Optional[Union[str, pathlib.Path]]=None) -> NoReturn:
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


#########################################
#                                       #
#           Helper Definitions          #
#                                       #
#########################################
def __get_clone_cmds(account: str,
                     account_type: str,
                     dirpath: Optional[Union[str, pathlib.Path]]=None) \
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


# Function calls -- testing
clone_repos('keiferc', 'users', 'dump')
