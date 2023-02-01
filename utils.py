import os, random, math
import cv2
import numpy as np
import pandas as pd
from albumentations.augmentations.geometric.transforms import *
import albumentations
from matplotlib import pyplot as plt

def random_bright(img):
    
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    img = np.array(img, dtype=np.float64)
    random_bright = .5 + np.random.uniform()
    img[:, :, 2] = img[:, :, 2] * random_bright
    img[:, :, 2][img[:, :, 2] > 255] = 255
    img = np.array(img, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    
    return img

def partial_write(plate, label, num_list, num_ims, plate_chars, num_size, row, col, random):
    
    if random:
        plate_int = int(np.random.randint(low=0, high=9, size=1))
    else:
        plate_int = int(plate_chars[-4])
        
    label += str(num_list[plate_int])
    plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[str(plate_int)], num_size)
    col += num_size[0]

    # number 5
    if random:
        plate_int = int(np.random.randint(low=0, high=9, size=1))
    else:
        plate_int = int(plate_chars[-3])
    
    label += str(num_list[plate_int])
    plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[str(plate_int)], num_size)
    col += num_size[0] 

    # number 6
    if random:
        plate_int = int(np.random.randint(low=0, high=9, size=1))
    else:
        plate_int = int(plate_chars[-2])
    
    label += str(num_list[plate_int])
    plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[str(plate_int)], num_size)
    col += num_size[0] 

    # number 7
    if random:
        plate_int = int(np.random.randint(low=0, high=9, size=1))
    else:
        plate_int = int(plate_chars[-1])
    
    label += str(num_list[plate_int])
    plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[str(plate_int)], num_size)
    col += num_size[0]
    
    return plate, label
    
def write(plate, label, num_list, num_ims, init_size, three_digit, char_list, plate_chars, num_size, num_size_2, char_ims, char_size, label_prefix, row, col, random):
    
    # number 1
    if random:
        plate_int = int(np.random.randint(low=0, high=9, size=1))
    else:
        plate_int = int(plate_chars[0])

    label += str(num_list[plate_int])
    
    if label_prefix == "basic_north" and three_digit: col -= 20
    elif label_prefix == "basic_europe" and three_digit: col -= 15
    
    if label_prefix == "basic_north":
        row -= 5
        col += 17
    plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[str(plate_int)], num_size) #(56, 83)
    col += num_size[0]

    # number 2
    if random:
        plate_int = int(np.random.randint(low=0, high=9, size=1))
    else:
        plate_int = int(plate_chars[1])
    
    label += str(num_list[plate_int])
    plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[str(plate_int)], num_size)
    col += num_size[0]
    
    if label_prefix == "commercial_europe":
        pass
    
    else:    
        if three_digit:

            if random:
                plate_int = int(np.random.randint(low=0, high=9, size=1))
            else:
                plate_int = int(plate_chars[2])

            label += str(num_list[plate_int])
            plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[str(plate_int)], num_size)
            col += num_size[0]

    if label_prefix == "commercial_north" or label_prefix == "green_old":
        row, col = 72, 8

    # character 3
    if label_prefix == "basic_north" or label_prefix == "basic_europe":

        if random:
            plate_int = int(np.random.randint(low=0, high=9, size=1))
            plate_int = char_list[plate_int]
        else:
            plate_int = (plate_chars[-5])
        
        label += str(plate_int)
        try:
            plate[row:row + char_size[1], col:col + char_size[0], :] = cv2.resize(char_ims[plate_int], char_size)
        except:
            print("\n!!!!!!!!!!!! FILE MISSING ERROR !!!!!!!!!!!!")
            print(f"Character {plate_chars[-5]} is missing!\n")
            
        if label_prefix == "basic_north":
            col += (char_size[0] + init_size[1])
        else:
            col += (char_size[0] + 25)

    else:
        if random:
            plate_int = int(np.random.randint(low=0, high=9, size=1))
            plate_int = char_list[plate_int]
        else:
            plate_int = (plate_chars[-5])
        
        label += str(plate_int)
        
        try:
            plate[row:row + char_size[1], col:col + char_size[0], :] = cv2.resize(char_ims[plate_int], char_size)
            col += char_size[0]

            if label_prefix == "green_basic":
                row, col = 75, 8
        except:
            print("\n!!!!!!!!!!!! FILE MISSING ERROR !!!!!!!!!!!!")
            print(f"Character {plate_chars[-5]} is missing!\n")
    
    if num_size_2 != None:
        plate, label = partial_write(plate, label, num_list, num_ims, plate_chars, num_size_2, row, col, random)
    else:
        plate, label = partial_write(plate, label, num_list, num_ims, plate_chars, num_size, row, col, random)
        
    return plate, label

