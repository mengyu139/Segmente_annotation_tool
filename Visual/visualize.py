# coding=utf-8
# 用对应的yaml 和 图片文件 , 制作带label的数据集
import cv2
import numpy as np
import yaml

import os




def label_plus_image(image_root,label_root):

    images = os.listdir(image_root)

    labels=os.listdir(label_root)


    for image in images:

        image_id = image.strip('.jpg')

        for label in labels:

            label_id = label.strip('_label.png')

            if label_id == image_id:

                label_data=cv2.imread(label_root+label)

                # label_data = label_data[...,0]
                label_data = cv2.cvtColor(label_data,cv2.COLOR_BGR2GRAY)
                unique = np.unique(label_data)

                print unique
                #BGR
                mask0 = np.where(label_data == 0 , 255 , 0)
                mask1 = np.where(label_data == 125, 255, 0)
                mask2 = np.where(label_data == 250, 255, 0)

                color_map=np.zeros( (label_data.shape[0],label_data.shape[1],3),dtype=np.uint8 )

                color_map[...,0] = mask0
                color_map[...,1] = mask1
                color_map[...,2] = mask2

                image_data = cv2.imread(image_root+image)
                print image_data.shape


                visual_img = cv2.addWeighted(image_data,0.5,color_map,0.5,0)

                cv2.imshow('color_map',color_map)
                cv2.imshow('visual_img', visual_img)

                cv2.waitKey(1000)
                print label_data.shape






if __name__ =="__main__":

    label_plus_image( image_root='../Data/dataset/train/img/' ,label_root='../Data/dataset/train/label/' )

    # a=np.zeros((3,3))
    # a[0,0]=1
    # a[1,1]=1
    # a[2,2]=1
    # print a
    #
    # b = np.where(a<1.,0,2)
    #
    # print b