#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# auth code identifier using svm


import os
from PIL import Image, ImageEnhance
import numpy as np
import math
from sklearn import svm

# train data file path

path = r'C:\Users\Wjw\Pictures\imgdata\traindata'

# image cut region

part = {'1': (0, 0, 27, 50), '2': (28, 0, 55, 50), '3': (63, 0, 90, 50), '4': (95, 0, 122, 50)}

# get look-up-table for Image.point() method

threshold = 163
table = []
for i in range(256):
    if i < threshold:
        table.append(0) # 0 for black
    else:
        table.append(1) # 1 for white
       


# image process

def img_preparation(img):
    img = img.convert('L')
    sharpness = ImageEnhance.Contrast(img)
    sharp_img = sharpness.enhance(2.0)
    two_value_out = sharp_img.point(table, '1')
    return two_value_out
    
def del_noise(img):
    for x in range(130): # horizontal
        for y in range(50): # vertical
            cur_pixel = img.getpixel((x,y))
            if cur_pixel == 0:
                if x == 0 and y == 0:
                    sum = img.getpixel((x,y+1)) + img.getpixel((x+1,y)) + img.getpixel((x+1,y+1))
                    if sum > 1:
                        img.putpixel((x,y), 1)
                elif x == 129 and y == 0:
                    sum = img.getpixel((x-1,y)) + img.getpixel((x-1,y+1)) + img.getpixel((x,y+1))
                    if sum > 1:
                        img.putpixel((x,y), 1)
                elif x == 0 and y == 49:
                    sum = img.getpixel((x,y-1)) + img.getpixel((x+1,y-1)) + img.getpixel((x+1,y))
                    if sum > 1:
                        img.putpixel((x,y), 1)
                elif x == 129 and y == 49:
                    sum = img.getpixel((x-1,y)) + img.getpixel((x-1,y-1)) + img.getpixel((x,y-1))
                    if sum > 1:
                        img.putpixel((x,y), 1)
                elif y == 0 and x != 0 and x != 129:
                    sum = img.getpixel((x-1,y)) + img.getpixel((x-1,y+1)) \
                        + img.getpixel((x,y+1)) + img.getpixel((x+1,y+1)) + img.getpixel((x+1,y))
                    if sum > 2:
                        img.putpixel((x,y), 1)
                elif y == 49 and x != 0 and x != 129:
                    sum = img.getpixel((x-1,y)) + img.getpixel((x-1,y-1)) \
                        + img.getpixel((x,y-1)) + img.getpixel((x+1,y-1)) + img.getpixel((x+1,y))
                    if sum > 2:
                        img.putpixel((x,y), 1)
                elif x == 0 and y != 0 and y != 49:
                    sum = img.getpixel((x,y-1)) + img.getpixel((x+1,y-1)) \
                        + img.getpixel((x+1,y)) + img.getpixel((x+1,y+1)) + img.getpixel((x,y+1))
                    if sum > 2:
                        img.putpixel((x,y), 1)
                elif x == 129 and y != 0 and y != 49:
                    sum = img.getpixel((x-1,y)) + img.getpixel((x-1,y-1)) \
                        + img.getpixel((x-1,y)) + img.getpixel((x-1,y+1)) + img.getpixel((x,y+1))
                    if sum > 2:
                        img.putpixel((x,y), 1)
                else:
                    sum = img.getpixel((x,y-1)) + img.getpixel((x,y+1)) \
                        + img.getpixel((x+1,y-1)) + img.getpixel((x+1,y)) + img.getpixel((x+1,y+1)) \
                        + img.getpixel((x-1,y-1)) + img.getpixel((x-1,y)) + img.getpixel((x-1,y+1))
                    if sum > 5:
                        img.putpixel((x,y), 1)
    return img

                
# get train data

