#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:10:09 2020
@author: noahzr
"""



import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import richdem as rd
from scipy import stats


matplotlib.rcParams['figure.figsize']=(8, 5.5)




# alterations: if nans are present in surface 

peaks = np.load('/Users/noahzr/Desktop/TerrainCharacterization/scripts/dem_part_guided.npy')
# downsample to 0.1m resolution
peaks_1 = peaks[::5,::5]

test =  rd.rdarray(peaks_1, no_data = 0)


aspect = rd.TerrainAttribute(test, attrib='aspect')
rd.rdShow(aspect, axes=False, cmap='jet')
plt.show()

Z_five = np.zeros(peaks.shape)
nodata_val = -9999
deg_rounded = 90
kernel_size = 10

aspect = deg_rounded * np.around(np.true_divide(aspect,deg_rounded)) 

# Performing Kolmogorov-Smirnov test:
    
    
# 50 x 50 analysis set while rounding to 10 degrees
for coord, j in np.ndenumerate(aspect):
    if (min(coord) > int(kernel_size/2)) & (coord[0] < (peaks.shape[0] - int(kernel_size/2))) & (coord[1] < (peaks.shape[1] - int(kernel_size/2))):
        # dataset to be evaluated
        analysis_set = concatenate(aspect[(coord[0] - int(kernel_size/2)):(coord[0] + int(kernel_size/2)),(coord[1] - int(kernel_size/2)):(coord[1] + int(kernel_size/2))])
        # removing nodata value from dataset
        analysis_set = np.delete(analysis_set, np.where(analysis_set == nodata_val))
        
        if analysis_set.shape[0] != 0:            
            # rounding to 10 degrees for more broader classification 
            ana_rounded5 = deg_rounded * np.around(np.true_divide(analysis_set,deg_rounded)) 
            # only account for north direction once
            ana_rounded5[ana_rounded5 == 360] = 0
            D, p = stats.kstest(np.true_divide(ana_rounded5,deg_rounded), stats.uniform(loc = 0, scale = (360/deg_rounded)-1).cdf)
            #Z[coord[0], coord[1]] = p
            #if p >= 0.90:
            Z_five[coord[0], coord[1]] = p

plt.figure()
plt.imshow(Z_five, interpolation = 'none')
plt.colorbar()
plt.show() 
  


