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

def load(files_path):
    
    chars_paths = sorted(os.listdir(files_path))
    ims, chars = {}, [] 

    for char_path in chars_paths:
        fname = os.path.splitext(char_path)[0]
        im = cv2.imread(os.path.join(files_path, char_path))
        ims[fname] = im
        chars.append(char_path[0:-4])
        
    return ims, chars

def generate_plate(plate_path, num, plate, plate_size, num_size, num_size_2, char_size, init_size, num_list, char_list, num_ims, char_ims, save_path, label_prefix, save):
    
    Plate = cv2.resize(cv2.imread(plate_path), plate_size)
    plate_chars = [char for char in plate]
    
    if regions != None:
        regions = [cv2.resize(region, region_size) for region in regions]

    for i, n in enumerate(range(num)):
        Plate = cv2.resize(cv2.imread(plate_path), plate_size)
        label = label_prefix # first letter when save the image
        # row -> y , col -> x
        row, col = init_size[0], init_size[1]  # row + 83, col + 56
        
        Plate[row:row + 60, col:col + 88, :] = regions[i % 16]
            col += 88 + 8
        
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

        # character 3
        label += plate_chars[2]
        try:
            Plate[row:row + char_size[1], col:col + char_size[0], :] = cv2.resize(char_ims[plate_chars[2]], char_size)
            col += (char_size[0] + init_size[1])
        except:
            print(plate_chars[2])

        if num_size_2 != None:
            print("Not none!")
            plate_int = int(plate_chars[3])
            label += num_list[plate_int]
            Plate[row:row + num_size_2[1], col:col + num_size_2[0], :] = cv2.resize(num_ims[plate_chars[3]], num_size_2)
            col += num_size_2[0]

            # number 5
            plate_int = int(plate_chars[4])
            label += num_list[plate_int]
            Plate[row:row + num_size_2[1], col:col + num_size_2[0], :] = cv2.resize(num_ims[plate_chars[4]], num_size_2)
            col += num_size_2[0]

            # number 6
            plate_int = int(plate_chars[5])
            label += num_list[plate_int]
            Plate[row:row + num_size_2[1], col:col + num_size_2[0], :] = cv2.resize(num_ims[plate_chars[5]], num_size_2)
            col += num_size_2[0]

            # number 7
            plate_int = int(plate_chars[6])
            label += num_list[plate_int]
            Plate[row:row + num_size_2[1], col:col + num_size_2[0], :] = cv2.resize(num_ims[plate_chars[6]], num_size_2)
            col += num_size_2[0]

            Plate = random_bright(Plate)
            if save:
                # tfs = albumentations.Compose([Affine(rotate=[-7, 7], shear=None, p=0.5),
                #                  Perspective(scale=(0.05, 0.12), p=0.5)])
                # Plate = tfs(image=Plate)
                cv2.imwrite(save_path + label + ".jpg", Plate)
            else:
                pass
        
        else:
            # number 4
            plate_int = int(plate_chars[3])
            label += num_list[plate_int]
            Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[3]], num_size)
            col += num_size[0]

            # number 5
            plate_int = int(plate_chars[4])
            label += num_list[plate_int]
            Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[4]], num_size)
            col += num_size[0]

            # number 6
            plate_int = int(plate_chars[5])
            label += num_list[plate_int]
            Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[5]], num_size)
            col += num_size[0]

            # number 7
            plate_int = int(plate_chars[6])
            label += num_list[plate_int]
            Plate[row:row + num_size[1], col:col + num_size[0], :] = cv2.resize(num_ims[plate_chars[6]], num_size)
            col += num_size[0]

            Plate = random_bright(Plate)
            if save:
                # tfs = albumentations.Compose([Affine(rotate=[-7, 7], shear=None, p=0.5),
                #                  Perspective(scale=(0.05, 0.12), p=0.5)])
                # Plate = tfs(image=Plate)
                cv2.imwrite(save_path + label + ".jpg", Plate)
            else:
                pass
        