def get_train_data():
    for i in range(1, 251):
        img = Image.open(r'C:\Users\Wjw\Pictures\imgdata' + r'\\' + str(i) + '.png')
        two_value_out = img_preparation(img)
        out = del_noise(two_value_out)
        #for k in range(3):
        #    out = del_noise(out)
        for j in range(1,5):
            imgPart = out.crop(part[str(j)])
            imgName = str(i) + '-' + str(j) + '.png'
            imgPath = os.path.join(path, imgName)
        #two_value_out.save(imgPath)
            imgPart.save(imgPath)
        img.close()


# get feature

def get_feature(pic):
    width, height = pic.size
    feature = []
    for y in range(height):
        cnt_x = 0
        for x in range(width):
            if pic.getpixel((x, y)) == 0:
                cnt_x += 1
        feature.append(cnt_x)
    for x in range(width):
        cnt_y = 0
        for y in range(height):
            if pic.getpixel((x, y)) == 0:
                cnt_y += 1
        feature.append(cnt_y)
    return feature
    
    
def get_trainSample_label():
    X = [] # feature
    y = [] # label
    for i in range(10):
        trainPics = os.listdir(r'C:\Users\Wjw\Pictures\imgdata\traindata\%s' % str(i))
        for trainPic in trainPics:
            pic = Image.open(r'C:\Users\Wjw\Pictures\imgdata\traindata\%s\%s' % (str(i), trainPic))
            feature = get_feature(pic)
            X.append(feature)
            y.append(str(i))
    return X, y

# try SVM    

def svmPredict(img):
    img_preprocess = del_noise(img_preparation(img))
    
    p1 = img_preprocess.crop(part['1'])
    p2 = img_preprocess.crop(part['2'])
    p3 = img_preprocess.crop(part['3'])
    p4 = img_preprocess.crop(part['4'])
    
    X, y = get_trainSample_label()
    clf = svm.SVC()
    clf.fit(X, y)
    
    predict = []
    for k in [p1, p2, p3, p4]:
        predict.append(clf.predict(get_feature(k))[0])
        
    return predict[0] + predict[1] + predict[2] + predict[3]
    
    
# try kNN

def kNN_identifier(img):
    img_preprocess = del_noise(img_preparation(img))
    
    p1 = img_preprocess.crop(part['1'])
    #p1.show()
    p2 = img_preprocess.crop(part['2'])
    #p2.show()
    p3 = img_preprocess.crop(part['3'])
    #p3.show()
    p4 = img_preprocess.crop(part['4'])
    #p4.show()
    
    predict = []
    for k in [p1, p2, p3, p4]:
        #k.show()
        imgMat = np.array(k)
        imgMat.dtype = 'int8'
        #print(list(imgMat))
        preMat = []
        for i in range(10):
            benpics = os.listdir(r'C:\Users\Wjw\Pictures\imgdata\traindata\%s' % str(i))
            temp = []
            for benpic in benpics:
                pic = Image.open(r'C:\Users\Wjw\Pictures\imgdata\traindata\%s\%s' % (str(i), benpic))
                picMat = np.array(pic)
                picMat.dtype = 'int8'
                ''' cosine similarity
                num = np.dot(imgMat.reshape(1350), picMat.reshape(1350))
                #print(num)
                denom = np.linalg.norm(imgMat.reshape(1350)) * np.linalg.norm(picMat.reshape(1350))
                cos = num / denom
                '''
                distance = math.sqrt(sum((imgMat.reshape(1350) - picMat.reshape(1350))**2)) # using euclidean distance correct rate high!!!
                #print(np.linalg.norm(imgMat.reshape(1350)), np.linalg.norm(picMat.reshape(1350)))
                #print(num, denom, cos)
                temp.append(distance)
            #print(list(temp))
            preMat.append((min(temp), str(i)))
        preMat.sort(key= lambda i : i[0], reverse= False)
        #print(list(preMat))
        predict.append(preMat[0])
    return predict[0][1] + predict[1][1] + predict[2][1] + predict[3][1]
    
if __name__ == '__main__':
    print('kNN identifier: ', kNN_identifier(Image.open(r'C:\Users\Wjw\Pictures\imgdata\499.png')))
    print('svm identifier: ', svmPredict(Image.open(r'C:\Users\Wjw\Pictures\imgdata\499.png')))