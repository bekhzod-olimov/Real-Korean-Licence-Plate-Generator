import argparse, os
from plate_generator import PlateGenerator
import pandas as pd

    
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--img_dir", help="save image directory",
                    type=str, default="./new_samples/to_test_new/")
parser.add_argument("-n", "--num", help="number of image",
                    type=int, default=3)
parser.add_argument("-s", "--save", help="save or imshow",
                    type=bool, default=True)

args = parser.parse_args()
img_dir = args.img_dir
generator = PlateGenerator(img_dir)

# num_img = args.num
Save = args.save

plates = args.plates

# df = pd.read_csv("/home/ubuntu/workspace/bekhzod/imagen/lp_recognition_cropped/train/labels.csv")
df = pd.read_csv("test.csv")
texts = []
for i, name in (enumerate(df['filename'])):
    plate_num = os.path.splitext(name)[0]
    texts.append(plate_num)
        
for idx, im_path in enumerate(texts):
    if len(im_path) < 8:
        generator.Generation(im_path, save=Save, plate_type="long")
    elif len(im_path) > 8:
        split_ = os.path.splitext(os.path.basename(im_path))[0]
        region_name = split_[:2]
        digits = split_[2:]
        generator.Generation(digits, save=Save, plate_type="yellow", region_name=region_name)
        


