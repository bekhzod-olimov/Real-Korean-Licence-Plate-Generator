import os, cv2, argparse, shutil
import numpy as np
from glob import glob

parser = argparse.ArgumentParser('Make Dataset for CUT train')
parser.add_argument('--in_im_paths', help = 'Input Images Path', type = str, default='/home/ubuntu/workspace/bekhzod/imagen/Korean-license-plate-Generator/new_samples/augmented')
parser.add_argument('--out_im_paths', help='Output Images Path', type = str, default='/home/ubuntu/workspace/bekhzod/imagen/lp_recognition_cropped/val')
parser.add_argument('--trainA', help = 'trainA Path', type = str, default='/home/ubuntu/workspace/bekhzod/cut/datasets/train_data/trainA')
parser.add_argument('--trainB', help='trainB Path', type = str, default='/home/ubuntu/workspace/bekhzod/cut/datasets/train_data/trainB')
parser.add_argument('--num_imgs', dest='num_ims', help='number of images', type=int, default=1000000)
args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg, getattr(args, arg))

im_files = [".jpg", ".png", ".jpeg"]
input_im_paths = sorted(glob(f"{args.in_im_paths}/*{[im_file for im_file in im_files]}"))
print(len(input_im_paths))
output_im_paths = sorted(glob(f"{args.out_im_paths}/*{[im_file for im_file in im_files]}"))
print(len(output_im_paths))
num_ims = min(args.num_ims, len(input_im_paths))

os.makedirs(args.trainA, exist_ok=True)
os.makedirs(args.trainB, exist_ok=True)

for i, path in enumerate(input_im_paths):
    # if i == 5:
    #     break
    im_name = os.path.basename(path)
    shutil.copy(path, args.trainA)
    shutil.copy(f"{args.out_im_paths}/{im_name}", args.trainB)
