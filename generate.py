import argparse, os
from plate_generator import PlateGenerator
import pandas as pd

    
parser = argparse.ArgumentParser()
parser.add_argument("-dp", "--data_path", help="Path to the csv file",
                    type=str, default="test.csv")
parser.add_argument("-sp", "--save_path", help="save image directory",
                    type=str, default="./new_samples/to_test_new/")
parser.add_argument("-n", "--num", help="number of image",
                    type=int, default=3)
parser.add_argument("-s", "--save", help="save or imshow",
                    type=bool, default=True)
parser.add_argument("-r", "--random", help="Random plate numbers",
                    type=bool, default=True)

args = parser.parse_args()
save_path = args.save_path
data_path = args.data_path
random = args.random
Save = args.save
sample = "100마0000"
# sample = "서울17마0000"

if random:
    generator = PlateGenerator(save_path=save_path, random=random)
    if len(sample) > 8:
        split_ = os.path.splitext(os.path.basename(sample))[0]
        region_name = split_[:2]
        digits = split_[2:]
        generator.Generation(digits, save=Save, num=10, plate_type="yellow", region_name=region_name)
    else:
        generator.Generation(sample, save=Save, num=10, plate_type="long")
    

else:
    generator = PlateGenerator(save_path=save_path, random=random)
    df = pd.read_csv("test.csv")
    texts = [os.path.basename(filename) for filename in df["filename"]]
    
    for sample in texts:
        if len(sample) > 8:
            split_ = os.path.splitext(os.path.basename(sample))[0]
            region_name = split_[:2]
            digits = split_[2:]
            generator.Generation(digits, save=Save, plate_type="yellow", region_name=region_name)
        else:
            generator.Generation(sample, save=Save, plate_type="long")
