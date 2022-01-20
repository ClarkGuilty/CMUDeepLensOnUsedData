#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 21:49:16 2022

@author: Javier Alejandro Acevedo Barroso
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.io import fits

#%%Reading challenge catalogue


# Path to export the data
export_path="./Data/"   # To be adjusted on your machine

from astropy.table import Table

# Loads the table created in the previous section
d = Table.read(export_path+'catalogs.hdf5', path='/ground')     # Path to be adjusted on your machine

#%%

# We use the full set for training,
# as we can test on the independent challenge testing set
# x = np.array(d['image']).reshape((-1,4,101,101))
# y = np.array(d['is_lens']).reshape((-1,1))

xtra = np.array(d['image'][:1000]).reshape((-1,4,101,101))
ytra = np.array(d['is_lens'][:1000]).reshape((-1,1))

# [Warning: We reuse the training set as our validation set,
# don't do that if you don't have an independent testing set]


xval = np.array(d['image'][15000:]).reshape((-1,4,101,101))
yval = np.array(d['is_lens'][15000:]).reshape((-1,1))

#%%

# Clipping and scaling parameters applied to the data as preprocessing
vmin=-1e-9
vmax=1e-9
scale=100

mask = np.where(xtra == 100)
mask_val = np.where(xval == 100)

xtra[mask] = 0
xval[mask_val] = 0

# Simple clipping and rescaling the images
xtra = np.clip(xtra, vmin, vmax)/vmax * scale
xval = np.clip(xval, vmin, vmax)/vmax * scale 

xtra[mask] = 0
xval[mask_val] = 0

#%%

# Illustration of a lens in the 4 bands provided
im = xtra[0].T
plt.subplot(221)
plt.imshow(im[:,:,0]); plt.colorbar()
plt.subplot(222)
plt.imshow(im[:,:,1]); plt.colorbar()
plt.subplot(223) 
plt.imshow(im[:,:,2]); plt.colorbar()
plt.subplot(224)
plt.imshow(im[:,:,3]); plt.colorbar()

#%%

from deeplens.resnet_classifier import deeplens_classifier

#%%

model = deeplens_classifier(learning_rate=0.001,  # Initial learning rate
                          learning_rate_steps=3,  # Number of learning rate updates during training
                          learning_rate_drop=0.1, # Amount by which the learning rate is updated
                          batch_size=128,         # Size of the mini-batch
                          n_epochs=5)           # Number of epochs for training





model.fit(xtra,ytra,xval,yval) # Train the model, the validation set is provided for evaluation of the model









