#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 15:26:58 2022

@author: rileygascoyne
"""
import cv2 
import os 
import glob 
from scipy.ndimage import convolve
from skimage.morphology import opening, remove_small_holes
import numpy as np
import matplotlib.pyplot as plt 
import PIL
from PIL import Image, ImageDraw, ImageOps
            

def riley_model(input_image):

    # where to write data to, does not need to be changed unless wanted
    data_path = os.path.join(img_dir,'*') 
    files = sorted(glob.glob(data_path))
    # an empty list to hold data
    data = [] 
    for f1 in files: 
        
        # reads all image files and turns to arrays
        img = cv2.imread(f1)  
        # adds arrays to empty data table above
        data.append(img)
        
        # converts back to images for analysis
        img = PIL.Image.fromarray(np.array(img))
        # greyscales image
        img_gs = img.convert(mode="L")
        
        # note that we are not dividing by 255 to reduce color range as we filter the image
        img_gs_array = 1 - np.array(img_gs) / 255
        #img_gs_array = np.clip(img_gs_array, 0, 1)
        
        #sets convolution kernel, note it is divied by 9.5 to give a small smoothing boost
        kernel = np.array([[0,1,0],
                           [1,1,1],
                           [0,1,0]]) / 6
        
        convolution = convolve(img_gs_array, kernel)
                  
        # array of the image:
        #grayscale_array = np.array(new_img)
                    
        # change to float representation, reduce color range:
        grayscale_array_float = convolution 
                    
        # apply threshold
        mask = grayscale_array_float < 0.5
                    
        # turn the array back to image for output
        image_mask = Image.fromarray(mask)
     
        
        # turns mask into an array                
        prediction1 = image_mask
        prediction_array1 = np.array(prediction1)
                    
        # determins the selem            
        pixels = np.array([[0., 1., 0.],
                           [1., 1., 1.],
                           [0., 1., 0.]])

        hole_rem = remove_small_holes(prediction_array1, area_threshold=100)    
    
       
        hole_rem1 = remove_small_holes(hole_rem, area_threshold=400)
        hole_img = PIL.Image.fromarray(hole_rem1)
        opened_array = opening(hole_img, selem = pixels)
        opened_img = PIL.Image.fromarray(opened_array)
            
    
        plt.figure()
        # this is the only way I have found thus far to return all files
        plt.imshow(opened_img)