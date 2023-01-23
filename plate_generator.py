from utils import *

class PlateGenerator:
    
    def __init__(self, save_path, random):
        
        self.save_path = save_path
        self.random = random

        # Basic nums and chars
        self.num_ims, self.num_lists = load("./num/")
        self.char_ims, self.char_lists = load("./char1/")

        # Yellow nums and chars
        self.num_ims_yellow, self.num_lists_yellow = load("./num_y/")
        self.char_ims_yellow, self.char_lists_yellow = load("./char1_y/")
        self.regions_yellow, self.regions_lists_yellow = load("./region_y/")
       
        # Green nums and chars
        self.num_ims_green, self.num_lists_green = load("./num_g/")
        self.char_ims_green, self.char_lists_green = load("./char1_g/")
        self.regions_green, self.regions_lists_green = load("./region_g/")

    def Generation(self, plate, save, plate_type, num=None, region_name=None):
        
        assert plate_type in ["short", "long", "yellow", "old", "green"], "Please choose the correct the plate type"
        
        if num != None:
            for i in range(num):
                if plate_type == "long":
                    generate_plate(plate_path="plate.jpg", random=self.random,
                               plate=plate, num_size=(56, 83), num_size_2=None, 
                               num_list=self.num_lists, init_size=(13, 36), # start from left to right
                               char_list=self.char_lists, regions=None, three_digit = None,
                               num_ims=self.num_ims, char_size=(60, 83), region_name=None,
                               char_ims=self.char_ims, label_prefix=plate_type,
                               save_path=self.save_path, region_size=None,
                               save_=save, plate_size=(520, 110))

                elif plate_type == "short":
                    generate_plate(plate_path="plate.jpg",  random=self.random,
                               plate=plate, num_size=(40, 83), num_size_2=None, 
                               num_list=self.num_lists, init_size=(46, 10),
                               char_list=self.char_lists, regions=None, three_digit = None,
                               num_ims=self.num_ims, char_size=(49, 70),  region_name=None,
                               char_ims=self.char_ims, label_prefix=plate_type,
                               save_path=self.save_path, region_size=None,
                               save_=save, plate_size=(355, 155))


                elif plate_type == "yellow":
                    assert region_name != None, "Please insert a region name"
                    assert region_name in [os.path.basename(region) for region in self.regions_lists_yellow], f"Please choose one of these regions: {[os.path.basename(region) for region in self.region_list_y]}"
                    generate_plate(plate_path="plate_y.jpg",  random=self.random,
                               plate=plate, num_size=(44, 60), num_size_2=(64, 90), 
                               num_list=self.num_lists_yellow, char_list=self.char_lists_yellow,
                               num_ims=self.num_ims_yellow, char_ims=self.char_ims_yellow,
                               init_size=(8, 76), # start from left to right
                               regions=self.regions_yellow, three_digit = None,
                               char_size=(64, 62), region_name=region_name,
                               label_prefix=plate_type, all_regions=self.regions_lists_yellow,
                               save_path=self.save_path, region_size=(88, 60),
                               save_=save, plate_size=(336, 170))

                elif plate_type == "old":
                    assert region_name != None, "Please insert a region name"
                    generate_plate(plate_path="plate_g.jpg", 
                               plate=plate, num_size=(44, 60), num_size_2=(64, 90), 
                               num_list=self.num_lists_green, char_list=self.char_lists_green,
                               num_ims=self.num_ims_green, char_ims=self.char_ims_green,
                               init_size=(8, 76), # start from left to right
                               regions=self.regions_green, three_digit = None,
                               char_size=(64, 62), region_name=region_name,
                               label_prefix=plate_type,  random=self.random,
                               save_path=self.save_path, region_size=(88, 60),
                               save_=save, plate_size=(336, 170))

                elif plate_type == "green":
                    generate_plate(plate_path="plate_g.jpg", 
                               plate=plate, num_size=(60, 65), num_size_2=(80, 90), 
                               num_list=self.num_lists_green, char_list=self.char_lists_green,
                               num_ims=self.num_ims_green, char_ims=self.char_ims_green, region_size=None,
                               init_size=(8, 78),  random=self.random, 
                               char_size=(60, 65), label_prefix=plate_type, regions=None,
                               save_path=self.save_path, region_name=None, three_digit = None,
                               save_=save, plate_size=(336, 170))
