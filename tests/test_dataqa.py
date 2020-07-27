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

standards_path = 'scripts/naming_convention.json'

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


def test_get_keys_by_category(): # test passing list of categories, try numbers
    with open(standards_path) as json_file:
        standards_raw = json.load(json_file)

    with pytest.raises(Exception):
        dne = dq.get_keys_by_category(standards_raw, '-1293urnpef13qewf')
    
    with pytest.raises(Exception):
        numbered = dq.get_keys_by_category(
        {1 : {9: 'asdf'}, 2 : {8: 'fdsa'}}, 1)
    
    with pytest.raises(Exception):
        xs = dq.get_keys_by_category(
            {'foo' : [1, 2, {'fdaa : asdf'}]}, 'foo')

    numbered = dq.get_keys_by_category(
        {1 : [{9: 'asdf'}], 2 : [{8: 'fdsa'}]}, 1)
    assert numbered == [9]

    parties = dq.get_keys_by_category(standards_raw, 'parties')
    assert parties == ['D', 'R', 'L', 'G', 'I', 'U']

    xs = dq.get_keys_by_category(
        {'[1, 2, 3]': ['asdf', 'fdaa'],
         '[4, 5, 6]': [{'fdas': 'fdsa'}, {'hjkl' : 'hjkl'}],
         'foo': [{'bar': 'bar'}]}, '[1, 2, 3]')
    assert xs == ['a', 's', 'd', 'f', 'f', 'd', 'a', 'a']

    xs = dq.get_keys_by_category(
        {'[1, 2, 3]': ['asdf', 'fdaa'],
         '[4, 5, 6]': [{'fdas': 'fdsa'}, {'hjkl' : 'hjkl'}],
         'foo': [{'bar': 'bar'}]}, '[4, 5, 6]')
    assert xs == ['fdas', 'hjkl']

    xs = dq.get_keys_by_category(
        {'[1, 2, 3]': [[1, 2, 3], {'fdaa' : 'asdf'}],
         '[4, 5, 6]': [{'fdas': 'fdsa'}, {'hjkl' : 'hjkl'}],
         'foo': [{'bar': 'bar'}]}, '[1, 2, 3]')
    assert xs == [1, 2, 3, 'fdaa']
    
    xs = dq.get_keys_by_category(
        {'category1' : [['key1']],
         'category2' : [['key2'], {'key3': 'value3'}]}, 
         ['category1', 'category2'])
    assert xs == ['key1', 'key2', 'key3']


def test_compare_column_names():
    pass


def test_sum_column_values():
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
    
    offices = dq.get_keys_by_category(standards_raw, 'offices')
    parties = dq.get_keys_by_category(standards_raw, 'parties')
    counts = dq.get_keys_by_category(standards_raw, 'counts')
    others = dq.get_keys_by_category(standards_raw, 
                ['geographies', 'demographics', 'districts', 'other'])

    elections = [office + format(year, '02') + party 
                    for office in offices
                    for year in range(0, 21)
                    for party in parties 
                    if not (office == 'PRES' and year % 4 != 0)]

    counts = [count + format(year, '02') 
                    for count in counts 
                    for year in range(0, 20)]

    return elections + counts + others
