from utils import *

class PlateGenerator:
    
    def __init__(self, save_path, random):
        
        self.save_path = save_path
        self.random = random
        self.plate_types = ["basic_europe", "basic_north", "commercial_europe", "commercial_north", "green_old", "green_basic"]

        # Basic nums and chars
        self.num_ims, self.num_lists = load("./digits/")
        # self.num_ims, self.num_lists = load("./digits_uzbek/")
        self.char_ims, self.char_lists = load("./characters/")

        # Yellow nums and chars
        self.num_ims_yellow, self.num_lists_yellow = load("./digits_yellow/")
        self.char_ims_yellow, self.char_lists_yellow = load("./characters_yellow/")
        self.regions_yellow, self.regions_lists_yellow = load("./regions_yellow/")
       
        # Green nums and chars
        self.num_ims_green, self.num_lists_green = load("./digits_green/")
        self.char_ims_green, self.char_lists_green = load("./characters_green/")
        self.regions_green, self.regions_lists_green = load("./regions_green/")
        
    def preprocessing(self, plate, random, plate_types):
        
        if random:
            try:
                plate_type = plate_types[int(np.random.choice(np.arange(0, len(plate_types)), p=[0.33, 0.32, 0.15, 0.15, 0.03, 0.02]))]

                init_digit_types = ["three", "two"]
                init_digit = init_digit_types[int(np.random.choice(np.arange(0, len(init_digit_types)), p=[0.4, 0.6]))]

                if plate_type in ["basic_europe", "basic_north", "green_basic"]: 
                    three_digit, plate = True if init_digit == "three" else False, "01마0000"

                elif plate_type in ["commercial_europe", "commercial_north", "green_old"]: 
                    three_digit, plate = False, "경기01마0101"
            
            except:
                pass
            
        else:
            if plate[0].isalpha(): 
                three_digit, plate_type  = False, "commercial_europe"
            elif plate[0].isdigit():
                three_digit, plate_type = True if len(plate) > 7 else False, "basic_europe"
        
        if plate_type in ["commercial_north", "commercial_europe", "green_old"]:
            
            split = os.path.splitext(os.path.basename(plate))[0]
            region_name, digits = split[:2], split[2:]
            
        else: digits, region_name = None, None
        
        return three_digit, plate, plate_type, digits, region_name
    
    def assertion(self, region_name, region_names):
        
        assert region_name != None, "Please insert a region name"
        assert region_name in [os.path.basename(region) for region in region_names], f"Please choose one of these regions: {[os.path.basename(region) for region in region_names]}"
    
    def generation(self, plate, save, plate_type, num, region_name):
        
        for _ in range(num):
            
            three_digit, plate, plate_type, digits, region_name = self.preprocessing(plate, self.random, self.plate_types)
            
            if plate_type == "basic_europe":
                generate_plate(plate_path="plates/plate.jpg", random=self.random,
                           plate=plate, num_size=(56, 83), num_size_2=None, 
                           num_list=self.num_lists, init_size=(13, 36), # start from left to right
                           char_list=self.char_lists, regions=None, three_digit = three_digit,
                           num_ims=self.num_ims, char_size=(60, 83), region_name=None,
                           char_ims=self.char_ims, label_prefix=plate_type,
                           save_path=self.save_path, region_size=None, all_regions=self.regions_lists_yellow,
                           save_=save, plate_size=(520, 110))

            elif plate_type == "basic_north":
                generate_plate(plate_path="plates/plate.jpg",  random=self.random,
                           plate=plate, num_size=(40, 83), num_size_2=None, 
                           num_list=self.num_lists, init_size=(46, 10),
                           char_list=self.char_lists, regions=None, three_digit = three_digit,
                           num_ims=self.num_ims, char_size=(49, 70),  region_name=None,
                           char_ims=self.char_ims, label_prefix=plate_type,
                           save_path=self.save_path, region_size=None, all_regions=self.regions_lists_yellow,
                           save_=save, plate_size=(355, 155))

            elif plate_type == "commercial_north":

                self.assertion(region_name, self.regions_lists_yellow)

                generate_plate(plate_path="plates/plate_y.jpg",  random=self.random,
                           plate=digits, num_size=(44, 60), num_size_2=(64, 90), 
                           num_list=self.num_lists_yellow, char_list=self.char_lists_yellow,
                           num_ims=self.num_ims_yellow, char_ims=self.char_ims_yellow,
                           init_size=(8, 76), # start from left to right
                           regions=self.regions_yellow, three_digit = three_digit,
                           char_size=(64, 62), region_name=region_name,
                           label_prefix=plate_type, all_regions=self.regions_lists_yellow,
                           save_path=self.save_path, region_size=(88, 60),
                           save_=save, plate_size=(336, 170))


            elif plate_type == "commercial_europe":

                self.assertion(region_name, self.regions_lists_yellow)

                generate_plate(plate_path="plates/plate_y.jpg",  random=self.random,
                           plate=digits, num_size=(56, 83), num_size_2=None, 
                           num_list=self.num_lists_yellow, char_list=self.char_lists_yellow,
                           num_ims=self.num_ims_yellow, char_ims=self.char_ims_yellow,
                           init_size=(13, 36), # start from left to right
                           regions=self.regions_yellow, three_digit = three_digit,
                           char_size=(60, 83), region_name=region_name,
                           label_prefix=plate_type, all_regions=self.regions_lists_yellow,
                           save_path=self.save_path, region_size=(88, 60),
                           save_=save, plate_size=(520, 110))

            elif plate_type == "green_old":
                
                self.assertion(region_name, self.regions_lists_yellow)

                generate_plate(plate_path="plates/plate_g.jpg", 
                           plate=digits, num_size=(44, 60), num_size_2=(64, 90), all_regions=self.regions_lists_yellow,
                           num_list=self.num_lists_green, char_list=self.char_lists_green,
                           num_ims=self.num_ims_green, char_ims=self.char_ims_green,
                           init_size=(8, 76), # start from left to right 
                           regions=self.regions_green, three_digit = three_digit,
                           char_size=(64, 62), region_name=region_name,
                           label_prefix=plate_type,  random=self.random,
                           save_path=self.save_path, region_size=(88, 60),
                           save_=save, plate_size=(336, 170))

            elif plate_type == "green_basic":
                generate_plate(plate_path="plates/plate_g.jpg", 
                           plate=plate, num_size=(60, 65), num_size_2=(80, 90), 
                           num_list=self.num_lists_green, char_list=self.char_lists_green,
                           num_ims=self.num_ims_green, char_ims=self.char_ims_green, region_size=None,
                           init_size=(8, 78),  random=self.random, all_regions=self.regions_lists_yellow,
                           char_size=(60, 65), label_prefix=plate_type, regions=None,
                           save_path=self.save_path, region_name=None, three_digit = False,
                           save_=save, plate_size=(336, 170))
