#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 20:40:16 2020
@author: noahzr
"""

import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import elevation
import richdem as rd
import pandas as pd
import scipy
from scipy import stats
import cv2

matplotlib.rcParams['figure.figsize']=(8, 5.5)



#TODO: add image guided filter to heightmap or some Low pass filter that smoothes out heightmap roughness but preserves the terrain features

# testing by simply counting occurences of elements rounded to 90 deg, so in total 4 possible values
#TODO: add resolution clause (has to have 0.1 resolution, if not downsample array)
    
#TODO: add Kolmogorov Smirnov test to test the aspect values within analysis window agains uniform distribution    
  

#peaks = np.load('/Users/noahzr/Desktop/TerrainCharacterization/scripts/dem_part_guided.npy')
peaks = np.load('/Users/noahzr/Desktop/TerrainCharacterization/scripts/dem_interp2633_guided.npy')
# downsample to 0.05m resolution
peaks_1 = peaks[::5,::5]
test =  rd.rdarray(peaks_1, no_data = 0)
aspect = rd.TerrainAttribute(test, attrib='aspect')
rd.rdShow(aspect, axes=False, cmap='jet')
plt.show()


Z = np.zeros(peaks_1.shape)
nodata_val = -9990
deg_rounded = 90
kernel_size = 10

aspect = deg_rounded * np.around(np.true_divide(aspect,deg_rounded)) 
#aspect =  rd.rdarray(aspect, no_data = -9990)
#aspect[aspect == 360] = 0
#rd.rdShow(aspect, axes=False, cmap='jet')
#plt.show()


# Performing Kolmogorov-Smirnov test:
    
    
# 10 x 10 analysis set while rounding to aspects to 90 degrees
for coord, j in np.ndenumerate(aspect):
    if (min(coord) > int(kernel_size/2)) & (coord[0] < (peaks.shape[0] - int(kernel_size/2))) & (coord[1] < (peaks.shape[1] - int(kernel_size/2))):
        # dataset to be evaluated
        analysis_set = concatenate(aspect[(coord[0] - int(kernel_size/2)):(coord[0] + int(kernel_size/2)),(coord[1] - int(kernel_size/2)):(coord[1] + int(kernel_size/2))])
        # ignoring nodata values for computation
        analysis_set = np.delete(analysis_set, np.where(analysis_set == nodata_val))
        # only account for north direction once
        analysis_set[analysis_set == 360] = 0
        frequency = np.bincount(analysis_set.astype(int))
        frequency = np.delete(frequency, np.where(frequency == 0)) #TODO this also deletes the zero value incase zero indicates this aspect direction never appears within the kernel.. 
        
        if (frequency.shape[0] == 4):  #&  (min(frequency) > (analysis_set.shape[0] * 0.1))  &  (max(frequency) < (analysis_set.shape[0] * 0.9)):     
            Z[coord[0], coord[1]] = 1/std(frequency)

plt.figure()
plt.imshow(Z, interpolation = 'none')
plt.colorbar()
plt.show() 
  





# Trying to do the guided image filtering in python
#dem_interp = np.load('/Users/noahzr/Desktop/TerrainCharacterization/scripts/dem_interp2633.npy')
#dem_interp_guided = cv2.guidedFilter