def save(plate, save_path, transformations, label):
    
    if transformations:
        plate = random_bright(plate)
        tfs = albumentations.Compose([Affine(rotate=[-7, 7], shear=None, p=0.5),
                                      Perspective(scale=(0.02, 0.1), p=0.1)])
        plate = tfs(image=plate)["image"]
    
    folder = label.split('__')[0]
    save_dir = os.path.join(save_path, folder)
    os.makedirs(save_dir, exist_ok = True)
    cv2.imwrite(os.path.join(save_dir, f"{label.split('__')[1]}__{folder}") + ".jpg", plate)
    print(f"Plate {label.split('__')[1]}__{folder}.jpg is saved to {save_dir}/!")

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
    
    plate = cv2.resize(cv2.imread(plate_path), plate_size)
    label = f"{label_prefix}__" 
    row, col = init_size[0], init_size[1]
    
    if len(plate_chars) > 7:
        
        three_digit = True
        if label_prefix == "basic_europe":
            row, col = init_size[0] + 2, init_size[1] - 18 
        elif label_prefix == "basic_north":
            # row, col = init_size[0] - 5, init_size[1] - 5 
            row, col = init_size[0] - 5, 2 
        elif label_prefix in ["green_old", "commercial_north"]:
            row, col = init_size[0], init_size[1] - 20 
        elif label_prefix == "green_basic":
            row, col = init_size[0], init_size[1] - 35 
    
    return plate, label, row, col, three_digit
    

def generate_plate(plate_path, plate, plate_size, num_size, num_size_2, random, all_regions,
                   char_size, init_size, num_list, three_digit, char_list, num_ims, char_ims, 
                   regions, region_name, region_size, save_path, label_prefix, save_):
    
    plate_chars = [char for char in plate]
    plate, label, row, col, three_digit = preprocess(plate_path, plate_size, label_prefix, init_size, three_digit, plate_chars)
    
    if random:
        randint = int(np.random.randint(low=0, high=len(all_regions), size=1))
        region_name = all_regions[randint]

    if label_prefix == "commercial_europe":

        row, col = 10, 25
        to_crop = regions[region_name].shape[1] // 2
        plate[row:row + row * 4, col:col + col * 2, :] = cv2.resize(regions[region_name][:, 0:to_crop], (col * 2, row * 4))
        row += 45
        plate[row:row + row - 15, col:col + col * 2, :] = cv2.resize(regions[region_name][:, to_crop:], (col * 2, row - 15))
        row, col = 13, 100
        
    elif label_prefix in ["commercial_north", "green_old"]:
        plate[row:row + region_size[1], col:col + region_size[0], :] = cv2.resize(regions[region_name], region_size)
        col += region_size[0] + 8
        
    plate, label = write(plate=plate, label=label, num_list=num_list, num_ims=num_ims, random=random,
                         init_size=init_size, three_digit=three_digit, plate_chars=plate_chars, char_list=char_list,
                         num_size_2=num_size_2, char_ims=char_ims, char_size=char_size, 
                         label_prefix=label_prefix, row=row, num_size=num_size, col=col)

    if save_: save(plate=plate, save_path=save_path, transformations=False, label=label)
