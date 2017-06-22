# coding=utf-8
# 用对应的yaml 和 图片文件 , 制作带label的数据集
import cv2
import numpy as np
import yaml
import os

# def make_img_txt(src_path='./Data/data.txt'):
#     image_root = '/media/m/d94fadf6-5355-44e1-8e01-4fac33ad7352/Quadro_robot/Dataset_software_town/road_images/'
#     f = open(src_path,'w')
#
#     for item in os.listdir(image_root+'road1/'):
#         if '.jpg' in item:
#             f.write('road1/'+item+'\n')
#
#     for item in os.listdir(image_root + 'road2/'):
#         if '.jpg' in item:
#             f.write('road2/'+item + '\n')
#
#
#     f.close()


def make_label(src_img_txt_path,src_yaml_folder,dst_folder):

    f_txt = open( src_img_txt_path,'r' )
    images=f_txt.readlines()
    images=[item.strip('\n') for item in images]
    f_txt.close()

    yamls=os.listdir(src_yaml_folder)
    yaml_names = [ item.split('.')[0] for item in yamls]


    image_root = '/media/m/d94fadf6-5355-44e1-8e01-4fac33ad7352/Quadro_robot/Dataset_software_town/road_images/'
    for item in images:

        image_src_path = image_root+item
        image = cv2.imread(image_src_path)

        if image.shape[0]>794 :
            image = cv2.resize(image,dsize=(794,595))


        image_name = item.split('/')[-1]
        image_dst_path = dst_folder+'img/'+image_name

        image_id=item.split('/')[-1].split('.')[0]

        if image_id in yaml_names:
            print image_id , image.shape,
            print image_dst_path

            cv2.imwrite( image_dst_path,image[25:575,25:775,...] )
            draw_one_label_image(yaml_path=src_yaml_folder+image_id+'.yaml',dst_folder=dst_folder+'label/')



def poly2contour(polys):
    contours = []
    for poly in polys:

        if poly.__len__() > 1:
            if poly[0] == poly[-1]:
                obj = np.asarray(poly[0:-1])
                obj = np.reshape(obj, newshape=(obj.shape[0], 1, obj.shape[1]))
                contours.append(obj)
    # self.data_dict['contours'] = contours
    return contours



def draw_one_label_image(yaml_path,dst_folder):

    label_name = yaml_path.split('/')[-1].split('.')[0]+'_label.png'
    fr = open(yaml_path, 'r')
    yaml_dict = yaml.load(fr)
    fr.close()
    image = np.zeros( (yaml_dict['shape'][0],yaml_dict['shape'][1]  ),dtype=np.uint8 )
    contours = poly2contour( yaml_dict['polys'] )
    for index, poly in enumerate(yaml_dict['polys'])  :
        cv2.drawContours(image,contours= contours,contourIdx= index,color=(250/2*yaml_dict['class_ids'][index]),thickness=-1)

    # cv2.imshow('frame',image)
    # cv2.waitKey(0)

    # uni = np.unique(image)
    # print uni
    # print image.shape

    image = image[...,np.newaxis]
    cv2.imwrite( dst_folder+label_name,image.astype(np.uint8)[25:575,25:775,...] )


if __name__ =="__main__":

    annotation_path = '/home/m/PycharmProjects/my_tool/Data/Annatotion_dataset/'

    make_label(src_img_txt_path=annotation_path+'data.txt',src_yaml_folder=annotation_path+'YAML/',dst_folder=annotation_path+'train/')



    # draw_one_label_image('./YAML/IMG_20170504_145426.yaml' ,'./Data/dataset/train/label/')
