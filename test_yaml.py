import yaml

aproject = {'filename': 'xxx.jpg'
            }

class_id = 0
aproject['class_'+str(0)]=class_id
aproject['poly_'+str(0)]=[[[269, 285], [330, 349], [210, 376], [269, 285]],[[269, 285], [330, 349], [210, 376], [269, 285]]]



# # write
# fw = open('example.yaml', 'w')
#
# yaml.dump(aproject,fw)
#
# fw.close()
#
#

# read
fr = open('example.yaml','r')

x = yaml.load(fr)

for k , v in x.items():
    print k

fr.close()