class ImageGenerator:
    
    def __init__(self, save_path):
        self.save_path = save_path
        # Plate
        self.plate = cv2.imread("plate.jpg")
        self.plate2 = cv2.imread("plate_y.jpg")
        self.plate3 = cv2.imread("plate_g.jpg")

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
        
        if plate_type == "short":
            generate_plate(plate_path="plate.jpg", 
                       plate=plate, num=num, num_size=(45, 83), num_size_2=None, 
                       num_list=self.number_list, init_size=(46, 10),
                       char_list=self.char_list, regions=None,
                       num_ims=self.Number, char_size=(49, 70),
                       char_ims=self.Char1, label_prefix=plate_type,
                       save_path=self.save_path, region_size=(88, 60)
                       save=save, plate_size=(355, 155))
        
        elif plate_type == "long":
            generate_plate(plate_path="plate.jpg", 
                       plate=plate, num=num, num_size=(56, 83), num_size_2=None, 
                       num_list=self.number_list, init_size=(13, 36), # start from left to right
                       char_list=self.char_list, regions=None,
                       num_ims=self.Number, char_size=(60, 83),
                       char_ims=self.Char1, label_prefix=plate_type,
                       save_path=self.save_path, region_size=(88, 60)
                       save=save, plate_size=(520, 110))
            
        elif plate_type == "yellow":
            generate_plate(plate_path="plate_y.jpg", 
                       plate=plate, num=num, num_size=(44, 60), num_size_2=(64, 90), 
                       num_list=self.number_list, init_size=(8, 76), # start from left to right
                       char_list=self.char_list, regions=self.Region_y,
                       num_ims=self.Number, char_size=(64, 62),
                       char_ims=self.Char1, label_prefix=plate_type,
                       save_path=self.save_path, region_size=(88, 60),
                       save=save, plate_size=(336, 170))
    
    def Type_3(self, num, plate, save=False):
        
        number1 = [cv2.resize(number, (44, 60)) for number in self.Number_y]
        number2 = [cv2.resize(number, (64, 90)) for number in self.Number_y]
        region = [cv2.resize(region, (88, 60)) for region in self.Region_y]
        # char = [cv2.resize(char1, (64, 62)) for char1 in self.Char1_y]
        
        plate_chars = []
        for char in plate:
            plate_chars.append(char)

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate2, (336, 170))

            label = "3_"
            # row -> y , col -> x
            row, col = 8, 76

            # region
            label += self.region_list_y[i % 16]
            Plate[row:row + 60, col:col + 88, :] = region[i % 16]
            col += 88 + 8

            # number 1
            rand_int = int(plate_chars[0])
            label += self.number_list_y[rand_int]
            Plate[row:row + 60, col:col + 44, :] = number1[rand_int]
            col += 44

            # number 2
            rand_int = int(plate_chars[1])
            label += self.number_list_y[rand_int]
            Plate[row:row + 60, col:col + 44, :] = number1[rand_int]

            row, col = 72, 8

            # character 3
            label += plate_chars[2]
            try:
                Plate[row:row + 62, col:col + 64, :] = cv2.resize(self.Char1_y[plate_chars[2]], (64, 62))
                # Plate[row:row + 68, col:col + 70, :] = cv2.resize(self.Char1_y[plate_chars[2]], (70, 68))
                col += 64
            except:
                print(plate_chars[2])
            
            # number 4
            rand_int = int(plate_chars[3])
            label += self.number_list_y[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 5
            rand_int = int(plate_chars[4])
            label += self.number_list_y[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 6
            rand_int = int(plate_chars[5])
            label += self.number_list_y[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 7
            rand_int = int(plate_chars[6])
            label += self.number_list_y[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            
            Plate = random_bright(Plate)
            if save:
                cv2.imwrite(self.save_path + label + ".jpg", Plate)
            else:
                cv2.imshow(label, Plate)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def Type_4(self, num, plate, save=False):
        
        number1 = [cv2.resize(number, (44, 60)) for number in self.Number_g]
        number2 = [cv2.resize(number, (64, 90)) for number in self.Number_g]
        region = [cv2.resize(region, (88, 60)) for region in self.Region_g]
        
        plate_chars = []
        for char in plate:
            plate_chars.append(char)

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate3, (336, 170))

            label = "4_"
            # row -> y , col -> x
            row, col = 8, 76

            # region
            label += self.region_list_g[i % 16]
            Plate[row:row + 60, col:col + 88, :] = region[i % 16]
            col += 88 + 8

            # number 1
            rand_int = int(plate_chars[0])
            label += self.number_list_g[rand_int]
            Plate[row:row + 60, col:col + 44, :] = number1[rand_int]
            col += 44

            # number 2
            rand_int = int(plate_chars[1])
            label += self.number_list_g[rand_int]
            Plate[row:row + 60, col:col + 44, :] = number1[rand_int]

            row, col = 72, 8

            # character 3
            label += plate_chars[2]
            try:
                Plate[row:row + 62, col:col + 64, :] = cv2.resize(self.Char1_g[plate_chars[2]], (64, 62))
                col += 64
            except:
                print(plate_chars[2])

            # number 4
            rand_int = int(plate_chars[3])
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 5
            rand_int = int(plate_chars[4])
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 6
            rand_int = int(plate_chars[5])
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            col += 64

            # number 7
            rand_int = int(plate_chars[6])
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            Plate = random_bright(Plate)
            if save:
                cv2.imwrite(self.save_path + label + ".jpg", Plate)
            else:
                cv2.imshow(label, Plate)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def Type_5(self, num, plate, save=False):
        
        number1 = [cv2.resize(number, (60, 65)) for number in self.Number_g]
        number2 = [cv2.resize(number, (80, 90)) for number in self.Number_g]
        # char = [cv2.resize(char1, (60, 65)) for char1 in self.Char1_g]
        
        plate_chars = []
        for char in plate:
            plate_chars.append(char)

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate3, (336, 170))
            random_width, random_height = 336, 170
            label = "5_"

            # row -> y , col -> x
            row, col = 8, 78

            # number 1
            rand_int = int(plate_chars[0])
            label += self.number_list_g[rand_int]
            Plate[row:row + 65, col:col + 60, :] = number1[rand_int]
            col += 60

            # number 2
            rand_int = int(plate_chars[1])
            label += self.number_list_g[rand_int]
            Plate[row:row + 65, col:col + 60, :] = number1[rand_int]
            col += 60

            # character 3
            label += plate_chars[2]
            try:
                Plate[row:row + 65, col:col + 60, :] = cv2.resize(self.Char1_g[plate_chars[2]], (60, 65))
            except:
                print(plate_chars[2])
            
            row, col = 75, 8
            # number 4
            rand_int = int(plate_chars[3])
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]
            col += 80


            # number 5
            rand_int = int(plate_chars[4])
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]
            # Plate[row:row + 90, col:col + 80, :] = cv2.resize(number2[rand_int], (58, 90))
            col += 80

            # number 6
            rand_int = int(plate_chars[5])
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]
            col += 80

            # number 7
            rand_int = int(plate_chars[6])
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]

            Plate = random_bright(Plate)

            if save:
                cv2.imwrite(self.save_path + label + ".jpg", Plate)
            else:
                cv2.imshow(label, Plate)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

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
                                        "13소1489", "24자1789", "48육4785",])
