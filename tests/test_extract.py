from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
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

good_inf2 = "tests/inputs/test2.csv"
good_col2 = "featurecla"
good_val2 = "Country"

good_out = "tests/dumps/dump"
dne_dir = "tests/dumps/dne"
dne_out = dne_dir + "/dump"

bad_inf1 = "this is a bad infile path"
bad_val1 = "this is a bad value"
bad_col1 = "this is a bad column"

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
        et.value = good_val1a
    with pytest.raises(Exception):
        et.column = good_col1a
    with pytest.raises(Exception):
        et.infile = bad_inf
    with pytest.raises(Exception):
        extracted = et.extract()


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
    et = ExtractTable()
    et.infile = good_inf1

    del_outs()

    et.outfile = good_out
    assert et.outfile == PosixPath(good_out)
    et.extract_to_file()
    assert os.path.isfile(good_out)

    et.outfile = dne_out
    assert et.outfile == PosixPath(dne_out)
    assert not os.path.isfile(dne_out)
    assert not os.path.isdir(dne_dir)
    et.extract_to_file()
    assert os.path.isfile(dne_out)

    del_outs()


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

    extract = et.extract()
    extract = et2.extract()



#===============================================

def run_tests2():
    try:
        et = ExtractTable.read_file()
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et = ExtractTable.read_file("asdf/asdf")
    except Exception as e:
        print('Expected failure.', e)

    try:
        et = ExtractTable.read_file(column=2, value='asdf')
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et = ExtractTable.read_file("tests/inputs/test1.csv", column="3")
    except Exception as e:
        print('Expected failure.', e) 

    try:
        et = ExtractTable.read_file("tests/inputs/test1.csv", value="3")
    except Exception as e:
        print('Expected failure.', e) 

    try:
        et = ExtractTable.read_file("tests/inputs/test1.csv", column="col1", value=3)
    except Exception as e:
        print('Expected failure.', e) 
    print()

    et = ExtractTable.read_file("tests/inputs/test1.csv")
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print(et.extract())
    print()


    et = ExtractTable.read_file("tests/inputs/test1.csv", column="col1")
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print(et.extract())
    print()

    et = ExtractTable.read_file("tests/inputs/test1.csv", column="col1", value="c")
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print(et.extract())
    print() 

    et = ExtractTable.read_file("tests/inputs/test1.csv", column="col1", value=['a', 'c'])
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print(et.extract())
    print()


def run_tests3():
    et = ExtractTable.read_file("tests/inputs/test1.csv")
    print(type(et.list_columns()))
    print(et.list_columns())
    print(et.extract())

    try:
        et.list_columns()
    except Exception as e:
        print("Expected failure.", e)
    print()
    
    print(type(et.list_values('field_1')))
    print(et.list_values('field_1'))
    print(et.list_values('field_1', unique=True))
    print()

    et.column = 'col1'
    print(type(et.list_values()))
    print(et.list_values())
    print(et.list_values(unique=True))
    print()

    print(type(et.list_values('geometry')))
    print(et.list_values('geometry'))
    print(et.list_values('geometry', unique=True))
    print()

def run_tests4():
    et = ExtractTable('tests/inputs/test1.csv', column="col2", value=['3', '5'])
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print(et.extract())
    print()

def run_tests5():
    #et = ExtractTable('nhgis0004_shapefile_tl2010_060_block_2010.zip')
    gdf = ExtractTable('tests/inputs/test1.csv').extract()
    print(type(gdf))
    et = ExtractTable(gdf)
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print(et.list_columns())
    print(et.list_values('col1', unique=True))
    print()

    et2 = ExtractTable(et.extract())
    print('infile = ', et2.infile)
    print('outfile = ', et2.outfile)
    print('column = ', et2.column)
    print('value = ', et2.value)
    print(et2.list_columns())
    print(et2.list_values('col1', unique=True))
    print()

    d = {'col1': ['name1', 'name2'], 'geometry': [Point(1,2), Point(2,1)]}
    gdf1 = gpd.GeoDataFrame(d, crs="EPSG:4326")
    et3 = ExtractTable(gdf1)
    print('infile = ', et3.infile)
    print('outfile = ', et3.outfile)
    print('column = ', et3.column)
    print('value = ', et3.value)
    print(et3.list_columns())
    et3.column = 'geometry'
    print(et3.list_values())
    print(et3.extract())
    print()

    df = pd.DataFrame(d)
    et4 = ExtractTable(df)
    print('infile = ', et3.infile)
    print('outfile = ', et3.outfile)
    print('column = ', et3.column)
    print('value = ', et3.value)
    print(et3.list_columns())
    print(et3.list_values())
    print(et3.extract())
    print()


# def run_tests6():
#     et = ExtractTable('../example-tests/inputs/example.csv')
#     gdf = et.extract()
#     print(gdf.head())
#     print(type(gdf['geometry'][0]))
#     et.extract_to_file('../dump/geo.shp')
#     print()

#     et2 = ExtractTable.read_file('test1.csv')
#     gdf2 = et2.extract()
#     print(gdf2.head())
#     print(type(gdf['geometry'][0]))
#     et2.extract_to_file('../dump/test1.csv')

# def run_tests7():
#     et = ExtractTable('../example-tests/inputs/example.zip')
#     print(et.extract().head())


#########################################
# Function Calls                        #
#########################################
# try:
# run_tests()
# run_tests2()
# run_tests3()
# run_tests4()
# run_tests5()
#     run_tests6()
# except Exception as e:
#     print('failed:', e)

# run_tests7()



