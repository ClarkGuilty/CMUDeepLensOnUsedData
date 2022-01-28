#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 09:57:07 2022

@author: Javier Alejandro Acevedo Barroso
"""
import warnings
warnings.simplefilter("ignore", UserWarning)


import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.io import fits
import os

#%%

from astropy.table import Table

export_path="./Data"
# Loads the table created in the previous section
# real_d = Table.read(os.path.join(export_path,'CFIS_real_data_1.hdf5')) #Data classified with such network.

#%%
import pandas as pd
real_d = Table.read(export_path+'CFIS_real_data_classified.hdf5')
#%%
# df = real_d.to_pandas(real_d[["name", "classification"]])
# real_d[["name", "classification"]].to_pandas()
# real_d["name"].shape
# real_d["classification"] = real_d["classification"].reshape(-1)
#%%
# df = pd.DataFrame({'name': real_d["name"],
#                    'classification': real_d["classification"].reshape(-1)})


# df.loc[df['classification'] > 0]
#%%

real_d["classification"] = real_d["classification"].reshape(-1)
df = real_d[["name","classification"]].to_pandas()
df.to_csv("classified_1.csv")































