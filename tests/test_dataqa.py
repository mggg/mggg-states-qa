import numpy as np
import pandas as pd
import geopandas as gpd

import pytest

import gdutils.extract as et
import gdutils.dataqa as dq

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

mggg_gdf = et.ExtractTable(mggg_file).extract()

medsl_df = pd.read_csv(medsl_file)
medsl_df = medsl_df.pivot_table(index='precinct', 
                                columns=['office', 'party'], 
                                values='votes')
medsl_df.columns = [' '.join(col).strip() for col in medsl_df.columns.values]
medsl_df.to_csv('tests/inputs/medsl18_ct_clean.csv')



#########################################
# Regression Tests                      #
#########################################

