import cv2
from glob import glob
import numpy as np
from matplotlib import pyplot as plt


def get_di(ims_list = ["real_A", "fake_B_100", "fake_B_130", "fake_B_160", "fake_B_180", "fake_B_200"]):
    
    di = {}
    for i, im_list in enumerate(ims_list):
        fake_ims = [im_path for im_path in sorted(glob(f"{im_list}/*"))]
        di[f"{im_list}"] = fake_ims
    
    return di

def read_im(im): return cv2.cvtColor(cv2.imread(im), cv2.COLOR_BGR2RGB)

def visualize(ims_list, i0, i1, i2, i3, i4, i5):
    
    plt.figure(figsize=(25, 4))
    plt.subplot(1, 6, 1)
    plt.imshow(i0)
    plt.title(f"{ims_list[0]}")
    plt.axis('off')
    plt.subplot(1, 6, 2)
    plt.imshow(i1)
    plt.title(f"{ims_list[1]}")
    plt.axis('off')
    plt.subplot(1, 6, 3)
    plt.imshow(i2)
    plt.title(f"{ims_list[2]}")
    plt.axis('off')
    plt.subplot(1, 6, 4)
    plt.imshow(i3)
    plt.title(f"{ims_list[3]}")
    plt.axis('off')
    plt.subplot(1, 6, 5)
    plt.imshow(i4)
    plt.title(f"{ims_list[4]}")
    plt.axis('off')
    plt.subplot(1, 6, 6)
    plt.imshow(i5)
    plt.title(f"{ims_list[5]}")
    plt.axis('off')
    
    plt.show()
