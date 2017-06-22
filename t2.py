# coding=utf-8

# t2:
# 功能:
# 1.完成显示部分的效果
# 2.完成yaml文件的导出
# 3.使用class管理

import cv2
import numpy as np
import yaml

import os

COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_RED = (0, 0, 255)

DOT_SIZE = 3
POLY_LINE_WIDTH = 2



class Tool(object):
    def __init__(self,data_obj,window_name='Tool',dst_folder='./'):

        self.data_obj = data_obj

        image_path = self.data_obj.get_path()

        self.image_ori = cv2.imread(image_path)

        if self.image_ori.shape[0]>794 :
            self.image_ori = cv2.resize(self.image_ori,dsize=(794,595))



        self.image=np.copy(self.image_ori)
        self.win_name=window_name

        self.data_dict = {}
        self.data_dict['file_name'] = image_path.split('/')[-1]
        self.data_dict['dst_folder'] = dst_folder
        self.data_dict['yaml_name'] = self.data_dict['file_name'].strip('.jpg') + '.yaml'
        self.data_dict['yaml_path']= self.data_dict['dst_folder'] + self.data_dict['yaml_name']
        self.data_dict['polys'] = [[]]
        self.data_dict['class_ids'] = [2]
        self.data_dict['current_position'] = [0, 0]
        self.data_dict['contours']=[]

        cv2.namedWindow(self.win_name)

        cv2.setMouseCallback(self.win_name,self._mouse_callback,param=self)

        self._load_yaml()

    def change_image(self):

        image_path = self.data_obj.get_path()

        self.image_ori = cv2.imread(image_path)

        if self.image_ori.shape[0]>794 :
            self.image_ori = cv2.resize(self.image_ori,dsize=(794,595))


        self.image = np.copy(self.image_ori)


        self.data_dict['file_name'] = image_path.split('/')[-1]

        # print self.data_dict['yaml_name']
        # print self.data_dict['dst_folder']

        self.data_dict['yaml_name'] = self.data_dict['file_name'].strip('.jpg') + '.yaml'
        self.data_dict['yaml_path'] = self.data_dict['dst_folder'] + self.data_dict['yaml_name']
        self.data_dict['polys'] = [[]]
        self.data_dict['class_ids'] = [2]
        self.data_dict['current_position'] = [0, 0]
        self.data_dict['contours'] = []

        self._load_yaml()
        # cv2.namedWindow(self.win_name)
        # cv2.setMouseCallback(self.win_name, self.mouse_callback, param=self)

    def _load_yaml(self):
        if os.path.exists(self.data_dict['yaml_path']):
            print 'there is coresponding yaml file'
            fr = open(self.data_dict['yaml_path'], 'r')

            yaml_dict = yaml.load(fr)

            self.data_dict['polys'] = yaml_dict['polys']
            self.data_dict['polys'].append([])
            self.data_dict['class_ids']=yaml_dict['class_ids']
            self.data_dict['class_ids'].append(2)

            # print self.data_dict['polys'].__len__()


            fr.close()


    # convert data in dict into ymal file
    # ymal file name:data_dict['file_name']
    # check if every poly is closed
    # alarm when there is unclosed polygon
    def _save_yaml(self):
        # 1.check if every polyfon is closed
        if self.data_dict['polys'][0].__len__() == 0:
            print 'can not conver dict to yaml , because: ', 'there is no polygons'
            return True
        else:
            if self.data_dict['polys'][-1].__len__() == 0:
                poly_list = self.data_dict['polys'][0:-1]
            else:
                poly_list = self.data_dict['polys']
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
            yaml_dict = {}
            yaml_dict['file_name'] = self.data_dict['file_name']
            yaml_dict['polys'] = self.data_dict['polys'][0:-1]
            yaml_dict['class_ids']=self.data_dict['class_ids'][0:-1]
            yaml_dict['shape']=list(self.image.shape)

            fw = open(self.data_dict['yaml_path'], 'w')
            yaml.dump(yaml_dict, fw)
            fw.close()

            # 3.return
            return True



    def _mouse_callback(self,event, x, y, flags, param):
        # mouse callback function
        if event == cv2.EVENT_LBUTTONUP:
            if (param.data_dict['polys'][-1].__len__() > 2) and \
                    ((abs(param.data_dict['polys'][-1][0][0] - param.data_dict['current_position'][0]) + abs(
                            param.data_dict['polys'][-1][0][1] - param.data_dict['current_position'][1])) < 10):  # at least 3 point and to find 4th point
                param.data_dict['polys'][-1].append(param.data_dict['polys'][-1][0])
                param.data_dict['class_ids'].append(param.data_dict['class_ids'][-1])
                param.data_dict['polys'].append([])
            else:
                param.data_dict['polys'][-1].append([x, y])
                # print param['poly'][-1]
                # print 1
        param.data_dict['current_position'][0] = x
        param.data_dict['current_position'][1] = y


        if event == cv2.EVENT_RBUTTONUP:
            print param.data_dict['class_ids']
            tmp = param.data_dict['class_ids'][-1] + 1
            if tmp > 2:
                tmp = 0
            param.data_dict['class_ids'][-1] = tmp
            # print param.data_dict['class_ids'][-1]

    def _plot_points(self):

        # plot lines
        for poly_instance in self.data_dict['polys']:
            if poly_instance.__len__() > 1:
                for i in range(poly_instance.__len__() - 1):
                    cv2.line(self.image, pt1=tuple(poly_instance[i]), pt2=tuple(poly_instance[i + 1]), color=COLOR_RED,
                             thickness=POLY_LINE_WIDTH)

        # plot points
        for poly_instance in self.data_dict['polys']:

            for i in range(poly_instance.__len__()):
                cv2.circle(self.image, center=tuple(poly_instance[i]), color=COLOR_GREEN, radius=DOT_SIZE, lineType=-1,
                           thickness=-1)

        # plot near point
        for poly_instance in self.data_dict['polys']:

            if poly_instance.__len__() > 0:

                if (abs(poly_instance[0][0] - self.data_dict['current_position'][0]) + abs(
                            poly_instance[0][1] - self.data_dict['current_position'][1])) < 10:
                    # print poly_instance[0], cur_position
                    cv2.circle(self.image, center=tuple(poly_instance[0]), color=COLOR_GREEN, radius=DOT_SIZE * 3,
                               lineType=-1,
                               thickness=-1)
        return self.image


    # delete a point in the last polygon
    def _delet_poly_point(self):
        if self.data_dict['polys'][0].__len__() is not 0:
            if self.data_dict['polys'][-1].__len__() == 0:
                self.data_dict['polys'].pop()
                self.data_dict['polys'][-1].pop()
                self.data_dict['class_ids'].pop()
            else:
                self.data_dict['polys'][-1].pop()


    # delete last polygon
    def _delet_poly(self):

        # print 'delet point from a poly'

        if self.data_dict['polys'].__len__() == 1:
            self.data_dict['polys'] = [[]]
        else:
            if self.data_dict['polys'][-1].__len__() == 0:
                self.data_dict['polys'].pop()
                self.data_dict['class_ids'].pop()
                self.data_dict['polys'][-1] = []
            else:
                self.data_dict['polys'][-1] = []
        return self.data_dict

    # convert polygons to contours data format list of n*1*2 shape matrix
    def _poly2contour(self):
        contours = []
        for poly in self.data_dict['polys']:

            if poly.__len__() > 1:
                if poly[0] == poly[-1]:
                    obj = np.asarray(poly[0:-1])
                    obj = np.reshape(obj, newshape=(obj.shape[0], 1, obj.shape[1]))
                    contours.append(obj)
        self.data_dict['contours'] = contours

    # a wonderful display
    def _fantacy_display(self):
        self._poly2contour()
        for index , contour in enumerate(self.data_dict['contours']) :
            # print index
            if cv2.pointPolygonTest(contour,pt=(self.data_dict['current_position'][0],self.data_dict['current_position'][1]),measureDist=False) > 0:
                i = index
                # print i
                # cv2.drawContours(image, contours, i, COLOR_RED, -1)
                image = np.copy(self.image)
                map = np.copy(self.image)

                color_map=[ (150, 0, 0),(0, 150, 0),(0, 0, 150) ]

                cv2.drawContours(map, self.data_dict['contours'], index, color_map[self.data_dict['class_ids'][index]], thickness=-1)
                self.image = cv2.addWeighted(image, 0.5, map, 0.5, 0)
                # break

        cv2.putText(self.image,text=str(self.data_dict['class_ids'][-1]),\
                    org=( int(self.image.shape[1]*0.9),int(self.image.shape[0]*0.9) ),\
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(188,188,0),thickness=2)

        cv2.putText(self.image, text=self.data_dict['file_name'], \
                    org=(int(self.image.shape[1] * 0.), int(self.image.shape[0] * 0.05)), \
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(188, 188, 0), thickness=2)


    def visual(self,key):

        # self.data_dict['class_ids'][-1]=2

        self.image = np.copy(self.image_ori)
        flag = True

        self._plot_points()
        self._fantacy_display()


        if key == 27:
            flag = False

        if key == 117:#'u'
            self._delet_poly_point()

        if key == 100:#'d'
            self._delet_poly()

        if key == 10:# enter

            self._save_yaml()
        # print self.data_dict['polys']

        if key == 81:# '<-'
            self.data_obj.step_to_last()
            self.change_image()

        if key == 83:# '->'

            res = self._save_yaml()
            if res :
                self.data_obj.step_to_next()
                self.change_image()

        # print key
        # print self.data_dict['class_ids']

        cv2.imshow(self.win_name,self.image)
        return flag


