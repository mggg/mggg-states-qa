import sys
sys.path.insert(1, '../')

from modules.extract import ExtractTable
from modules.compare import CompareTables
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd

#########################################
# Regression Tests                      #
#########################################

def run_tests():
    try:
        cmp = CompareTables()
    except Exception as e:
        print("Expected failure:", e)
    
    try:
        cmp = CompareTables(None)
    except Exception as e:
        print("Expected failure:", e)
    
    try:
        cmp = CompareTables(None)
    except Exception as e:
        print("Expected failure:", e)

#########################################
# Function Calls                        #
#########################################
run_tests()
