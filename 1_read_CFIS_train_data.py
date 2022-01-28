#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 01:20:29 2022

@author: Javier Alejandro Acevedo Barroso
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.io import fits
import os


#%%Reading challenge catalogue

# Path to the downloaded files
data_path="./Data/"  # To be adjusted on your machine
lenses_path = "new_training"
nonlenses_path = "PS1trainingset"

lenses_list = np.array(os.listdir(data_path+lenses_path))
nonlenses_list = np.array(os.listdir(data_path+nonlenses_path))
names = np.append(lenses_list,nonlenses_list)


classifications = np.zeros((len(lenses_list)+len(nonlenses_list)))
classifications[:len(lenses_list)] += 1


data = Table()
data["name"] = names
data["classification"] = classifications

#%%
ims = np.zeros((len(names), 44, 44))

particular_path = dict()
particular_path[0] = nonlenses_path
particular_path[1] = lenses_path
for i, path in enumerate(names):
    # print(path)
    # print(classifications[i], names[i],i)
    # ims[i] = fits.getdata(os.path.join(data_path,
    #                particular_path[classifications[i]],names[i]))
    try: #easy way to find all the images that are not 44x44. Those were purged from the dataset.
        ims[i] = fits.getdata(os.path.join(data_path,
                   particular_path[classifications[i]],names[i]))
    except:
        print(names[i],i)
    
data['image'] = ims

# Path to export the data
export_path="./Data/"   # To be adjusted on your machine


# Export catalog as HDF5
data.write(export_path+'CFIS_training_data.hdf5', append=True, overwrite = True)

print("Done !")
