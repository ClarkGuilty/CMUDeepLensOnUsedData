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

#%%

from astropy.table import Table

export_path="./Data"
# Loads the table created in the previous section
d = Table.read(os.path.join(export_path,'CFIS_training_data.hdf5')) #Data Elodie used to train the original network.

real_d = Table.read(os.path.join(export_path,'CFIS_real_data_1.hdf5')) #Data classified with such network (chunk 1).


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
X_real = np.array(real_d['image']).reshape((-1,1,size,size))
X_real = (X_real - np.mean(X_real)) / np.std(X_real)
#%%
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
                          n_epochs=1)           # Number of epochs for training





model.fit(X_train,y_train,X_val,y_val) # Train the model, the validation set is provided for evaluation of the model

#%%
model.save('deeplens_params.npy')
#%%
y_real = model.predict_proba(X_real)
real_d["classification"] = y_real
print("found",np.sum(y_real > 0.5),"lenses.")
# real_d.write(export_path+'CFIS_real_data_classified.hdf5', append=True, overwrite = True)
real_d["classification"] = real_d["classification"].reshape(-1)
df = real_d[["name","classification"]].to_pandas()
df.to_csv("classified_1.csv")


#%%

print(model.eval_purity_completeness(X_test,y_test))
#%%
tpr,fpr,th = model.eval_ROC(X_test,y_test)
plt.title('ROC on Test set')
plt.plot(fpr,tpr)
plt.xlabel('FPR'); plt.ylabel('TPR')
plt.xlim(0,0.35); plt.ylim(0.70,1.)
plt.grid('on')

plt.savefig("ROC_test_set.png")


#%%


#%%
# array_orig = np.array(model.save('deeplens_params.npy'))
# #%%
# model1 = deeplens_classifier(learning_rate=0.001,  # Initial learning rate
#                           learning_rate_steps=3,  # Number of learning rate updates during training
#                           learning_rate_drop=0.1, # Amount by which the learning rate is updated
#                           batch_size=128,         # Size of the mini-batch
#                           n_epochs=5)           # Number of epochs for training

# array_restore = np.array(model1.load("deeplens_params.npy",X_train,y_train))
# #%%
# results = 0
# for i in range(len(array_orig)):
#     results += (array_orig[i] != array_restore[i]).all()
    
#     #%%

# print(model1.eval_purity_completeness(X_test,y_test))

# #%%
# model1.save("rip.npy")