args = parser.parse_args()


img_dir = args.img_dir
A = ImageGenerator(img_dir)

num_img = args.num
Save = args.save

plates = args.plates

# df = pd.read_csv("/home/ubuntu/workspace/bekhzod/imagen/lp_recognition_cropped/labels.csv")
# texts = []
# for i, name in (enumerate(df['filename'])):
#     if i == 10000:
#         break
#     plate_num = os.path.splitext(name)[0]
#     if len(plate_num) < 8:
#         texts.append(plate_num)

# for idx in range(1, len(texts) + 1):
#     A.Type_1(idx, texts[idx - 1], save=Save)
#     print(f"Plate {texts[idx - 1]} is generated and saved in {img_dir} as {texts[idx - 1]}.jpg!")


# for idx in range(1, len(plates) + 1):
#     A.Type_1(idx, plates[idx - 1], save=Save)
#     print(f"Plate {plates[idx - 1]} is generated and saved in {img_dir} as {plates[idx - 1]}.jpg!")
#     with Image(filename =f"{img_dir}{plates[idx - 1]}.jpg") as img:
#         lens = 80
#         film = 105
#         args = (
#             lens/film * 180/math.pi,
#         )

#         arguments = (0, 0, 12, 1,
#                      90, 0, 85, 2,
#                      0, 90, 10, 88,
#                      90, 90, 88, 91)

#         img.distort('plane_2_cylinder', args)
#         img.distort('perspective', arguments)
#         img.distort('arc', (15, ))
#         img.save(filename=f"{img_dir}{plates[idx - 1]}.png")
        
for idx in range(23, len(plates) + 1):
    # A.Generation(idx, plates[idx - 1], save=Save, plate_type="long")
    # A.Generation(idx, plates[idx - 1], save=Save, plate_type="short")
    A.Generation(idx, plates[idx - 1], save=Save, plate_type="yellow")
    # A.Type_1(idx, plates[idx - 1], save=Save)
    # print(f"Plate {plates[idx - 1]} is generated and saved in {img_dir} as {plates[idx - 1]}.jpg!")
    # A.Type_2(idx, plates[idx - 1], save=Save)
    # print(f"Plate {plates[idx - 1]} is generated and saved in {img_dir} as {plates[idx - 1]}.jpg!")
    # A.Type_3(idx, plates[idx - 1], save=Save)
    # print(f"Plate {plates[idx - 1]} is generated and saved in {img_dir} as {plates[idx - 1]}.jpg!")
    # A.Type_4(idx, plates[idx - 1], save=Save)
    # print(f"Plate {plates[idx - 1]} is generated and saved in {img_dir} as {plates[idx - 1]}.jpg!")
    # A.Type_5(idx, plates[idx - 1], save=Save)
    # print(f"Plate {plates[idx - 1]} is generated and saved in {img_dir} as {plates[idx - 1]}.jpg!")
