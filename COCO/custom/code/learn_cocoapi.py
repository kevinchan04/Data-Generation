from pycocotools.coco import COCO
import numpy as np
from matplotlib import pyplot as plt

annfiles = r"/home/ubuntu/PyTorch-YOLOv3/data/coco/images/annotations/"
# captions_train2017.json       instances_train2017.json
# captions_val2017.json         instances_val2017.json
# image_info_test2017.json      person_keypoints_train2017.json
# image_info_test-dev2017.json  person_keypoints_val2017.json

coco = COCO(annfiles+"person_keypoints_train2017.json")

catIds = coco.getCatIds(catNms=['person'])#get category Id(s) by category name(s)
imgIds = coco.getImgIds(catIds=catIds)#get image Ids by category Id(s)

#get image information dictionary by imgIds
imgID = imgIds[np.random.randint(0, len(imgIds))]
img = coco.loadImgs(ids=imgID)[0]

#show the img
img_path = r'/home/ubuntu/PyTorch-YOLOv3/data/coco/images/train2017'
pic = plt.imread(img_path+'/'+img['file_name'])
plt.imshow(pic)
plt.axis('off')

#get annotations information Id by image Id, 
#or/and catIds, areaRng, iscrowd
annIds = coco.getAnnIds(imgIds=imgID)

#get annotations information by information Id
anns = coco.loadAnns(annIds)
print(anns)
print(coco.loadCats(ids=catIds))

#show annotations by annotations information
coco.showAnns(anns)

plt.show()#plt.imshow() just process the image, ptl.show() to show the image
