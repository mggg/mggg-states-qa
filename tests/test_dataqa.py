import numpy as np
import pandas as pd
import geopandas as gpd
import os

import pytest

import gdutils.extract as et
import gdutils.dataqa as dq


#########################################
# Regression Test Inputs                #
#########################################

mggg_file = 'tests/inputs/CT_precincts.zip'
    # pulled from github.com/mggg-states/CT-shapefiles

medsl_file = 'tests/inputs/medsl18_ct_clean.csv'
    # pulled from github.com/MEDSL/2018-elections-official/
    # source file: precinct_2018.zip
    # file used in test contains a subtable of CT specific data extracted
    # from precinct_2018.zip using the ``gdutils.extract``` module
    # pivoted with 'office', 'party' and flattened multi-index column

mggg_gdf = et.read_file(mggg_file).extract()
medsl_gdf = et.read_file(medsl_file).extract()

gh_user = 'octocate'
gh_acct_type = 'users'
gh_repos = ['linguist.git', # Note: this list is subject to change
            'octocat.github.io.git', 
            'git-consortium.git', 
            'hello-worId.git', 
            'test-repo1.git', 
            'boysenberry-repo-1.git', 
            'Hello-World.git', 
            'Spoon-Knife.git']

gitignores = [ # Note: also subject to change
    'tests/dumps/linguist.git/.gitignore', 
    'tests/dumps/linguist.git/vendor/grammars/Sublime-Inform/.gitignore']

htmls = ['./tests/dumps/linguist.git/samples/HTML/pages.html', 
         './tests/dumps/octocat.github.io.git/index.html', 
         './tests/dumps/Spoon-Knife.git/index.html']


#########################################
# Regression Tests                      #
#########################################

def test_clone_repos():
    with pytest.raises(Exception):
        dq.clone_repos()
    with pytest.raises(Exception):
        dq.clone_repos('octocat')
    with pytest.raises(Exception):
        dq.clone_repos('octocat', 'asdf')
    with pytest.raises(Exception):
        dq.clone_repos('octocat', 'orgs')
    with pytest.raises(Exception): # randomly generated string for user
        dq.clone_repos('XGx2ePfMTt3jbQEGWCzCHaRzWpC6Vz7qY48VY', 'users')

    dq.clone_repos('octocat', 'users', 'tests/dumps')
    
    dirs = next(os.walk(os.path.join('tests', 'dumps')))
    assert dirs[1] == gh_repos


def test_list_files_of_type():
    files = dq.list_files_of_type('.gitignore', os.path.join('tests', 'dumps'))
    assert files == gitignores

    files = dq.list_files_of_type('.q;weoifh0[238ubfasdf')
    assert files == []

    files = dq.list_files_of_type(['.gitignore', '.html'])
    assert files.sort() == (gitignores + htmls).sort()


def test_remove_repos():
    with pytest.raises(Exception):
        dq.remove_repos('XGx2ePfMTt3jbQEGWCzCHaRzWpC6Vz7qY48VY')

    dq.remove_repos(os.path.join('tests', 'dumps'))
    dirs = next(os.walk(os.path.join('tests', 'dumps')))
    assert not any(list(map(lambda x, y: x == y, dirs[1], gh_repos)))

    dq.remove_repos(os.path.join('tests', 'dumps')) # should not raise anything



