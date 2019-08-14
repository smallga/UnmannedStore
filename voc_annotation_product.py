import xml.etree.ElementTree as ET
from os import getcwd

sets=[('2019', 'train'), ('2019', 'val'), ('2019', 'test')]

classes = ["buzz","pig","goofy"]

#for count object number
class_num = len(classes)
cls_count = [0] * class_num

def convert_annotation(year, image_id, list_file):
    in_file = open('Product/ProductAnnotations/%s.xml'%(image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()

    

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        cls_count[cls_id] += 1 #for count object number
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()

for year, image_set in sets:
    image_ids = open('Product/ImageSets/Main/%s.txt'%(image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/Product/ProductImage/%s.jpg'%(wd, image_id))
        convert_annotation(year, image_id, list_file)
        list_file.write('\n')
    list_file.close()

#for count object number
for i in range(len(classes)):
    print(classes[i],"  count=  ",cls_count[i])