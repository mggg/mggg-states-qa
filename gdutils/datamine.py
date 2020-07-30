"""
gdutils.datamine
================

Provides
    - A ``python`` module for mining and listing data sources.

Metadata
--------
:Module:        ``gdutils.datamine``
:Filename:      `datamine.py <https://github.com/keiferc/gdutils/>`_
:Author:        `@KeiferC <https://github.com/keiferc>`_
:Date:          27 July 2020
:Version:       0.0.1
:Description:   Module for data mining

Documentation
-------------
Documentation for the ``datamine`` module can be found as docstrings. 
Run ``import gdutils.datamine; help(gdutils.datamine)`` to view documentation.
::

    $ python
    >>> import gdutils.datamine; help(gdutils.datamine)

Additionally, documentation can be found on `Read the Docs 
<https://gdutils.readthedocs.io>`_.

"""
import json
import os
import pathlib
import requests
import subprocess
import sys
import urllib.parse

from typing import Dict, Hashable, Iterable, List, NoReturn, Optional, Union



#########################################
#                                       #
#       Function Definitions            #
#                                       #
#########################################

def list_gh_repos(account: str, account_type: str) -> List[str]:
    """
    Returns a list of public GitHub repositories associated with the given
    account and account type.

    Parameters
    ----------
    account : str
        Github account whose public repos are to be cloned.
    account_type: str
        Type of github account whose public repos are to be cloned.
        Valid options: ``'users'``, ``'orgs'``.

    Returns
    -------
    List[str]
        A list of public Github repositories.

    Raises
    ------
    ValueError
        Raised if the given account_type is neither ``'users'`` nor ``'orgs'``.
    RuntimeError
        Raised if unable to query GitHub for repo information.

    Examples
    --------
    >>> repos = datamine.list_gh_repos('octocat', 'users')
    >>> for repo in repos:
    ...     print(repo)
    https://github.com/octocat/boysenberry-repo-1.git
    https://github.com/octocat/git-consortium.git
    https://github.com/octocat/hello-worId.git
    https://github.com/octocat/Hello-World.git
    https://github.com/octocat/linguist.git
    https://github.com/octocat/octocat.github.io.git
    https://github.com/octocat/Spoon-Knife.git
    https://github.com/octocat/test-repo1.git

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
        return [repo['clone_url'] for repo in response]
    except Exception:
        msg = "Unable to list repos for account {}.".format(account)
        try:
            raise RuntimeError(msg + response['message'])
        except:
             raise RuntimeError(msg + e)


def clone_gh_repos(account: str,
                   account_type: str,
                   repo: Optional[Union[str, List[str]]] = None,
                   outpath: Optional[Union[str, pathlib.Path]] = None
                   ) -> NoReturn:
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
    >>> datamine.clone_repos('mggg-states', 'orgs')

    >>> datamine.clone_repos(
    ...     'mggg-states', 'orgs', 
    ...     'https://github.com/mggg-states/AZ-shapefiles.git')

    >>> datamine.clone_repos(
    ...     'mggg-states', 'orgs', 
    ...     ['https://github.com/mggg-states/AZ-shapefiles.git',
    ...      'https://github.com/mggg-states/HI-shapefiles.git'])

    >>> datamine.clone_repos(
    ...     'mggg-states', 'orgs', 
    ...     'https://github.com/mggg-states/HI-shapefiles.git', 'shps/')

    >>> datamine.clone_repos('octocat', 'users', outpath='cloned-repos/')

    """
    try:
        if repo is None:
            queried_repos = list_gh_repos(account, account_type)
            cmds = __generate_clone_cmds(queried_repos, outpath)
        elif isinstance(repo, str):
            cmds = __generate_clone_cmds([repo], outpath)
        else:
            cmds = __generate_clone_cmds(repo, outpath)

        responses = list(map(lambda cmd : subprocess.run(cmd), cmds))

        for res in responses:
            if res.returncode != 0:
                sys.stderr.write("Failed to clone {}.\n".format(res.args[2]))

    except Exception as e:
        raise RuntimeError("Unable to clone repos. {}".format(e))


