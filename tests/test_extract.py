from shapely.geometry import Point
import pandas as pd
import geopandas as gpd

from context import gdutils
from gdutils.extract import ExtractTable

import pytest

#########################################
# Regression Tests                      #
#########################################

def test_constructor():
    et = ExtractTable()

    with pytest.raises(Exception):
        et.value = 'fail'

#===============================================

def run_tests():
    print('et = ExtractTable()')
    et = ExtractTable()
    print('infile = ', et.infile)
    print('outfile = ', et.outfile)
    print('column = ', et.column)
    print('value = ', et.value)
    print()

    try:
        et.value = 'fail'
    except Exception as e:
        print('Expected failure:', e)
    
    try:
        et.column = 'fail'
    except Exception as e:
        print('Expected failure:', e)

    try:
        et.infile = "tests/inputs/asdf"
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        extracted = et.extract()
    except Exception as e:
        print('Expected failure.', e)
    print()

    et.infile = "tests/inputs/test1.csv"

    try:
        et.value = "sdf"
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et.infile = "asdf/asdf"
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et.column = "col"
    except Exception as e:
        print('Expected failure.', e)

    print(et.extract())
    print()

    et.column = "col1"
    
    try:
        et.value = "fda"
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et.column = "col"
    except Exception as e:
        print('Expected failure.', e)
    
    try:
        et.value = "fda"
    except Exception as e:
        print('Expected failure.', e)

    print(et.extract())
    print()

    et.value = "c"
    print(et.extract())
    print()


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
run_tests()
run_tests2()
run_tests3()
run_tests4()
run_tests5()
#     run_tests6()
# except Exception as e:
#     print('failed:', e)

# run_tests7()



