#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 23:32:09 2022

@author: Javier Alejandro Acevedo Barroso
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.io import fits
import os

#%%

from astropy.table import Table

export_path="./Data"
# Loads the table created in the previous section
d = Table.read(os.path.join(export_path,'CFIS_data.hdf5'))

size = 44
#%%

# We use the full set for training,
# as we can test on the independent challenge testing set

from numpy.random import default_rng

rng = default_rng()
numbers = rng.choice(len(d), size=len(d), replace=False)

#%%
from sklearn.model_selection import train_test_split

X = np.array(d['image'])[numbers].reshape((-1,1,size,size))
y = np.array(d['classification'])[numbers].reshape((-1,1))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.15)

#%%

# # Clipping and scaling parameters applied to the data as preprocessing
# vmin=-1e-9
# vmax=1e-9
# scale=100

# mask = np.where(x == 100)
# mask_val = np.where(xval == 100)

# x[mask] = 0
# xval[mask_val] = 0

# # Simple clipping and rescaling the images
# x = np.clip(x, vmin, vmax)/vmax * scale
# xval = np.clip(xval, vmin, vmax)/vmax * scale 

from sklearn.preprocessing import scale


X_train = (X_train - np.mean(X_train)) / np.std(X_train)
X_val = (X_val - np.mean(X_val)) / np.std(X_val)
X_test = (X_test - np.mean(X_test)) / np.std(X_test) #The example uses kind of a MinMax scaling. TODO: to try that.

#%%

from deeplens.resnet_classifier import deeplens_classifier

#%%

model = deeplens_classifier(learning_rate=0.001,  # Initial learning rate
                          learning_rate_steps=3,  # Number of learning rate updates during training
                          learning_rate_drop=0.1, # Amount by which the learning rate is updated
                          batch_size=128,         # Size of the mini-batch
                          n_epochs=5)           # Number of epochs for training





model.fit(X_train,y_train,X_val,y_val) # Train the model, the validation set is provided for evaluation of the model