# TODO: consider adding ability to remove specific repos?
def remove_repos(dirpath: Union[str, pathlib.Path]) -> NoReturn:
    """
    Given a name/path of a directory, recursively removes all git repositories
    starting from the given directory. This action cannot be undone.

    *Warning:* this function will remove the given directory if the given 
    directory itself is a git repo.

    Parameters
    ----------
    dirpath: str | pathlib.Path
        Name/path of directory from which recursive removal of repos begins.
    
    Raises
    ------
    FileNotFoundError
        Raised if unable to find the given directory.
    
    Examples
    --------
    >>> datamine.remove_repos()

    >>> datamine.remove_repos('repos_to_remove/')

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
                       exclude_hidden: Optional[bool] = True
                       ) -> List[str]:
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
        List of file paths of files containing the given extension.

    Raises
    ------
    FileNotFoundError
        Raised if unable to find given directory.

    Examples
    --------
    >>> list_of_zips = datamine.list_files_of_type('.zip')
    >>> print(list_of_zips)
    ['./zipfile1.zip', './zipfile2.zip', './shapefiles/shape1.zip', 
    './shapefiles/shape2.zip']

    >>> list_of_shps = datamine.list_files_of_type('.shp', 'shapefiles/')
    >>> print(list_of_shps)
    ['./shapefiles/shape1/shape1.shp', './shapefiles/shape2/shape2.shp']

    >>> list_of_csvs = datamine.list_files_of_type('.csv', 
    ...                                            exclude_hidden = False)
    >>> print(list_of_csvs)
    ['./csv1.csv', './.hidden-dir/csv_hidden.csv']

    >>> list_of_mix = datamine.list_files_of_type(['.shp', '.zip'])
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
                         category: Union[Hashable, List[Hashable]]
                         ) -> List[Hashable]:
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
    ...                'category2' : [{'key2' : 2}, {'key3' : 3}]}
    >>> keys = datamine.get_keys_by_category(sample_dict, 'category2')
    >>> print(keys)
    ['key2', 'key3']

    >>> sample_dict =  {'category1' : [['key1']],
    ...                 'category2' : [['key2'], {'key3': 'value3'}]}
    >>> keys = datamine.get_keys_by_category(sample_dict, 'category2')
    >>> print(keys)
    ['key2', 'key3']

    >>> keys = datamine.get_keys_by_category(sample_dict, 
    ...                                      ['category1', 'category2'])
    >>> print(keys)
    ['key1', 'key2', 'key3']

    """
    flatten = lambda xs : [x for sublist in xs for x in sublist]
    try:
        return flatten([list(key) for key in dictionary[category]])
    except: # category is a list
        return flatten([list(key) for item in category 
                                  for key in dictionary[item]])



#########################################
#                                       #
#           Helper Definitions          #
#                                       #
#########################################

def __generate_clone_cmds(
        repos: Optional[Union[Dict[str, str], List[str]]] = None,
        dirpath: Optional[Union[str, pathlib.Path]] = None
        ) -> List[str]:
    """
    Given a list of repos, returns a list of subprocess-valid 
    git clone commands.

    """
    try: # if repos is a Dict - EAFP
        cmds = [['git', 'clone', repo['clone_url']] for repo in repos]
    except Exception:
        pass

    try: # if repos is a List - EAFP
        cmds = [['git', 'clone', repo] for repo in repos]
    except Exception as e:
        raise RuntimeError(
            'Unable to generate clone commands. {}'.format(e))

    if dirpath is not None:
        [cmd.append(os.path.join(dirpath, cmd[2].split('/')[-1])) 
            for cmd in cmds]

    return cmds
    

def __list_repos(dirpath: Optional[Union[str, pathlib.Path]] = '.'
                 ) -> List[str]:
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
        
