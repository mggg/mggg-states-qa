import os
import json
import subprocess

import pytest

import gdutils.datamine as dm


#########################################
# Regression Test Inputs                #
#########################################

standards_path = 'scripts/naming_convention.json'

gh_user = 'octocat'
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
public_gh_repos = [ # Note: also subject to change
    'https://github.com/octocat/boysenberry-repo-1.git', 
    'https://github.com/octocat/git-consortium.git', 
    'https://github.com/octocat/hello-worId.git', 
    'https://github.com/octocat/Hello-World.git', 
    'https://github.com/octocat/linguist.git', 
    'https://github.com/octocat/octocat.github.io.git', 
    'https://github.com/octocat/Spoon-Knife.git', 
    'https://github.com/octocat/test-repo1.git']

gitignores = [ # Note: same
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
def test_list_gh_repos():
    with pytest.raises(Exception):
        dm.list_gh_repos()
    with pytest.raises(Exception):
        dm.list_gh_repos('octocat')
    with pytest.raises(Exception):
        dm.list_gh_repos('octocat', 'asdf')
    with pytest.raises(Exception): # randomly generated string for user
        dm.list_gh_repos('XGx2ePfMTt3jbQEGWCzCHaRzWpC6Vz7qY48VY', 'users')
    
    repos = dm.list_gh_repos('octocat', 'users')
    assert repos == public_gh_repos


def test_clone_gh_repos():
    with pytest.raises(Exception):
        dm.clone_gh_repos()
    with pytest.raises(Exception):
        dm.clone_gh_repos('octocat')
    with pytest.raises(Exception):
        dm.clone_gh_repos('octocat', 'asdf')
    with pytest.raises(Exception):
        dm.clone_gh_repos('octocat', 'orgs')
    with pytest.raises(Exception): # randomly generated string for user
        dm.clone_gh_repos('XGx2ePfMTt3jbQEGWCzCHaRzWpC6Vz7qY48VY', 'users')

    dm.clone_gh_repos('octocat', 'users', outpath='tests/dumps')
    dirs = next(os.walk(os.path.join('tests', 'dumps')))
    assert set(dirs[1]) == set(gh_repos)

    dm.clone_gh_repos('mggg-states', 'orgs', 
                      'https://github.com/mggg-states/CT-shapefiles.git', 
                      os.path.join('tests', 'dumps2'))
    dirs = next(os.walk(os.path.join('tests', 'dumps2'))) 
    assert set(dirs[1]) == {'CT-shapefiles.git'}

    dm.clone_gh_repos('mggg-states', 'orgs', 
                      ['https://github.com/mggg-states/AZ-shapefiles.git', 
                       'https://github.com/mggg-states/HI-shapefiles.git'], 
                      os.path.join('tests', 'dumps2'))
    dirs = next(os.walk(os.path.join('tests', 'dumps2'))) 
    assert set(dirs[1]) == {'CT-shapefiles.git', 'AZ-shapefiles.git', 
                            'HI-shapefiles.git'}


def test_list_files_of_type():
    with pytest.raises(Exception):
        dm.list_files_of_type(1)

    files = dm.list_files_of_type('description')
    ds = descriptions.copy()
    ds.append('./tests/dumps2/AZ-shapefiles.git/.git/description')
    ds.append('./tests/dumps2/CT-shapefiles.git/.git/description')
    ds.append('./tests/dumps2/HI-shapefiles.git/.git/description')
    assert set(files) == set(ds)

    files = dm.list_files_of_type('.q;weoifh0[238ubfasdf')
    assert files == []

    files = dm.list_files_of_type(['description', '.html'],
                                  os.path.join('tests', 'dumps'))
    assert files.sort() == (descriptions + htmls).sort()

    files = dm.list_files_of_type('description', 
                                  os.path.join('tests', 'dumps'))
    descriptions.remove('./.git/description')
    descrs = [d.lstrip('./') for d in descriptions]
    assert set(files) == set(descrs)

    files = dm.list_files_of_type('.gitignore', exclude_hidden = True)
    assert files == []

    files = dm.list_files_of_type('.gitignore', exclude_hidden = False)
    assert files == gitignores


def test_get_keys_by_category(): # test passing list of categories, try numbers
    with open(standards_path) as json_file:
        standards_raw = json.load(json_file)
    with pytest.raises(Exception):
        dne = dm.get_keys_by_category(standards_raw, '-1293urnpef13qewf')
    with pytest.raises(Exception):
        numbered = dm.get_keys_by_category(
        {1 : {9: 'asdf'}, 2 : {8: 'fdsa'}}, 1)
    with pytest.raises(Exception):
        xs = dm.get_keys_by_category(
            {'foo' : [1, 2, {'fdaa : asdf'}]}, 'foo')

    numbered = dm.get_keys_by_category(
        {1 : [{9: 'asdf'}], 2 : [{8: 'fdsa'}]}, 1)
    assert numbered == [9]

    parties = dm.get_keys_by_category(standards_raw, 'parties')
    assert parties == ['D', 'R', 'L', 'G', 'I', 'U']

    xs = dm.get_keys_by_category(
        {'[1, 2, 3]': ['asdf', 'fdaa'],
         '[4, 5, 6]': [{'fdas': 'fdsa'}, {'hjkl' : 'hjkl'}],
         'foo': [{'bar': 'bar'}]}, '[1, 2, 3]')
    assert xs == ['a', 's', 'd', 'f', 'f', 'd', 'a', 'a']

    xs = dm.get_keys_by_category(
        {'[1, 2, 3]': ['asdf', 'fdaa'],
         '[4, 5, 6]': [{'fdas': 'fdsa'}, {'hjkl' : 'hjkl'}],
         'foo': [{'bar': 'bar'}]}, '[4, 5, 6]')
    assert xs == ['fdas', 'hjkl']

    xs = dm.get_keys_by_category(
        {'[1, 2, 3]': [[1, 2, 3], {'fdaa' : 'asdf'}],
         '[4, 5, 6]': [{'fdas': 'fdsa'}, {'hjkl' : 'hjkl'}],
         'foo': [{'bar': 'bar'}]}, '[1, 2, 3]')
    assert xs == [1, 2, 3, 'fdaa']
    
    xs = dm.get_keys_by_category(
        {'category1' : [['key1']],
         'category2' : [['key2'], {'key3': 'value3'}]}, 
         ['category1', 'category2'])
    assert xs == ['key1', 'key2', 'key3']


def test_remove_repos():
    with pytest.raises(Exception):
        dm.remove_repos('XGx2ePfMTt3jbQEGWCzCHaRzWpC6Vz7qY48VY')

    dm.remove_repos(os.path.join('tests', 'dumps'))
    dirs = next(os.walk(os.path.join('tests', 'dumps')))
    assert not any(list(map(lambda x, y: x == y, set(dirs[1]), set(gh_repos))))

    dm.remove_repos(os.path.join('tests', 'dumps2'))
    dirs = next(os.walk(os.path.join('tests', 'dumps2')))
    assert not any(list(map(lambda x, y: x == y, set(dirs[1]),
                            {'CT-shapefiles.git', 'AZ-shapefiles.git', 
                             'HI-shapefiles.git'})))

    path_to_ak_shp = os.path.join('tests', 'dumps', 'AK-shapefiles.git')
    dm.clone_gh_repos('mggg-states', 'orgs', 
        )
    assert 'AK-shapefiles.git/README.md' in \
            dm.list_files_of_type('.md', path_to_ak_shp)
    dm.remove_repos(path_to_ak_shp)
    with pytest.raises(FileNotFoundError):
        xs = dm.list_files_of_type('.md', path_to_ak_shp)


    dm.remove_repos(os.path.join('tests', 'dumps')) # should not raise anything

