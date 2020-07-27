import pandas as pd
import geopandas as gpd
import numpy as np
from pathlib import PosixPath
import os

import pytest

import gdutils.extract as et


#########################################
# Regression Test Inputs                #
#########################################

good_inf1 = "tests/inputs/test1.csv"
good_col1a = "col1"
good_col1b = "col2"
good_val1a = "c"
good_val1b = '5'
good_vals1a = ['a', 'c']
full_cols1 = ['Unnamed: 0', 'col1', 'col2']
full_vals1 = ['a', 'c', 'c', 'c', 'b']

good_inf2 = "tests/inputs/test2.csv"
good_col2 = "featurecla"
good_val2 = "Country"
full_cols2 = ['Unnamed: 0', 'scalerank', 'featurecla', 'geometry']

good_out = "tests/dumps/dump"
dne_dir = "tests/dumps/dne"
dne_out = dne_dir + "/dump"

bad_inf = "this is a bad infile path"
bad_val = "this is a bad value"
bad_col = "this is a bad column"

zip_inf = "tests/inputs/CT_precincts.zip"

def del_outfile(outfile):
    if os.path.exists(outfile):
        try:
            os.remove(outfile)
        except:
            os.rmdir(outfile)

def del_outs():
    del_outfile(good_out)
    del_outfile(dne_out)
    del_outfile(dne_dir)


#########################################
# Regression Tests                      #
#########################################

def test_empty_constructor():
    test_et = et.ExtractTable()

    assert test_et.infile is None
    assert test_et.outfile is None
    assert test_et.column is None 
    assert test_et.value is None

    with pytest.raises(Exception):
        extracted = test_et.extract()


def test_constructor_errors():
    with pytest.raises(Exception):
        test_et = et.ExtractTable(bad_inf)
    with pytest.raises(Exception):
        test_et = et.ExtractTable(good_inf1, None, bad_col)
    with pytest.raises(Exception):
        test_et = et.ExtractTable(good_inf1, None, bad_col, bad_val)
    with pytest.raises(Exception):
        test_et = et.ExtractTable(good_inf1, None, good_col1a, bad_val)


def test_constructor():
    test_et = et.ExtractTable(good_inf1)
    assert test_et.infile == good_inf1
    assert test_et.outfile is None
    assert test_et.column is None 
    assert test_et.value is None

    test_et = et.ExtractTable(good_inf1, good_out)
    assert test_et.infile == good_inf1
    assert test_et.outfile == PosixPath(good_out)
    assert test_et.column is None 
    assert test_et.value is None

    test_et = et.ExtractTable(good_inf1, good_out, good_col1a)
    assert test_et.infile == good_inf1
    assert test_et.outfile == PosixPath(good_out)
    assert test_et.column == good_col1a
    assert test_et.value is None

    test_et = et.ExtractTable(good_inf1, good_out, good_col1a, good_val1a)
    assert test_et.infile == good_inf1
    assert test_et.outfile == PosixPath(good_out)
    assert test_et.column == good_col1a
    assert test_et.value == good_val1a

    test_et = et.ExtractTable(good_inf1, None, good_col1a)
    assert test_et.infile == good_inf1
    assert test_et.outfile == None
    assert test_et.column == good_col1a
    assert test_et.value == None

    test_et = et.ExtractTable(good_inf1, column=good_col1a)
    assert test_et.infile == good_inf1
    assert test_et.outfile == None
    assert test_et.column == good_col1a
    assert test_et.value == None

    test_et = et.ExtractTable(good_inf1, column=good_col1a, value=good_val1a)
    assert test_et.infile == good_inf1
    assert test_et.outfile == None
    assert test_et.column == good_col1a
    assert test_et.value == good_val1a

    test_et = et.ExtractTable(good_inf1, None, good_col1a, good_vals1a)
    assert test_et.infile == good_inf1
    assert test_et.outfile == None
    assert test_et.column == good_col1a
    assert test_et.value == good_vals1a


