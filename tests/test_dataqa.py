import numpy as np
import pandas as pd
import geopandas as gpd
import os
import json
import subprocess

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
medsl_df = pd.read_csv(os.path.join('tests', 'inputs', 'medsl18_ct_clean.csv'),
                                    encoding='ISO-8859-1')

standards_path = 'scripts/naming_convention.json'



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



#########################################
# Regression Tests                      #
#########################################

def test_compare_column_names():
    with pytest.raises(Exception):
        _, _ = dq.compare_column_names('asdf', ['asdf'])

    m, d = dq.compare_column_names(pd.DataFrame(), ['asdf'])
    assert m == set()
    assert d == set()

    standards = ['COL1', 'COL2', 'COL3']
    df = pd.DataFrame(data=[[1, 2, 3], [4, 5, 6]],
                      columns=['COL1', 'col2', 'COL3'])
    (matches, discrepancies) = dq.compare_column_names(df, standards)
    assert matches == {'COL1', 'COL3'}
    assert discrepancies == {'col2'}

    standards = []
    (matches, discrepancies) = dq.compare_column_names(df, standards)
    assert matches == set()
    assert discrepancies == {'COL1', 'COL3', 'col2'}

    subprocess.run(['git', 'clone', 
                    'https://github.com/mggg-states/AK-shapefiles.git',
                    'tests/dumps/AK-shapefiles.git'])

    standards = get_standards()
    (ak_matches, ak_discrepancies) = dq.compare_column_names(
            et.read_file(os.path.join('tests', 'dumps', 'AK-shapefiles.git',
                                      'AK_precincts.zip')).extract(), 
                         standards)
    assert ak_matches == {'USH14R', 'SEN16D', 'USH18D', '2MOREVAP', 'TOTPOP', 
                          'USH18R', 'SEN16L', 'GOV18R', 'GOV18D', 'USH16D', 
                          'PRES16L', 'PRES16G', 'SEN16R', 'BVAP', 'USH14D', 
                          'PRES16D', 'GOV18L', 'ASIANVAP', 'geometry', 
                          'USH16L', 'OTHERVAP', 'PRES16R', 'AMINVAP', 'VAP', 
                          'NHPIVAP', 'USH16R', 'HDIST', 'WVAP', 'USH14L'}
    assert ak_discrepancies == {'NAME', 'DISTRICT', 'ID', 'BLACK', '2MORE', 
                                'OTHER', 'WHITE', 'NHPI', 'PRES16C', 'AREA', 
                                'POPULATION', 'ASIAN', 'AMIN'}


def test_sum_column_values():
    ak_gdf = et.read_file(os.path.join('tests', 'dumps', 'AK-shapefiles.git',
                                       'AK_precincts.zip')).extract()
    with pytest.raises(Exception):
        totals = dq.sum_column_values(pd.DataFrame(), ['asdf'])
    with pytest.raises(Exception):
        totals = dq.sum_column_values(ak_gdf, ['geometry'])
    with pytest.raises(Exception):
        totals = dq.sum_column_values(ak_gdf, 'geometry')

    cols = ['COL1', 'COL3']
    df = pd.DataFrame(data=[[1, 2, 3], [4, 5, 6]],
                      columns=['COL1', 'COL2', 'COL3'])
    totals = dq.sum_column_values(df, cols)
    assert totals == [('COL1', 5), ('COL3', 9)]

    totals = dq.sum_column_values(ak_gdf, ['USH14R'])
    assert totals == [('USH14R', 102464)]

    totals = dq.sum_column_values(ak_gdf, ['PRES16D', 'PRES16G', 'PRES16L'])
    assert totals == [('PRES16D', 69097), ('PRES16G', 3782), 
                      ('PRES16L', 12004)]

    totals = dq.sum_column_values(medsl_df, ['Treasurer independent'])
    assert totals == [('Treasurer independent', 21149.54761904762)]

    totals = dq.sum_column_values(medsl_df, [])
    assert totals == []


def notest_compare_column_values(): # remove 'no' prefix once ready to test
    df1 = pd.DataFrame(data=[[1, 2, 3], [4, 5, 6]],
                       columns=['COL1', 'COL2', 'COL3'])
    df2 = pd.DataFrame(data=[[4, 5], [1, 2]],
                       columns=['col2', 'col1'])
    df3 = pd.DataFrame(data=[['asdf', 'fdsa'], ['foo', 'bar']],
                       columns=['c1', 'c2'])
    
    with pytest.raises(Exception):
        results = dq.compare_column_values(pd.DataFrame(), pd.DataFrame(),
                                           'asdf', 'asdf')
    with pytest.raises(Exception):
        results = dq.compare_column_values(pd.DataFrame(), df1, 'asdf', 'asdf')
    with pytest.raises(Exception):
        results = dq.compare_column_values(df1, df2, 'col2', 'COL1')
    with pytest.raises(Exception):
        results = dq.compare_column_values(df1, df2, df1.columns, df2.columns)
    with pytest.raises(Exception):
        results = dq.compare_column_values(df1, df2, ['COL1', 'COL2'], 
                                           ['col1', 'col2'], 1, 'adsf')
    with pytest.raises(Exception):
        results = dq.compare_column_values(df1, df2, 'COL1', 'col1', 1, -1)
    with pytest.raises(Exception):
        results = dq.compare_column_values(df1, df3, 'COL1', 'c1')
    with pytest.raises(Exception):
        results = dq.compare_column_values(df1, df2, 'COL1', 'col2', [0, 1], 1)
    with pytest.raises(Exception):
        results = dq.compare_column_values(df1, df2, 'COL1', 'col2', [0, 1], 
                                           [0, 5])
    
    results = dq.compare_column_values(df1, df2, 'COL1', 'col1')
    assert results == {'COL1-col1' : [('0-0', 0), ('1-1', 0)]}

    results = dq.compare_column_values(df1, df2, 'COL3', 'col2')
    assert results == {'COL1-col2' : [('0-0', 1), ('1-1', 5)]}

    results = dq.compare_column_values(df1, df2, ['COL1', 'COL2'], 
                                       ['col1', 'col2'])
    assert results == {'COL1-col1' : [('0-0', 0), ('1-1', 0)],
                       'COL2-col2' : [('0-0', 0), ('1-1', 0)]}

    results = dq.compare_column_values(df1, df2, 'COL1', 'col1', 0, 1)
    assert results == {'COL1-col1': [('0-1', 1)]}

    results = dq.compare_column_values(df1, df2, 'COL1', 'col1', [0, 1],
                                       [1, 0])
    assert results == {'COL1-col1': [('0-1', 1), ('1-0', 1)]}

    results = dq.compare_column_values(df1, df1, 'COL1', 'COL2', 0, 0)
    assert results == {'COL1-COL2': [('0-0', 1)]}

    results = dq.compare_column_values(mggg_gdf, medsl_df, 'AG18D', 
                                       'Attorney General democrat', 
                                       'Plainfield - DISTRICT 1-1-1a Town Hall',
                                       '1a Town Hall')
    (_, diff) = results['AG18D-Attorney General democrat'][0]
    ct_et = et.ExtractTable(mggg_gdf, column='PRECINCT', 
                            value='Plainfield - DISTRICT 1-1-1a Town Hall')
    assert diff == abs(ct_et.extract()['AG18D'] - 361.0)


def notest_compare_column_sum(): # remove 'no' prefix when ready to test
    pass # TODO


def test_remove_repos(): # for cleaning up test files
    dq.remove_repos(os.path.join('tests', 'dumps')) 

