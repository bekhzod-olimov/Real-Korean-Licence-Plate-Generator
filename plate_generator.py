from utils import *

class PlateGenerator:
    
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

    def Generation(self, plate, save, plate_type, region_name=None):
        
        assert plate_type in ["short", "long", "yellow", "old", "green"], "Please choose the correct the plate type"
        
        if plate_type == "long":
            generate_plate(plate_path="plate.jpg", 
                       plate=plate, num_size=(56, 83), num_size_2=None, 
                       num_list=self.number_list, init_size=(13, 36), # start from left to right
                       char_list=self.char_list, regions=None, three_digit = None,
                       num_ims=self.Number, char_size=(60, 83), region_name=None,
                       char_ims=self.Char1, label_prefix=plate_type,
                       save_path=self.save_path, region_size=None,
                       save_=save, plate_size=(520, 110))
        
        elif plate_type == "short":
            generate_plate(plate_path="plate.jpg", 
                       plate=plate, num_size=(40, 83), num_size_2=None, 
                       num_list=self.number_list, init_size=(46, 10),
                       char_list=self.char_list, regions=None, three_digit = None,
                       num_ims=self.Number, char_size=(49, 70),  region_name=None,
                       char_ims=self.Char1, label_prefix=plate_type,
                       save_path=self.save_path, region_size=None,
                       save_=save, plate_size=(355, 155))
        
            
        elif plate_type == "yellow":
            assert region_name != None, "Please insert a region name"
            assert region_name in [os.path.basename(region) for region in self.region_list_y], f"Please choose one of these regions: {[os.path.basename(region) for region in self.region_list_y]}"
            generate_plate(plate_path="plate_y.jpg", 
                       plate=plate, num_size=(44, 60), num_size_2=(64, 90), 
                       num_list=self.number_list_y, char_list=self.char_list_y,
                       num_ims=self.Number_y, char_ims=self.Char1_y,
                       init_size=(8, 76), # start from left to right
                       regions=self.Region_y, three_digit = None,
                       char_size=(64, 62), region_name=region_name,
                       label_prefix=plate_type,
                       save_path=self.save_path, region_size=(88, 60),
                       save_=save, plate_size=(336, 170))
            
        elif plate_type == "old":
            assert region_name != None, "Please insert a region name"
            generate_plate(plate_path="plate_g.jpg", 
                       plate=plate, num_size=(44, 60), num_size_2=(64, 90), 
                       num_list=self.number_list_g, char_list=self.char_list_g,
                       num_ims=self.Number_g, char_ims=self.Char1_g,
                       init_size=(8, 76), # start from left to right
                       regions=self.Region_g, three_digit = None,
                       char_size=(64, 62), region_name=region_name,
                       label_prefix=plate_type,
                       save_path=self.save_path, region_size=(88, 60),
                       save_=save, plate_size=(336, 170))
            
        elif plate_type == "green":
            generate_plate(plate_path="plate_g.jpg", 
                       plate=plate, num_size=(60, 65), num_size_2=(80, 90), 
                       num_list=self.number_list_g, char_list=self.char_list_g,
                       num_ims=self.Number_g, char_ims=self.Char1_g, region_size=None,
                       init_size=(8, 78), # start from left to right
                       char_size=(60, 65), label_prefix=plate_type, regions=None,
                       save_path=self.save_path, region_name=None, three_digit = None,
                       save_=save, plate_size=(336, 170))
