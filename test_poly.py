
# coding=utf-8

import cv2
import numpy as np
import yaml



COLOR_GREEN = (0,255,0)
COLOR_BLUE=(255,0,0)
COLOR_RED=(0,0,255)

DOT_SIZE = 3
POLY_LINE_WIDTH = 2


def draw_circle(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONUP:

        # cv2.circle(param['image'],(x,y),DOT_SIZE,COLOR_GREEN,-1)

        # param['poly'][-1].append((x,y))

        # if param['poly'][-1].__len__() == 0:
        #     param['poly'][-1].append((x, y))
        #
        # else:


        if (  param['poly'][-1].__len__() > 2 )and \
                ((abs(param['poly'][-1][0][0] - cur_position[0]) + abs(param['poly'][-1][0][1] - cur_position[1])) < 10) :#at least 3 point and to find 4th point

            param['poly'][-1].append(param['poly'][-1][0])
            param['poly'].append([])

        else:
            param['poly'][-1].append((x, y))


        # print param['poly'][-1]
        # print 1

    param['current_position'][0] = x
    param['current_position'][1] = y





    # print param['current_position']

if __name__ == "__main__":

    data_dict = {}



    image = cv2.imread('3_1_1.jpg')

    image = image[ :,0:image.shape[1]/2,... ]
    image_ori = cv2.resize(image,dsize=(0,0),fx=0.4,fy=0.4)


    poly=[]
    class_list=[]
    point_list=[]
    poly.append(point_list)
    print poly.__len__()

    cur_position=[]
    cur_position.append(0)
    cur_position.append(0)


    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', draw_circle,param={'image':image,'poly':poly,'class':class_list,'current_position':cur_position})


    flag = True
    while flag:

        image = np.copy(image_ori)

        # plot lines
        for poly_instance in poly:
            if poly_instance.__len__() >1:
                for i in range(poly_instance.__len__()-1):
                    cv2.line(image,pt1=poly_instance[i],pt2=poly_instance[i+1],color=COLOR_RED,thickness=POLY_LINE_WIDTH)



        # plot points
        for poly_instance in poly:

                for i in range(poly_instance.__len__() ):
                    cv2.circle(image,center=poly_instance[i],color=COLOR_GREEN,radius=DOT_SIZE,lineType=-1,thickness=-1)



        #plot near point

        for poly_instance in poly:

            if poly_instance.__len__() > 0:

                if ( abs(poly_instance[0][0] - cur_position[0]) + abs(poly_instance[0][1] - cur_position[1]) ) < 10:

                    print poly_instance[0] , cur_position
                    cv2.circle(image, center=poly_instance[0], color=COLOR_GREEN, radius=DOT_SIZE*3, lineType=-1,thickness=-1)




        # more morden dsiplay
        tmp_img = np.zeros_like( image,dtype=np.uint8 )

        for poly_instance in poly:
            if  poly_instance.__len__()>1 :
                if poly_instance[0]==poly_instance[-1]:#find a close contour

                    pass



        cv2.imshow('frame',image)

        key = cv2.waitKey(30)&0xff# esc:27

        if key == 27:

            flag = False


    cv2.destroyAllWindows()

    # cv2.imshow('frame',image)
    #
    # cv2.waitKey(0)