def test_infile():
    test_et = et.ExtractTable()

    test_et.infile = good_inf1
    assert test_et.infile == good_inf1

    with pytest.raises(Exception):
        test_et.value = good_val1a
    with pytest.raises(Exception):
        test_et.column = bad_col
    with pytest.raises(Exception):
        test_et.infile = bad_inf
    with pytest.raises(Exception):
        test_et.infile = good_inf2
    
    extract = test_et.extract()

    with pytest.raises(Exception):
        test_et.infile = zip_inf
    
    test_et2 = et.ExtractTable()
    test_et2.infile = zip_inf

    with pytest.raises(Exception):
        test_et.value = good_val1a
    with pytest.raises(Exception):
        test_et.column = bad_col
    with pytest.raises(Exception):
        test_et.infile = bad_inf
    with pytest.raises(Exception):
        test_et.infile = good_inf2
    
    extract = test_et2.extract()


def test_column():
    test_et = et.ExtractTable()
    test_et.infile = good_inf1

    test_et.column = good_col1a
    assert test_et.column == good_col1a

    with pytest.raises(Exception):
        test_et.value = bad_val
    with pytest.raises(Exception):
        test_et.column = bad_col
    
    extract = test_et.extract()


def test_value():
    test_et = et.ExtractTable()
    test_et.infile = good_inf1
    test_et.column = good_col1a

    test_et.value = good_val1a
    assert test_et.value == good_val1a

    test_et.value = 'b'
    assert test_et.value == 'b'

    extract = test_et.extract()


def test_outfile():
    test_et = et.ExtractTable(good_inf1)

    test_et.outfile = good_out
    assert test_et.outfile == PosixPath(good_out)

    test_et.outfile = dne_out
    assert test_et.outfile == PosixPath(dne_out)


def test_setters_2():
    test_et = et.ExtractTable()
    test_et.infile = good_inf1
    test_et.column = good_col1a
    test_et.value = good_val1a

    assert test_et.column == good_col1a
    assert test_et.value == good_val1a
    
    test_et.column = good_col1b
    assert test_et.column == good_col1b
    assert test_et.value is None

    test_et.value = good_val1b
    assert test_et.value == good_val1b
    
    test_et2 = et.ExtractTable()
    test_et2.infile = good_inf2
    test_et2.column = good_col2
    test_et2.value = good_val2

    assert test_et2.infile == good_inf2
    assert test_et2.column == good_col2 
    assert test_et2.value == good_val2


def test_read_file_errors():
    with pytest.raises(Exception):
        test_et = et.read_file()
    with pytest.raises(Exception): 
        test_et = et.read_file(bad_inf)
    with pytest.raises(Exception):
        test_et = et.read_file(column=good_col1a, value=good_val1a)
    with pytest.raises(Exception):
        test_et = et.read_file(good_inf1, column=bad_col)
    with pytest.raises(Exception):
        test_et = et.read_file(good_inf1, value=good_val1a)
    with pytest.raises(Exception):
        test_et = et.read_file(
                good_inf1, column=good_col1a, value=bad_val)
    with pytest.raises(Exception):
        test_et = et.read_file(bad_inf, column=bad_col, value= bad_val)
    

def test_read_file():
    test_et = et.read_file(good_inf1)
    assert test_et.infile == good_inf1
    assert test_et.outfile is None
    assert test_et.column is None
    assert test_et.value is None

    test_et = et.read_file(good_inf1, good_col1a)
    assert test_et.infile == good_inf1
    assert test_et.outfile == None
    assert test_et.column == good_col1a
    assert test_et.value is None

    test_et = et.read_file(good_inf1, good_col1a, good_val1a)
    assert test_et.infile == good_inf1
    assert test_et.outfile == None
    assert test_et.column == good_col1a
    assert test_et.value == good_val1a

    test_et = et.read_file(good_inf1, good_col1a, good_vals1a)
    assert test_et.infile == good_inf1
    assert test_et.outfile == None
    assert test_et.column == good_col1a
    assert test_et.value == good_vals1a

    test_et = et.read_file(good_inf2, good_col2, good_val2)
    assert test_et.infile == good_inf2
    assert test_et.outfile == None
    assert test_et.column == good_col2
    assert test_et.value == good_val2


