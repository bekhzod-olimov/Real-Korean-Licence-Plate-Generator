import os, random, math
# from wand.image import Image
import cv2, argparse
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
    
        
class ImageGenerator:
    
    def __init__(self, save_path):
        
        self.save_path = save_path

        # Basic nums and chars
        self.Number, self.number_list = load("./num/")
        self.Char1, self.char_list = load("./char1/")

        # Yellow nums and chars
        self.Number_y, self.number_list_y = load("./num_y/")
        self.Char1_y, self.char_list_y = load("./char1_y/")
        self.Region_y, self.region_list_y = load("./region_y/")
       
        # Green nums and chars
        self.Number_g, self.number_list_g = load("./num_g/")
        self.Char1_g, self.char_list_g = load("./char1_g/")
        self.Region_g, self.region_list_g = load("./region_g/")

    def Generation(self, num, plate, save, plate_type):
        
        assert plate_type in ["short", "long", "yellow", "green_old", "green"], "Please choose the correct the plate type"
        
        if plate_type == "short":
            generate_plate(plate_path="plate.jpg", 
                       plate=plate, num=num, num_size=(45, 83), num_size_2=None, 
                       num_list=self.number_list, init_size=(46, 10),
                       char_list=self.char_list, regions=None,
                       num_ims=self.Number, char_size=(49, 70),  region_name=None,
                       char_ims=self.Char1, label_prefix=plate_type,
                       save_path=self.save_path, region_size=None,
                       save_=save, plate_size=(355, 155))
        
        elif plate_type == "long":
            generate_plate(plate_path="plate.jpg", 
                       plate=plate, num=num, num_size=(56, 83), num_size_2=None, 
                       num_list=self.number_list, init_size=(13, 36), # start from left to right
                       char_list=self.char_list, regions=None,
                       num_ims=self.Number, char_size=(60, 83), region_name=None,
                       char_ims=self.Char1, label_prefix=plate_type,
                       save_path=self.save_path, region_size=None,
                       save_=save, plate_size=(520, 110))
            
        elif plate_type == "yellow":
            generate_plate(plate_path="plate_y.jpg", 
                       plate=plate, num=num, num_size=(44, 60), num_size_2=(64, 90), 
                       num_list=self.number_list_y, char_list=self.char_list_y,
                       num_ims=self.Number_y, char_ims=self.Char1_y,
                       init_size=(8, 76), # start from left to right
                       regions=self.Region_y,
                       char_size=(64, 62), region_name="서울",
                       label_prefix=plate_type,
                       save_path=self.save_path, region_size=(88, 60),
                       save_=save, plate_size=(336, 170))
            
        elif plate_type == "green_old":
            generate_plate(plate_path="plate_g.jpg", 
                       plate=plate, num=num, num_size=(44, 60), num_size_2=(64, 90), 
                       num_list=self.number_list_g, char_list=self.char_list_g,
                       num_ims=self.Number_g, char_ims=self.Char1_g,
                       init_size=(8, 76), # start from left to right
                       regions=self.Region_g, 
                       char_size=(64, 62), region_name="서울",
                       label_prefix=plate_type,
                       save_path=self.save_path, region_size=(88, 60),
                       save_=save, plate_size=(336, 170))
            
        elif plate_type == "green":
            generate_plate(plate_path="plate_g.jpg", 
                       plate=plate, num=num, num_size=(60, 65), num_size_2=(80, 90), 
                       num_list=self.number_list_g, char_list=self.char_list_g,
                       num_ims=self.Number_g, char_ims=self.Char1_g, region_size=None,
                       init_size=(8, 78), # start from left to right
                       char_size=(60, 65), label_prefix=plate_type, regions=None,
                       save_path=self.save_path, region_name=None,
                       save_=save, plate_size=(336, 170))
    
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--img_dir", help="save image directory",
                    type=str, default="./new_samples/to_test/")
parser.add_argument("-n", "--num", help="number of image",
                    type=int, default=3)
parser.add_argument("-s", "--save", help="save or imshow",
                    type=bool, default=True)
parser.add_argument("-p", "--plates", help="plate to generate",
                    type=list, default=["12가3456", "98마2478", "47오7895",
                                        "15로1007", "08사0793", "84모4711",
                                        "46바6908", "37보3564", "71모2471",
                                        "32다2312", "03고0077", "55머6006",
                                        "88호0497", "75주6845", "57어2897",
                                        "19누3471", "07구0793", "24오1788",
                                        "57두6974", "57너3564", "87로5755",
                                        "13소1489", "24자1789", "14육4785",])
args = parser.parse_args()


img_dir = args.img_dir
A = ImageGenerator(img_dir)

num_img = args.num
Save = args.save

plates = args.plates

for idx in range(24, len(plates) + 1):
    A.Generation(idx, plates[idx - 1], save=Save, plate_type="long")
    A.Generation(idx, plates[idx - 1], save=Save, plate_type="short")
    A.Generation(idx, plates[idx - 1], save=Save, plate_type="yellow")
    A.Generation(idx, plates[idx - 1], save=Save, plate_type="green_old")
    A.Generation(idx, plates[idx - 1], save=Save, plate_type="green")
