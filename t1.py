# coding=utf-8

# t1:
# 功能:
# 1.完成显示部分的效果
# 2.完成yaml文件的导出


import cv2
import numpy as np
import yaml
import copy

COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_RED = (0, 0, 255)

DOT_SIZE = 3
POLY_LINE_WIDTH = 2

# convert polygons to contours data format list of n*1*2 shape matrix
def poly2contour(polys):
    contours = []

    for poly in polys:

        if poly.__len__()>1:
            if poly[0]==poly[-1]:
                obj = np.asarray( poly[0:-1] )
                obj = np.reshape(obj,newshape=( obj.shape[0],1,obj.shape[1] ))

                contours.append( obj )

    return contours


# mouse callback function
def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:

        if (param['polys'][-1].__len__() > 2) and \
                ((abs(param['polys'][-1][0][0] - data_dict['current_position'][0]) + abs(
                        param['polys'][-1][0][1] - data_dict['current_position'][1])) < 10):  # at least 3 point and to find 4th point

            param['polys'][-1].append(param['polys'][-1][0])

            data_dict['class_ids'].append([])
            param['polys'].append([])

        else:
            param['polys'][-1].append([x, y])


            # print param['poly'][-1]
            # print 1

    param['current_position'][0] = x
    param['current_position'][1] = y


# delete a point in the last polygon
def delet_poly_point(dict):

    if data_dict['polys'] is not [[]]:
        if data_dict['polys'][-1].__len__() == 0:
            data_dict['polys'].pop()
            data_dict['polys'][-1].pop()
            data_dict['class_ids'].pop()
        else:
            data_dict['polys'][-1].pop()
    return dict


# delete last polygon
def delet_poly(dict):
    if data_dict['polys'].__len__() == 1:
        data_dict['polys'] = [[]]
    else:
        if data_dict['polys'][-1].__len__() == 0:
            data_dict['polys'].pop()
            data_dict['class_ids'].pop()
            data_dict['polys'][-1] = []

        else:
            data_dict['polys'][-1] = []
    return dict


# a wonderful display
def fantacy_display(contours,index,src):
    image = np.copy(src)
    map = np.copy(src)
    cv2.drawContours(map,contours,index,color=(0,0,150),thickness=-1)
    color_image = cv2.addWeighted( image,0.5,map,0.5,0 )
    return color_image



# convert data in dict into ymal file
# ymal file name:data_dict['file_name']
# check if every poly is closed
# alarm when there is unclosed polygon
def convert_dict_to_ymal(dict):

    # 1.check if every polyfon is closed
    if dict['polys'][0].__len__() == 0:
        print 'can not conver dict to yaml , because: ','there is no polygons'
        return False
    else:
        if dict['polys'][-1].__len__() == 0:
            poly_list=dict['polys'][0:-1]
        else:
            poly_list = dict['polys']

        for poly in poly_list:

            if poly.__len__() < 4:
                print 'can not conver dict to yaml , because: ', 'some polygons have less than 4 points'
                return False

            else:
                if poly[0] != poly[-1]:
                    print 'can not conver dict to yaml , because: ', 'some polygons are not closed'
                    return False

    print 'successed conver dict to yaml !!!'

    # 2.start to conver

    yaml_dict={}
    yaml_dict['file_name']=dict['file_name']

    yaml_dict['polys'] = dict['polys'][0:-1]



    # yaml_dict['class_' + str(index)] = dict['class_ids'][index]
    fw = open('example.yaml', 'w')
    yaml.dump(yaml_dict, fw)
    fw.close()

    # 3.return
    return True








if __name__ == "__main__":

    image = cv2.imread('3_1_1.jpg')

    image = image[:, 0:image.shape[1] / 2, ...]
    image_ori = cv2.resize(image, dsize=(0, 0), fx=0.4, fy=0.4)

    data_dict={}
    data_dict['file_name']='3_1_1.jpg'
    data_dict['polys'] = [[]]
    data_dict['class_ids'] = [0]
    data_dict['current_position']=[0,0]


    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', draw_circle,
                         param=data_dict)

    flag = True
    key=None
    visual_image=None

    while flag:

        image = np.copy(image_ori)
        data_dict['class_ids'][-1]=0


        # plot lines
        for poly_instance in data_dict['polys']:
            if poly_instance.__len__() > 1:
                for i in range(poly_instance.__len__() - 1):
                    cv2.line(image, pt1=tuple(poly_instance[i]), pt2=tuple(poly_instance[i + 1]), color=COLOR_RED,
                             thickness=POLY_LINE_WIDTH)



        # plot points
        for poly_instance in data_dict['polys']:

            for i in range(poly_instance.__len__()):
                cv2.circle(image, center= tuple(poly_instance[i]), color=COLOR_GREEN, radius=DOT_SIZE, lineType=-1,
                           thickness=-1)

        # plot near point

        for poly_instance in data_dict['polys']:

            if poly_instance.__len__() > 0:

                if (abs(poly_instance[0][0] - data_dict['current_position'][0]) + abs(poly_instance[0][1] - data_dict['current_position'][1])) < 10:
                    # print poly_instance[0], cur_position
                    cv2.circle(image, center=tuple(poly_instance[0]), color=COLOR_GREEN, radius=DOT_SIZE * 3, lineType=-1,
                               thickness=-1)



        # more morden dsiplay
        contours = poly2contour(data_dict['polys'])
        i = -1
        for index , contour in enumerate(contours) :
            # print index
            if cv2.pointPolygonTest(contour,pt=(data_dict['current_position'][0],data_dict['current_position'][1]),measureDist=False) > 0:
                i = index
                # print i
                # cv2.drawContours(image, contours, i, COLOR_RED, -1)
                image = fantacy_display(contours,i,image)

                break

        if key == 27:
            flag = False


        if key == 117:#'u'
            data_dict = delet_poly_point(data_dict)


        if key == 100:#'d'
            data_dict = delet_poly(data_dict)


        # print key
        # print data_dict['class_ids']

        if key == 10:# enter
            # tmp_img = np.zeros_like(image, dtype=np.uint8)
            # tmp_img = np.copy(image_ori)
            # cv2.drawContours(tmp_img, contours, -1, COLOR_RED, -1)
            # cv2.imshow('tmp_img', tmp_img)

            convert_dict_to_ymal(data_dict)


        cv2.imshow('frame', image)

        if visual_image is not None:
            cv2.imshow('visual_image',visual_image)

        key = cv2.waitKey(30) & 0xff  # esc:27


    cv2.destroyAllWindows()

    # cv2.imshow('frame',image)
    #
    # cv2.waitKey(0)

