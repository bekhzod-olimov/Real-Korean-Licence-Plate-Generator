import os, random, math
import cv2
import numpy as np
import pandas as pd
from albumentations.augmentations.geometric.transforms import *
import albumentations

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
    
def write(Plate, label, num_list, num_ims, init_size, three_digit, plate_chars, num_size, num_size_2, char_ims, char_size, label_prefix, row, col):
    
    # number 1
    plate_int = int(plate_chars[0])
    label += num_list[plate_int]
    Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[0]], num_size) #(56, 83)
    col += num_size[0]

    # number 2
    plate_int = int(plate_chars[1])
    label += num_list[plate_int]
    Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[1]], num_size)
    col += num_size[0]
    
    if three_digit:
        
        plate_int = int(plate_chars[2])
        label += num_list[plate_int]
        Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[2]], num_size)
        col += num_size[0]

    if label_prefix == "yellow" or label_prefix == "old":
        row, col = 72, 8

    # character 3
    if label_prefix == "short" or label_prefix == "long":

        label += plate_chars[-5]
        try:
            Plate[row:row + char_size[1], col:col + char_size[0], :] = cv2.resize(char_ims[plate_chars[-5]], char_size)
        except:
            print(plate_chars[-5])
            
        if label_prefix == "short":
            col += (char_size[0] + init_size[1])
        else:
            col += (char_size[0] + 25)

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

def save(Plate, save_path, transformations, label):
    
    if transformations:
        Plate = random_bright(Plate)
        tfs = albumentations.Compose([Affine(rotate=[-7, 7], shear=None, p=0.5),
                         Perspective(scale=(0.05, 0.12), p=0.5)])
        Plate = tfs(image=Plate)["image"]
        # print(type(Plate))
    
    folder = label.split('_')[0]
    save_dir = os.path.join(save_path, folder)
    os.makedirs(save_dir, exist_ok = True)
    cv2.imwrite(os.path.join(save_dir, f"{label.split('_')[1]}") + ".jpg", Plate)
    print(f"Plate {label.split('_')[1]}.jpg is saved to {save_dir}/!")

def load(files_path):
    
    chars_paths = sorted(os.listdir(files_path))
    ims, chars = {}, [] 

    for char_path in chars_paths:
        fname = os.path.splitext(char_path)[0]
        im = cv2.imread(os.path.join(files_path, char_path))
        ims[fname] = im
        chars.append(char_path[0:-4])
        
    return ims, chars

def preprocess(plate_path, plate_size, label_prefix, init_size, three_digit, plate_chars):
    
    Plate = cv2.resize(cv2.imread(plate_path), plate_size)
    label = f"{label_prefix}_" 
    row, col = init_size[0], init_size[1]
    
    if len(plate_chars) > 7:
        
        three_digit = True
        if label_prefix == "long":
            row, col = init_size[0] + 2, init_size[1] - 18 
        elif label_prefix == "short":
            row, col = init_size[0] - 5, init_size[1] - 5 
        elif label_prefix in ["old", "yellow"]:
            row, col = init_size[0], init_size[1] - 20 
        elif label_prefix == "green":
            row, col = init_size[0], init_size[1] - 35 
    
    return Plate, label, row, col, three_digit
    

def generate_plate(plate_path, plate, plate_size, num_size, num_size_2,
                   char_size, init_size, num_list, three_digit, char_list, num_ims, char_ims, 
                   regions, region_name, region_size, save_path, label_prefix, save_):
    
    plate_chars = [char for char in plate]
    Plate, label, row, col, three_digit = preprocess(plate_path, plate_size, label_prefix, init_size, three_digit, plate_chars)

    if label_prefix == "yellow" or label_prefix == "old":
        Plate[row:row + region_size[1], col:col + region_size[0], :] = cv2.resize(regions[region_name], region_size)
        col += region_size[0] + 8

    Plate, label = write(Plate=Plate, label=label, num_list=num_list, num_ims=num_ims, 
                         init_size=init_size, three_digit=three_digit, plate_chars=plate_chars, 
                         num_size_2=num_size_2, char_ims=char_ims, char_size=char_size, 
                         label_prefix=label_prefix, row=row, num_size=num_size, col=col)

    if save_: save(Plate=Plate, save_path=save_path, transformations=True, label=label)