def test_list_columns():
    test_et = et.ExtractTable()
    
    with pytest.raises(Exception):
        cols = test_et.list_columns()

    test_et = et.read_file(good_inf1)
    cols = test_et.list_columns()
    assert type(cols) == np.ndarray
    assert (cols == np.array(full_cols1)).all()

    test_et = et.read_file(good_inf2)
    cols = test_et.list_columns()
    assert type(cols) == np.ndarray
    assert (cols == np.array(full_cols2, dtype=object)).all()


def test_list_values():
    test_et = et.ExtractTable()

    with pytest.raises(Exception):
        cols = test_et.list_values()
    
    test_et.infile = good_inf1
    
    vals = test_et.list_values(good_col1a)
    assert type(vals) == np.ndarray
    assert (vals == np.array(full_vals1)).all()
    
    vals = test_et.list_values(good_col1a, unique=True)
    assert type(vals) == np.ndarray
    assert set(vals) == set(np.unique(np.array(full_vals1, dtype=object)))

    test_et.column = good_col1b

    vals = test_et.list_values(good_col1a)
    assert type(vals) == np.ndarray
    assert (vals == np.array(full_vals1)).all()
    
    vals = test_et.list_values(good_col1a, unique=True)
    assert type(vals) == np.ndarray
    assert set(vals) == set(np.unique(np.array(full_vals1, dtype=object)))

    test_et.column = good_col1a

    vals = test_et.list_values()
    assert type(vals) == np.ndarray
    assert (vals == np.array(full_vals1)).all()

    vals = test_et.list_values(unique=True)
    assert type(vals) == np.ndarray
    assert set(vals) == set(np.unique(np.array(full_vals1, dtype=object)))


def test_extract():
    test_et = et.ExtractTable(good_inf1)
    gdf1 = gpd.read_file(good_inf1)
    gdf1 = gdf1.rename(columns={'field_1' : 'Unnamed: 0'})
        # Note: gpd has inconsistent naming compared with pd

    extract = test_et.extract()
    assert type(extract) == gpd.GeoDataFrame
    assert extract.equals(gdf1)

    test_et.column = good_col1a
    gdf1 = gdf1.set_index(good_col1a)
    extract = test_et.extract()
    assert type(extract) == gpd.GeoDataFrame
    assert extract.equals(gdf1)

    test_et.value = good_val1a
    gdf1 = gpd.GeoDataFrame(gdf1.loc[good_val1a])
    extract = test_et.extract()
    assert type(extract) == gpd.GeoDataFrame
    assert extract.equals(gdf1)


def test_extract_to_file():
    del_outs()

    test_et = et.ExtractTable(good_inf1, good_out)

    test_et.extract_to_file()
    assert os.path.isfile(good_out)

    test_et.outfile = dne_out
    assert not os.path.isfile(dne_out)
    assert not os.path.isdir(dne_dir)
    test_et.extract_to_file()
    assert os.path.isfile(dne_out)

    del_outs()

def test_value_dtype_preservation():
    # To test, uncomment following and insert large non-geo tabular data
    # medsl_p18 = 'tests/inputs/precinct_2018/precinct_2018.csv'

    # pd_df = pd.read_csv(medsl_p18, encoding='ISO-8859-1')
    # et_df = pd.DataFrame(et.read_file(medsl_p18).extract())

    # assert all(list(map(
    #                 lambda x, y : x == y and \
    #                               pd_df[x].dtype == et_df[y].dtype,
    #                 pd_df.columns, et_df.columns)))
    
    gpd_gdf1 = gpd.read_file(good_inf1).rename(
                        columns={'field_1':'Unnamed: 0'})
    et_gdf1 = et.read_file(good_inf1).extract()

    assert all(list(map(
                    lambda x, y : x == y and \
                                  gpd_gdf1[x].dtype == et_gdf1[y].dtype,
                    gpd_gdf1.columns, et_gdf1.columns)))


# To test, remove "no" prefix from function name and insert path to large file
def notest_large(): 
    large_file = ''
    test_et = et.ExtractTable(large_file, 'tests/dumps/large.zip', 
                              column='NAME10')
    test_et.extract_to_file()

