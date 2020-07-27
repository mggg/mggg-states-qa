import numpy as np
import pandas as pd
import geopandas as gpd
import os
import json

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

standards_path = '../scripts/naming_convention.json'

gh_user = 'octocate'
gh_acct_type = 'users'
gh_repos = [ # Note: this list is subject to change
    'linguist.git', 
    'octocat.github.io.git', 
    'git-consortium.git', 
    'hello-worId.git', 
    'test-repo1.git', 
    'boysenberry-repo-1.git', 
    'Hello-World.git', 
    'Spoon-Knife.git']

gitignores = [ # Note: also subject to change
    './.gitignore', 
    './.pytest_cache/.gitignore', 
    './tests/dumps/linguist.git/.gitignore', 
    './tests/dumps/linguist.git/vendor/grammars/Sublime-Inform/.gitignore']

htmls = [ # Note: same here
    './tests/dumps/linguist.git/samples/HTML/pages.html', 
    './tests/dumps/octocat.github.io.git/index.html', 
    './tests/dumps/Spoon-Knife.git/index.html']

descriptions = [ # Note: ditto
    './tests/dumps/linguist.git/.git/description', 
    './tests/dumps/octocat.github.io.git/.git/description', 
    './tests/dumps/git-consortium.git/.git/description', 
    './tests/dumps/hello-worId.git/.git/description', 
    './tests/dumps/test-repo1.git/.git/description', 
    './tests/dumps/boysenberry-repo-1.git/.git/description', 
    './tests/dumps/Hello-World.git/.git/description', 
    './tests/dumps/Spoon-Knife.git/.git/description', 
    './.git/description']


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
    with pytest.raises(Exception):
        dq.list_files_of_type(1)

    files = dq.list_files_of_type('description')
    assert files == descriptions

    files = dq.list_files_of_type('.q;weoifh0[238ubfasdf')
    assert files == []

    files = dq.list_files_of_type(['description', '.html'])
    assert files.sort() == (descriptions + htmls).sort()

    files = dq.list_files_of_type('description', 
                                  os.path.join('tests', 'dumps'))
    descriptions.remove('./.git/description')
    descrs = [d.lstrip('./') for d in descriptions]
    assert files == descrs

    files = dq.list_files_of_type('.gitignore', exclude_hidden = True)
    assert files == []

    files = dq.list_files_of_type('.gitignore', exclude_hidden = False)
    assert files == gitignores


def test_compare_column_names():
    pass


def test_remove_repos():
    with pytest.raises(Exception):
        dq.remove_repos('XGx2ePfMTt3jbQEGWCzCHaRzWpC6Vz7qY48VY')

    dq.remove_repos(os.path.join('tests', 'dumps'))
    dirs = next(os.walk(os.path.join('tests', 'dumps')))
    assert not any(list(map(lambda x, y: x == y, dirs[1], gh_repos)))

    dq.remove_repos(os.path.join('tests', 'dumps')) # should not raise anything


#########################################
# Helper Functions                      #
#########################################

def get_standards():
    with open(standards_path) as json_file:
        standards_raw = json.load(json_file)
    
    geographies = dq.get_keys_by_category(standards_raw, 'geographies')
    offices = dq.get_keys_by_category(standards_raw, 'offices')
    parties = dq.get_keys_by_category(standards_raw, 'parties')
    demographics = dq.get_keys_by_category(standards_raw, 'demographics')
    districts = dq.get_keys_by_category(standards_raw, 'districts')
    counts = dq.get_keys_by_category(standards_raw, 'counts')
    other = dq.get_keys_by_category(standards_raw, 'other')

    elections = [office + format(year, '02') + party 
                    for office in offices
                    for year in range(0, 21)
                    for party in parties 
                    if not (office == 'PRES' and year % 4 != 0)]

    counts = [count + format(year, '02') 
                    for count in counts 
                    for year in range(0, 20)]

    return geographies + elections + demographics + districts + \
           counts + other

