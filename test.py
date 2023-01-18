import os, random, math
from wand.image import Image
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

class ImageGenerator:
    def __init__(self, save_path):
        self.save_path = save_path
        # Plate
        self.plate = cv2.imread("plate.jpg")
        self.plate2 = cv2.imread("plate_y.jpg")
        self.plate3 = cv2.imread("plate_g.jpg")

        # loading Number
        file_path = "./num/"
        file_list = sorted(os.listdir(file_path))
        self.Number = list()
        self.number_list = list()
        for file in file_list:
            img_path = os.path.join(file_path, file)
            img = cv2.imread(img_path)
            self.Number.append(img)
            self.number_list.append(file[0:-4])

        # loading Char
        file_path = "./char1/"
        file_list = sorted(os.listdir(file_path))
        self.char_list = list()
        self.Char1 = dict()
        for file in file_list:
            fname = os.path.splitext(file)[0]
            img_path = os.path.join(file_path, file)
            img = cv2.imread(img_path)
            self.Char1[fname] = img
            self.char_list.append(file[0:-4])
        # print(self.char_list)

        # loading Number ====================  yellow-two-line  ==========================
        file_path = "./num_y/"
        file_list = os.listdir(file_path)
        self.Number_y = list()
        self.number_list_y = list()
        for file in file_list:
            img_path = os.path.join(file_path, file)
            img = cv2.imread(img_path)
            self.Number_y.append(img)
            self.number_list_y.append(file[0:-4])

        # loading Char
        file_path = "./char1_y/"
        file_list = os.listdir(file_path)
        self.char_list_y = list()
        self.Char1_y = list()
        for file in file_list:
            img_path = os.path.join(file_path, file)
            img = cv2.imread(img_path)
            self.Char1_y.append(img)
            self.char_list_y.append(file[0:-4])

        # loading Resion
        file_path = "./region_y/"
        file_list = os.listdir(file_path)
        self.Resion_y = list()
        self.resion_list_y = list()
        for file in file_list:
            img_path = os.path.join(file_path, file)
            img = cv2.imread(img_path)
            self.Resion_y.append(img)
            self.resion_list_y.append(file[0:-4])
        #=========================================================================

        # loading Number ====================  green-two-line  ==========================
        file_path = "./num_g/"
        file_list = os.listdir(file_path)
        self.Number_g = list()
        self.number_list_g = list()
        for file in file_list:
            img_path = os.path.join(file_path, file)
            img = cv2.imread(img_path)
            self.Number_g.append(img)
            self.number_list_g.append(file[0:-4])

        # loading Char
        file_path = "./char1_g/"
        file_list = os.listdir(file_path)
        self.char_list_g = list()
        self.Char1_g = list()
        for file in file_list:
            img_path = os.path.join(file_path, file)
            img = cv2.imread(img_path)
            self.Char1_g.append(img)
            self.char_list_g.append(file[0:-4])

        # loading Resion
        file_path = "./region_g/"
        file_list = os.listdir(file_path)
        self.Resion_g = list()
        self.resion_list_g = list()
        for file in file_list:
            img_path = os.path.join(file_path, file)
            img = cv2.imread(img_path)
            self.Resion_g.append(img)
            self.resion_list_g.append(file[0:-4])
        #=========================================================================


    def Type_1(self, num, plate, save=False):
        number = [cv2.resize(number, (56, 83)) for number in self.Number]
        Plate = cv2.resize(self.plate, (520, 110))
        plate_chars = []
        for char in plate:
            plate_chars.append(char)

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate, (520, 110))
            label = "" # first letter when save the image
            # row -> y , col -> x
            row, col = 13, 35  # row + 83, col + 56
            # number 1
            rand_int = int(plate_chars[0])
            label += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            # number 2
            rand_int = int(plate_chars[1])
            label += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            # character 3
            label += plate_chars[2]
            try:
                Plate[row:row + 83, col:col + 60, :] = cv2.resize(self.Char1[plate_chars[2]], (60, 83))
                col += (60 + 36)
            except:
                print(plate_chars[2])
            
            # number 4
            rand_int = int(plate_chars[3])
            label += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            # number 5
            rand_int = int(plate_chars[4])
            label += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            # number 6
            rand_int = int(plate_chars[5])
            label += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56

            # number 7
            rand_int = int(plate_chars[6])
            label += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            col += 56
            Plate = random_bright(Plate)
            if save:
                tfs = albumentations.Compose([Affine(rotate=[-7, 7], shear=None, p=0.5),
                                 Perspective(scale=(0.05, 0.12), p=0.5)])
                Plate = tfs(image=Plate)
                cv2.imwrite(self.save_path + label + ".jpg", Plate["image"])
            else:
                cv2.imshow(label, Plate)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--img_dir", help="save image directory",
                    type=str, default="./new_samples/augmented/")
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

df = pd.read_csv("/home/ubuntu/workspace/bekhzod/imagen/lp_recognition_cropped/labels.csv")
texts = []
for i, name in (enumerate(df['filename'])):
    if i == 10000:
        break
    plate_num = os.path.splitext(name)[0]
    if len(plate_num) < 8:
        texts.append(plate_num)

for idx in range(1, len(texts) + 1):
    A.Type_1(idx, texts[idx - 1], save=Save)
    print(f"Plate {texts[idx - 1]} is generated and saved in {img_dir} as {texts[idx - 1]}.jpg!")


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
        
# for idx in range(1, len(plates) + 1):
#     A.Type_1(idx, plates[idx - 1], save=Save)
#     print(f"Plate {plates[idx - 1]} is generated and saved in {img_dir} as {plates[idx - 1]}.jpg!")

# A.Type_2(num_img, save=Save)
# print("Type 2 finish")
# A.Type_3(num_img, save=Save)
# print("Type 3 finish")
# A.Type_4(num_img, save=Save)
# print("Type 4 finish")
# A.Type_5(num_img, save=Save)
# print("Type 5 finish")
