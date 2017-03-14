#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# get orginal images
__author__ = "Frank"


import os
from urllib.request import urlretrieve

#for i in range(1,501):
#    url = 'http://www.169ol.com/Stream/Code/getCode'
#    path = r'C:\Users\Wjw\Pictures\imgdata'
#    imgname = str(i) + '.png'
#    imgpath = os.path.join(path, imgname)
#    urlretrieve(url, imgpath)
 
def getCode():
    url = 'http://www.169ol.com/Stream/Code/getCode'
    path = r'C:\Users\Wjw\Pictures\imgdata'
    imgname = '501.png'
    imgpath = os.path.join(path, imgname)
    urlretrieve(url, imgpath)
