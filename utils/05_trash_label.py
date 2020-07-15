import xml.etree.ElementTree as ET
import os
import cv2

import numpy as np


import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
 
sets = ['train','val']
 
# classes = ['fast_food_box','paper_works','charge_pal','leftover_food ','bag','ash-bin','plastic_ware','plastic_toy','plastic_hanger','big_bone','dry_cell','curier_bags','plugs_cables ','old_clothes','pop_can','pillow','cuticle','dolls','stained_plastic','stained_paper','toiletries','cigarette_butt ','toothpick','glassware','cutting-board','chopsticks','paper_box','flowerpot','tea_leave','vegetable','eggshell','spice_jar','ointment','expired_drugs','winebottle','metalic_kitchenware','metalware','metal_food_can','pan','ceramic_vessels ','shoe','oil_containers','drink_bottle','fish_bone']
classes = ['一次性快餐盒','书籍纸张','充电宝',
                  '剩饭剩菜' ,'包','垃圾桶','塑料器皿','塑料玩具','塑料衣架',
                   '大骨头','干电池','快递纸袋','插头电线','旧衣服','易拉罐',
                   '枕头','果皮果肉','毛绒玩具','污损塑料','污损用纸','洗护用品',
                   '烟蒂','牙签','玻璃器皿','砧板','筷子','纸盒纸箱','花盆',
                   '茶叶渣','菜帮菜叶','蛋壳','调料瓶','软膏','过期药物',
                   '酒瓶','金属厨具','金属器皿','金属食品罐','锅','陶瓷器皿',
                   '鞋','食用油桶','饮料瓶','鱼骨']
 
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
 
 
def convert_annotation(image_id):
    in_file = open('Annotations/%s.xml' % (image_id))
    out_file = open('labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
 
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        if (np.array(bb) > 1).any():
            return
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
 
 
wd = getcwd()
for image_set in sets:
    if not os.path.exists('labels'):
        os.makedirs('labels')
    image_ids = open('ImageSets/Main/%s.txt' % (image_set)).read().strip().split()
    list_file = open('trash_%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write('images/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()