class Data(object):

    def __init__(self,data_txt_path,image_root):
        self.image_root = image_root
        self.data_txt_path = data_txt_path
        self.cnt = np.int32(0)
        self.image_paths=[]

        f = open(data_txt_path, 'w')
        folder_list = os.listdir(image_root)

        for folder in folder_list:
            image_list = os.listdir( image_root+folder )
            for image_file in image_list:
                if '.jpg' in image_file:
                    # print image_root+folder+'/'+image_file
                    # image_files.append(folder+'/'+image_file)
                    self.image_paths.append( image_root+folder+'/'+image_file )
                    f.write( folder+'/'+image_file+'\n' )
        f.close()
        self.image_paths = sorted(self.image_paths)
        self.number = self.image_paths.__len__()
        print 'we have',self.number,'images, Let us annptate them!!!'


    def get_path(self):
        return self.image_paths[self.cnt]

    def step_to_last(self):
        self.cnt -= 1
        if self.cnt < 0:
            self.cnt = 0

        return self.image_paths[self.cnt]


    def step_to_next(self):
        self.cnt += 1
        if self.cnt > self.number-1:
            self.cnt = self.number-1
        return self.image_paths[self.cnt]


if __name__ == "__main__":

    image_root = '/media/m/d94fadf6-5355-44e1-8e01-4fac33ad7352/Quadro_robot/Dataset_software_town/road_images/'
    annotation_path = '/home/m/PycharmProjects/my_tool/Data/Annatotion_dataset/'


    # data = Data(data_txt_path='./Data/data.txt', image_root=image_root)

    # data = Data( data_txt_path= './Data/data.txt',image_root=image_root)
    # tool = Tool(data,dst_folder='./YAML/')

    data = Data(data_txt_path=annotation_path+'data.txt', image_root=image_root)
    tool = Tool(data, dst_folder=annotation_path+'YAML/')


    flag=True
    key=-1

    while flag:

        flag=tool.visual(key)
        key = cv2.waitKey(10)&0xff