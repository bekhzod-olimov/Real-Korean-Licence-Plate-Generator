import argparse
from plate_generator import PlateGenerator

    
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
                                        "13소1489", "24자1789", "144육4785",])
args = parser.parse_args()


img_dir = args.img_dir
A = PlateGenerator(img_dir)

num_img = args.num
Save = args.save

plates = args.plates

for idx in range(24, len(plates) + 1):
    A.Generation(plates[idx - 1], save=Save, plate_type="long")
    A.Generation(plates[idx - 1], save=Save, plate_type="short")
    A.Generation(plates[idx - 1], save=Save, plate_type="yellow")
    A.Generation(plates[idx - 1], save=Save, plate_type="old")
    A.Generation(plates[idx - 1], save=Save, plate_type="green")
