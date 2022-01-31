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
import pandas as pd

#%%


export_path="./Data"
# Loads the table created in the previous section
d = Table.read(os.path.join(export_path,'CFIS_training_data.hdf5')) #Data Elodie used to train the original network.



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
# X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.99)

#%%
X_train = (X_train - np.mean(X_train)) / np.std(X_train)
X_val = (X_val - np.mean(X_val)) / np.std(X_val)
X_test = (X_test - np.mean(X_test)) / np.std(X_test) #The example uses kind of a MinMax scaling. TODO: to try that.

#%%
from deeplens.resnet_classifier import deeplens_classifier

#%%

model = deeplens_classifier(learning_rate=0.001,  # Initial learning rate
                          learning_rate_steps=4,  # Number of learning rate updates during training
                          learning_rate_drop=0.1, # Amount by which the learning rate is updated
                          batch_size=256,         # Size of the mini-batch
                          n_epochs=100,            # Number of epochs for training
                          val_nepoch=10)          # Number of epochs before checking validation scores. 





model.fit(X_train,y_train,X_val,y_val) # Train the model, the validation set is provided for evaluation of the model

#%%
# model.save('deeplens_params.npy')
#%%
import time
# i = 0
for i in range(4):
    old_time = time.time()
    print('CFIS_real_data_'+str(i)+'.hdf5')
    X_real = Table.read(os.path.join(export_path,'CFIS_real_data_'+str(i)+'.hdf5')) #Data classified with such network (chunk 1).
    names = X_real["name"]
    X_real = np.array(X_real['image']).reshape((-1,1,size,size))
    X_real = (X_real - np.mean(X_real)) / np.std(X_real)
    print("heh")
    y_real = model.predict_proba(X_real)
    # y_real = np.random.rand(len(names))
    df = pd.DataFrame({"name": names, "classification": y_real})
    
    print("found",np.sum(y_real > 0.5),"candidates out of", len(y_real), "images.")
    df.to_csv(os.path.join("Classifications","classified_"+str(i)+".csv")) 
    
    # real_d["classification"] = y_real
    # print("found",np.sum(y_real > 0.5),"candidates out of", len(y_real), "images.")
    # # real_d.write(export_path+'CFIS_real_data_classified.hdf5', append=True, overwrite = True)
    # real_d["classification"] = real_d["classification"].reshape(-1)
    # df = real_d[["name","classification"]].to_pandas()
    # df.to_csv(os.path.join("Classifications","classified_"+str(i)+".csv")) 
    print(time.time()-old_time, (time.time()-old_time)/len(y_real))

#%%

print(model.eval_purity_completeness(X_test,y_test))
#%%
tpr,fpr,th = model.eval_ROC(X_test,y_test)
plt.title('ROC on Test set')
plt.plot(fpr,tpr)
plt.xlabel('FPR'); plt.ylabel('TPR')
plt.xlim(0,0.35); plt.ylim(0.70,1.)
plt.grid('on')

plt.savefig(os.path.join("Figures","ROC_test_set_only_flips.png"))

