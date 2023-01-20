from glob import glob
import numpy as np
from matplotlib import pyplot as plt
import os, random, math, cv2
import numpy as np
import pandas as pd
from albumentations.augmentations.geometric.transforms import *
import albumentations

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
    
  
def random_bright(img):
    
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    img = np.array(img, dtype=np.float64)
    random_bright = .5 + np.random.uniform()
    img[:, :, 2] = img[:, :, 2] * random_bright
    img[:, :, 2][img[:, :, 2] > 255] = 255
    img = np.array(img, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    
    return img

def partial_write(Plate, label, num_list, num_ims, plate_chars, num_size, row, col):
    
    plate_int = int(plate_chars[-4])
    label += num_list[plate_int]
    Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[-4]], num_size)
    col += num_size[0]

    # number 5
    plate_int = int(plate_chars[-3])
    label += num_list[plate_int]
    Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[-3]], num_size)
    col += num_size[0]

    # number 6
    plate_int = int(plate_chars[-2])
    label += num_list[plate_int]
    Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[-2]], num_size)
    col += num_size[0]

    # number 7
    plate_int = int(plate_chars[-1])
    label += num_list[plate_int]
    Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[-1]], num_size)
    col += num_size[0]
    
    return Plate, label
    
def write(Plate, label, num_list, num_ims, init_size, plate_chars, num_size, num_size_2, char_ims, char_size, label_prefix, row, col):
    
    # number 1
    plate_int = int(plate_chars[-7])
    label += num_list[plate_int]
    Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[-7]], num_size) #(56, 83)
    col += num_size[0]

    # number 2
    plate_int = int(plate_chars[-6])
    label += num_list[plate_int]
    Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[-6]], num_size)
    col += num_size[0]

    if label_prefix == "yellow" or label_prefix == "green_old":
        row, col = 72, 8
    else:
        pass

    # character 3
    if label_prefix == "short" or label_prefix == "long":

        label += plate_chars[-5]
        # try:
        Plate[row:row + char_size[1], col:col + char_size[0], :] = cv2.resize(char_ims[plate_chars[-5]], char_size)

        if label_prefix == "short":
            col += (char_size[0] + init_size[1])
        else:
            col += (char_size[0] + 25)
        # except:
        #     print(plate_chars[-5])

    else:
        label += plate_chars[-5]
        try:
            Plate[row:row + char_size[1], col:col + char_size[0], :] = cv2.resize(char_ims[plate_chars[-5]], char_size)
            col += char_size[0]

            if label_prefix == "green":
                row, col = 75, 8
        except:
            print(plate_chars[-5])
    
    if num_size_2 != None:
        Plate, label = partial_write(Plate, label, num_list, num_ims, plate_chars, num_size_2, row, col)
    else:
        Plate, label = partial_write(Plate, label, num_list, num_ims, plate_chars, num_size, row, col)
        
    return Plate, label

def save(save, Plate, save_path, label):
    
    Plate = random_bright(Plate)
    if save:
        # tfs = albumentations.Compose([Affine(rotate=[-7, 7], shear=None, p=0.5),
        #                  Perspective(scale=(0.05, 0.12), p=0.5)])
        # Plate = tfs(image=Plate)
        cv2.imwrite(save_path + label + ".jpg", Plate)
    else:
        pass

def load(files_path):
    
    chars_paths = sorted(os.listdir(files_path))
    ims, chars = {}, [] 

    for char_path in chars_paths:
        fname = os.path.splitext(char_path)[0]
        im = cv2.imread(os.path.join(files_path, char_path))
        ims[fname] = im
        chars.append(char_path[0:-4])
        
    return ims, chars

def preprocess(plate_path, plate_size, label_prefix, init_size):
    
    Plate = cv2.resize(cv2.imread(plate_path), plate_size)
    label = label_prefix 
    # row -> y , col -> x
    row, col = init_size[0], init_size[1]  # row + 83, col + 56
    
    return Plate, label, row, col
    

def generate_plate(plate_path, num, plate, plate_size, num_size, num_size_2,
                   char_size, init_size, num_list, char_list, num_ims, char_ims, 
                   regions, region_name, region_size, save_path, label_prefix, save_):
    
    plate_chars = [char for char in plate]

    for i, n in enumerate(range(num)):
        
        Plate, label, row, col = preprocess(plate_path, plate_size, label_prefix, init_size)
        
        if label_prefix == "yellow" or label_prefix == "green_old":
            Plate[row:row + region_size[1], col:col + region_size[0], :] = cv2.resize(regions[region_name], region_size) # 88,60
            col += region_size[0] + 8
        else:
            pass
            
        Plate, label = write(Plate=Plate, label=label, num_list=num_list, num_ims=num_ims, 
                             init_size=init_size, plate_chars=plate_chars, num_size=num_size, 
                             num_size_2=num_size_2, char_ims=char_ims, char_size=char_size, 
                             label_prefix=label_prefix, row=row, col=col)
        
        if save_: save(save, Plate, save_path, label)
    
    print("Done")
