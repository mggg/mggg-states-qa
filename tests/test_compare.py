import numpy as np
import pandas as pd
import geopandas as gpd

from context import gdutils
from gdutils.compare import CompareTables


#########################################
# Regression Test Inputs                #
#########################################
mggg_file = 'tests/inputs/CT_precincts.zip'
    # pulled from github.com/mggg-states/CT-shapefiles

medsl_file = 'tests/inputs/medsl18_ct.csv'
    # pulled from github.com/MEDSL/2018-elections-official/
    # source file: precinct_2018.zip
    # file used in test contains a subtable of CT specific data extracted
    # from precinct_2018.zip using the ``gdutils.extract``` module

mggg_gdf = ExtractTable(mggg_file).extract()
medsl_df = pd.read_csv(medsl_file)
medsl_df = medsl_df.pivot_table(index='precinct', 
                                columns=['office', 'party'], 
                                values='votes')

#########################################
# Regression Tests                      #
#########################################

