#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 23:32:09 2022

@author: Javier Alejandro Acevedo Barroso
"""
import warnings
warnings.simplefilter("ignore", UserWarning)


import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.io import fits
import os
import time

#%%Reading challenge catalogue

# Path to the downloaded files
data_path="./Data"  # To be adjusted on your machine
CFIS_path = "CFIS_real"
full_path = os.path.join(data_path,CFIS_path)

CFIS_folder_list = np.array(os.listdir(full_path))


#%%
# no_images = 0
# for folder in CFIS_folder_list[:586]:
#     no_images += len(os.listdir(os.path.join(data_path,CFIS_path,folder,"IMA")))

# no_folders_per_execution = 586
# total_no_images = 2322366
# no_images_per_iteration = 387061

# data = Table(names = ['name', 'classification', 'image'])

# data["name"] = CFIS_list
# data["classification"] = np.zeros(no_images)


#%% Cleaning the dataset from images with size different to 44x44 or that fail to load.

# ims = np.zeros((2, 44, 44),)
# wrong_dimensions = []

# j = 0
# old_time = time.time()
# for i, path in enumerate(CFIS_folder_list):
#     print(i,"/",len(CFIS_folder_list))
#     # print(classifications[i], names[i],i)
#     long_path = os.path.join(full_path,path,"IMA")
#     for file in os.listdir(long_path):
        
#         try: #easy way to find all the images that are not 44x44. Those are purged from the dataset.
#             image_data = fits.getdata(os.path.join(long_path,file))
#             try:
#                 ims[j] = image_data
#                 # names[j] = file.split(".")[0]
#                 # j += 1
#             except:
#                 print(file,i,image_data.shape)
#                 os.replace(os.path.join(long_path,file),
#                         os.path.join(data_path,'CFIS_bad_frames',file))
#         except:
#             print(file,i, "failed to load.")
#             # wrong_dimensions.append(file)
#             os.replace(os.path.join(long_path,file),
#                         os.path.join(data_path,'CFIS_bad_frames',file))

# print(time.time()-old_time)

#%% Actually loading the data.
no_maximum_folder_iterations = 4
no_folders_per_execution = 586
# no_folders_per_execution = 4

for folder_iteration in range(no_maximum_folder_iterations):
    data = Table(names = ['name', 'classification', 'image'])
    i_folder = folder_iteration * no_folders_per_execution
    
    no_images = 0
    for folder in CFIS_folder_list[i_folder : i_folder +  no_folders_per_execution]:
        no_images += len(os.listdir(os.path.join(data_path,CFIS_path,folder,"IMA")))
    print("folder iteration:", folder_iteration, ", no. images: ",no_images)
    
    j = 0
    j_max = no_images
    i = 0
    names = np.zeros(j_max,"U30")
    ims = np.zeros((j_max, 44, 44),)
    
    old_time = time.time()
    # for i, path in enumerate(CFIS_folder_list):
    while j < j_max:
        path = CFIS_folder_list[i_folder+i]
        # print(i,"/",len(CFIS_folder_list))
        # print(classifications[i], names[i],i)
        long_path = os.path.join(full_path,path,"IMA")
        for file in os.listdir(long_path):
            ims[j] = fits.getdata(os.path.join(long_path,file))
            names[j] = file.split(".")[0]
            j += 1
        i += 1
        
    data = Table([names,np.zeros(len(names)), ims],names = ['name', 'classification', 'image'])
    export_path="./Data/"   # To be adjusted on your machine
    
    
    # Export catalog as HDF5
    data.write(os.path.join(export_path,
                            'CFIS_real_data_'+str(folder_iteration)+'.hdf5'), append=True,
                               overwrite = True)
    print("iteration:", folder_iteration,", time:", time.time()-old_time)

print("Done !")
