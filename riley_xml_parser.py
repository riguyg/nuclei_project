#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 19:13:09 2022

label = read_label_mask(example_label)
label
prediction = riley_model(img_dir)
prediction_array = np.array(prediction)
label_array = np.array(label)

@author: rileygascoyne
"""
import cv2 
import os 
import glob 
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import numpy as np
#from my_io import read_label_mask



# where to write data to, does not need to be changed unless wanted

def analysis(input_image):
    data_path = os.path.join(label_dir,'*') 
    files = sorted(glob.glob(data_path))
    # an empty list to hold data
    data1 = [] 
    for f2 in files: 
            
        # reads all image files and turns to arrays
        #label = cv2.imread(f1) 
        # adds arrays to empty data table above
        #data1.append(label)
        tree = ET.parse(f2)
        root = tree.getroot()
        
        # create blank B&W image
        # assume image size is always 1000x1000 -- CHECK THIS
        new_img = Image.new(mode='1', size=(1000, 1000))
        
        # create drawing environment for new_img
        pdraw = ImageDraw.Draw(new_img)
        
        # iterate over all regions
        for region in root.iter('Region'):
            # each region contains a list of vertices
            # put vertices in a tuple so that we can send them to pdraw
            vertices = tuple((float(v.get('X')), float(v.get('Y'))) for v in region.find('Vertices'))
            
            # draw the polygon
            pdraw.polygon(vertices, fill="white")
  
        plt.figure() 
        plt.imshow(new_img)
        # return the image
