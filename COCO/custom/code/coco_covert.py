'''
get the coco style labels for body parts
version 1
Shortage: it can not change nn_pixel according the square of body parts
'''
from pycocotools.coco import COCO
import numpy as np
from matplotlib import pyplot as plt
import argparse

# if __name__ == "__main__":

parser = argparse.ArgumentParser()
parser.add_argument("--imgs_folder",type=str,default=r"/home/ubuntu/PyTorch-YOLOv3/data/custom/images/val2017", help="data folder path")
parser.add_argument("--anns_folder",type=str,default=r"/home/ubuntu/PyTorch-YOLOv3/data/custom/images/annotations", help="anns folder path")
parser.add_argument("--anns_file",type=str,default=r"/person_keypoints_val2017.json", help="JSON anns file name")
parser.add_argument("--imgs_txt_folder",type=str,default=r"/home/ubuntu/PyTorch-YOLOv3/data/custom/code/custom_datalist", help="Saved the imgs path list for train or val, test")
parser.add_argument("--anns_txt_folder",type=str,default=r"/home/ubuntu/PyTorch-YOLOv3/data/custom/code/custom_anns/val2017", help="Saved the custom anns txt files")
parser.add_argument("--imgs_txt",type=str,default=r"/val2017.txt",help="txt file to store img paths")
opt = parser.parse_args()

# anns_folder = r"/home/ubuntu/PyTorch-YOLOv3/data/coco/images/annotations"
# anns_file = r"/person_keypoints_train2017.json"
# captions_train2017.json       instances_train2017.json
# captions_val2017.json         instances_val2017.json
# image_info_test2017.json      person_keypoints_train2017.json
# image_info_test-dev2017.json  person_keypoints_val2017.json
# train_imgs_folder = r"/home/ubuntu/PyTorch-YOLOv3/data/coco/images/train2017"
# val_imgs_folder = r"/home/ubuntu/PyTorch-YOLOv3/data/coco/images/val2017"

#hpyer params
#get keypoints name dictionary
kps_list = ['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle', 'person']
# kps_dict = {'nose':[], 'left_eye':[], 'right_eye':[], 'left_ear':[], 'right_ear':[], 'left_shoulder':[], 'right_shoulder':[], 'left_elbow':[], 'right_elbow':[], 'left_wrist':[], 'right_wrist':[], 'left_hip':[], 'right_hip':[], 'left_knee':[], 'right_knee':[], 'left_ankle':[], 'right_ankle':[]}
kps_lable = {'nose':0, 'left_eye':1, 'right_eye':2, 'left_ear':3, 'right_ear':4, 'left_shoulder':5, 'right_shoulder':6, 'left_elbow':7, 'right_elbow':8, 'left_wrist':9, 'right_wrist':10, 'left_hip':11, 'right_hip':12, 'left_knee':13, 'right_knee':14, 'left_ankle':15, 'right_ankle':16, 'person':17}
alpha_ = 100
flag_w_imgs_list = False

coco = COCO(opt.anns_folder + opt.anns_file)

#get category Id(s) by category name(s)
catIds = coco.getCatIds(catNms=['person'])
#get image Ids by category Id(s)
imgIds = coco.getImgIds(catIds=catIds)#The Ids of images include "person"

#get images information dictionary by imgIds
imgs_info_dict_list = coco.loadImgs(ids=imgIds)
#open a txt to store img path
imgs_list_txt = open(opt.imgs_txt_folder+opt.imgs_txt, "a")
for img_info_dict in imgs_info_dict_list:
    #get imgId
    imgId = img_info_dict['id']
    #get img path
    img_filename = img_info_dict['file_name']
    img_path = opt.imgs_folder + '/' + img_filename
    #get img width and height
    img_width = img_info_dict['width']
    img_height = img_info_dict['height']
    #plt imread
    # pic = plt.imread(fname=img_path)
    # plt.imshow(pic)
    # plt.axis('off')
    #get AnnIds, Anns
    annIds = coco.getAnnIds(imgIds=imgId)
    anns = coco.loadAnns(annIds)
    #create a txt label file, file name should be samilar with img file_name
    #for loop in Anns
    for ann in anns:
        if ann['num_keypoints'] != 0:
            flag_w_imgs_list = True
            img_anns_txt = open(opt.anns_txt_folder+"/"+img_filename[:-4]+".txt", "a+")#delete ".jpg" in img_filename
            keypoints_list = ann['keypoints']#get keypoint
            bbox_width = ann['bbox'][2]#full body bbox width
            bbox_height = ann['bbox'][3]#full body bbox height
            nn_pixel = alpha_ * (bbox_height * bbox_width) // (img_height * img_width) + 1
            nn_pixel_x_s = nn_pixel / img_width#s means scale
            nn_pixel_y_s = nn_pixel / img_height
            t_ = 0
            kps_dict = {}
            list_ = []
            for d_ in keypoints_list:
                list_.append(d_)
                if len(list_) == 3:
                    kps_dict[kps_list[t_]] = list_
                    t_ += 1
                    list_ = []
            #get the label from kps dict
            # take_kps = ['nose', 'right_ankle']#select tha kps you want to covert label style
            for kp_name, kp_axis in kps_dict.items():
                if kp_axis[2] == 2:#[x,y,v], v = 2 means the kp is available to be saw in picture
                    kp_center_x = kp_axis[0] / img_width
                    kp_center_y = kp_axis[1] / img_height
                    if nn_pixel % 2 != 0:
                        nn_pixel += 1
                    label_ = kps_lable[kp_name]
                    img_anns_txt.write(str(label_)+" "+str(kp_center_x)+" "+str(kp_center_y)+" "+str(nn_pixel_x_s)+" "+str(nn_pixel_y_s)+"\r")
            #person
            person_center_x = (ann['bbox'][0] + bbox_width / 2) / img_width
            person_center_y = (ann['bbox'][1] + bbox_height / 2) / img_height
            bbox_width_s = bbox_width / img_width
            bbox_height_s = bbox_height / img_height
            label_ = kps_lable['person']
            # kps_dict['person'] = 
            img_anns_txt.write(str(label_)+" "+str(person_center_x)+" "+str(person_center_y)+" "+str(bbox_width_s)+" "+str(bbox_height_s)+"\r")
            #close txt
            img_anns_txt.close()
    #store img path
    if flag_w_imgs_list:
        imgs_list_txt.write(img_path+"\r")
        flag_w_imgs_list = False
    # break
imgs_list_txt.close()  
print("finish")       

#show annotations by annotations information
# coco.showAnns(anns)

# plt.show()#plt.imshow() just process the image, ptl.show() to show the image
