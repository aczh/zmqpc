'''
Example use of image sending.
Sends/receives 100 images.
Displays the last image.
'''
import os
import cv2
from pathlib import Path
from zmqpc import Events

IMGS_TO_PUBLISH = 100
RECV_IMG_NUM = 0
RECV_IMG = None

pub = Events()
sub = Events()

def save_img(img):
    global RECV_IMG_NUM, RECV_IMG
    RECV_IMG_NUM += 1
    print(f'recv img {RECV_IMG_NUM}/{IMGS_TO_PUBLISH}')
    RECV_IMG = img

sub.connect(save_img, 'apple')

cur_dir = os.path.abspath(os.path.dirname(__file__))
img_path = str(Path(cur_dir, 'resources/img.jpg').absolute())
img = cv2.imread(img_path)

for i in range(0, IMGS_TO_PUBLISH):
    print(f'publishing img {i}/{IMGS_TO_PUBLISH}')
    pub.publish('apple', img)

cv2.imshow('last_img', RECV_IMG)
cv2.waitKey(0)
