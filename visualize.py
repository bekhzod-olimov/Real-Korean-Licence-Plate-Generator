import cv2
from glob import glob
import numpy as np
from matplotlib import pyplot as plt
import os.path as osp


def get_di(ims_list):
    
    ims_names = sorted([osp.basename(name) for name in (glob(f"{ims_list[0]}/*"))])

    return {idx: [f"{im_list}/{im_name}" for _, im_list in enumerate(ims_list)] for (idx, im_name) in enumerate(ims_names)}

def read_ims(ims_list): return [cv2.cvtColor(cv2.imread(im), cv2.COLOR_BGR2RGB) for im in ims_list]
    
def plot(rows, ims, ims_list, ims_len, i):
    
    plt.subplot(rows, ims_len, i+1)
    plt.imshow(ims[i])
    plt.title(f"{ims_list[i]}")
    plt.axis('off')
    
def visualize(ims_list, ims, ims_len, rows = 1):
    
    if len(ims_list) > 7 and len(ims_list) % 2 == 0: rows = 2

    if rows == 1: plt.figure(figsize=(25, 4))        
    else: plt.figure(figsize=(25, 6))        

    for i in range(ims_len):
        if rows == 1: plot(rows, ims, ims_list, ims_len, i)
        else: plot(rows, ims, ims_list, ims_len // 2, i)
