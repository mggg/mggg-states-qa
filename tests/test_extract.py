import pandas as pd
import geopandas as gpd
import numpy as np
from pathlib import PosixPath
import os

import pytest

from context import gdutils
from gdutils.extract import ExtractTable


#########################################
# Regression Test Inputs                #
#########################################

good_inf1 = "tests/inputs/test1.csv"
good_col1a = "col1"
good_col1b = "col2"
good_val1a = "c"
good_val1b = '5'
good_vals1a = ['a', 'c']
full_cols1 = ['field_1', 'col1', 'col2']
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
    et = ExtractTable()

    assert et.infile is None
    assert et.outfile is None
    assert et.column is None 
    assert et.value is None

    with pytest.raises(Exception):
        extracted = et.extract()


def test_constructor_errors():
    with pytest.raises(Exception):
        et = ExtractTable(bad_inf)
    with pytest.raises(Exception):
        et = ExtractTable(good_inf1, None, bad_col)
    with pytest.raises(Exception):
        et = ExtractTable(good_inf1, None, bad_col, bad_val)
    with pytest.raises(Exception):
        et = ExtractTable(good_inf1, None, good_col1a, bad_val)


def test_constructor():
    et = ExtractTable(good_inf1)
    assert et.infile == good_inf1
    assert et.outfile is None
    assert et.column is None 
    assert et.value is None

    et = ExtractTable(good_inf1, good_out)
    assert et.infile == good_inf1
    assert et.outfile == PosixPath(good_out)
    assert et.column is None 
    assert et.value is None

    et = ExtractTable(good_inf1, good_out, good_col1a)
    assert et.infile == good_inf1
    assert et.outfile == PosixPath(good_out)
    assert et.column == good_col1a
    assert et.value is None

    et = ExtractTable(good_inf1, good_out, good_col1a, good_val1a)
    assert et.infile == good_inf1
    assert et.outfile == PosixPath(good_out)
    assert et.column == good_col1a
    assert et.value == good_val1a

    et = ExtractTable(good_inf1, None, good_col1a)
    assert et.infile == good_inf1
    assert et.outfile == None
    assert et.column == good_col1a
    assert et.value == None

    et = ExtractTable(good_inf1, column=good_col1a)
    assert et.infile == good_inf1
    assert et.outfile == None
    assert et.column == good_col1a
    assert et.value == None

    et = ExtractTable(good_inf1, column=good_col1a, value=good_val1a)
    assert et.infile == good_inf1
    assert et.outfile == None
    assert et.column == good_col1a
    assert et.value == good_val1a

    et = ExtractTable(good_inf1, None, good_col1a, good_vals1a)
    assert et.infile == good_inf1
    assert et.outfile == None
    assert et.column == good_col1a
    assert et.value == good_vals1a


def test_infile():
    et = ExtractTable()

    et.infile = good_inf1
    assert et.infile == good_inf1

    with pytest.raises(Exception):
        et.value = good_val1a
    with pytest.raises(Exception):
        et.column = bad_col
    with pytest.raises(Exception):
        et.infile = bad_inf
    with pytest.raises(Exception):
        et.infile = good_inf2
    
    extract = et.extract()


def test_column():
    et = ExtractTable()
    et.infile = good_inf1

    et.column = good_col1a
    assert et.column == good_col1a

    with pytest.raises(Exception):
        et.value = bad_val
    with pytest.raises(Exception):
        et.column = bad_col
    
    extract = et.extract()


def test_value():
    et = ExtractTable()
    et.infile = good_inf1
    et.column = good_col1a

    et.value = good_val1a
    assert et.value == good_val1a

    et.value = 'b'
    assert et.value == 'b'

    extract = et.extract()


def test_outfile():
    et = ExtractTable(good_inf1)

    et.outfile = good_out
    assert et.outfile == PosixPath(good_out)

    et.outfile = dne_out
    assert et.outfile == PosixPath(dne_out)


def test_setters_2():
    et = ExtractTable()
    et.infile = good_inf1
    et.column = good_col1a
    et.value = good_val1a

    assert et.column == good_col1a
    assert et.value == good_val1a
    
    et.column = good_col1b
    assert et.column == good_col1b
    assert et.value is None

    et.value = good_val1b
    assert et.value == good_val1b
    
    et2 = ExtractTable()
    et2.infile = good_inf2
    et2.column = good_col2
    et2.value = good_val2

    assert et2.infile == good_inf2
    assert et2.column == good_col2 
    assert et2.value == good_val2


def test_read_file_errors():
    with pytest.raises(Exception):
        et = ExtractTable.read_file()
    with pytest.raises(Exception): 
        et = ExtractTable.read_file(bad_inf)
    with pytest.raises(Exception):
        et = ExtractTable.read_file(column=good_col1a, value=good_val1a)
    with pytest.raises(Exception):
        et = ExtractTable.read_file(good_inf1, column=bad_col)
    with pytest.raises(Exception):
        et = ExtractTable.read_file(good_inf1, value=good_val1a)
    with pytest.raises(Exception):
        et = ExtractTable.read_file(
                good_inf1, column=good_col1a, value=bad_val)
    with pytest.raises(Exception):
        et = ExtractTable.read_file(bad_inf, column=bad_col, value= bad_val)
    

def test_read_file():
    et = ExtractTable.read_file(good_inf1)
    assert et.infile == good_inf1
    assert et.outfile is None
    assert et.column is None
    assert et.value is None

    et = ExtractTable.read_file(good_inf1, good_col1a)
    assert et.infile == good_inf1
    assert et.outfile == None
    assert et.column == good_col1a
    assert et.value is None

    et = ExtractTable.read_file(good_inf1, good_col1a, good_val1a)
    assert et.infile == good_inf1
    assert et.outfile == None
    assert et.column == good_col1a
    assert et.value == good_val1a

    et = ExtractTable.read_file(good_inf1, good_col1a, good_vals1a)
    assert et.infile == good_inf1
    assert et.outfile == None
    assert et.column == good_col1a
    assert et.value == good_vals1a

    et = ExtractTable.read_file(good_inf2, good_col2, good_val2)
    assert et.infile == good_inf2
    assert et.outfile == None
    assert et.column == good_col2
    assert et.value == good_val2


def test_list_columns():
    et = ExtractTable()
    
    with pytest.raises(Exception):
        cols = et.list_columns()

    et = ExtractTable.read_file(good_inf1)
    cols = et.list_columns()
    assert type(cols) == np.ndarray
    assert (cols == np.array(full_cols1)).all()


    et = ExtractTable.read_file(good_inf2)
    cols = et.list_columns()
    assert type(cols) == np.ndarray
    assert (cols == np.array(full_cols2, dtype=object)).all()


def test_list_values():
    et = ExtractTable()

    with pytest.raises(Exception):
        cols = et.list_values()
    
    et.infile = good_inf1
    
    vals = et.list_values(good_col1a)
    assert type(vals) == np.ndarray
    assert (vals == np.array(full_vals1)).all()
    
    vals = et.list_values(good_col1a, unique=True)
    assert type(vals) == np.ndarray
    assert set(vals) == set(np.unique(np.array(full_vals1, dtype=object)))

    et.column = good_col1b

    vals = et.list_values(good_col1a)
    assert type(vals) == np.ndarray
    assert (vals == np.array(full_vals1)).all()
    
    vals = et.list_values(good_col1a, unique=True)
    assert type(vals) == np.ndarray
    assert set(vals) == set(np.unique(np.array(full_vals1, dtype=object)))

    et.column = good_col1a

    vals = et.list_values()
    assert type(vals) == np.ndarray
    assert (vals == np.array(full_vals1)).all()

    vals = et.list_values(unique=True)
    assert type(vals) == np.ndarray
    assert set(vals) == set(np.unique(np.array(full_vals1, dtype=object)))


def test_extract():
    et = ExtractTable(good_inf1)
    gdf1 = gpd.read_file(good_inf1)

    extract = et.extract()
    assert type(extract) == gpd.GeoDataFrame
    assert extract.equals(gdf1)

    et.column = good_col1a
    gdf1 = gdf1.set_index(good_col1a)
    extract = et.extract()
    assert type(extract) == gpd.GeoDataFrame
    assert extract.equals(gdf1)

    et.value = good_val1a
    gdf1 = gpd.GeoDataFrame(gdf1.loc[good_val1a])
    extract = et.extract()
    assert type(extract) == gpd.GeoDataFrame
    assert extract.equals(gdf1)


def test_extract_to_file():
    del_outs()

    et = ExtractTable(good_inf1, good_out)

    et.extract_to_file()
    assert os.path.isfile(good_out)

    et.outfile = dne_out
    assert not os.path.isfile(dne_out)
    assert not os.path.isdir(dne_dir)
    et.extract_to_file()
    assert os.path.isfile(dne_out)

    del_outs()


# To test, remove "no" prefix from function name and insert path to large file
def notest_large(): 
    large_file = ''
    et = ExtractTable(large_file, 'tests/dumps/large.zip', column='NAME10')
    et.extract_to_file()


