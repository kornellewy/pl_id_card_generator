import os 
import random
import csv

class Type2Generator(object):
    def __init__(self):
        self.front_base_mask_path = os.path.join('data','type2_back.jpg')
        self.back_base_mask_path = os.path.join('data','type2_front.jpg')
        # bbox are bound to images, change if images change
        # [x1, y1, x2, y2]
        self.bbox_front_img_big = [100, 300, 550, 875]
        self.bbox_front_img_small = [1250, 655, 1430, 870]
        self.bbox_surname = [590, 320]
        self.bbox_first_name = [590,465]
        self.bbox_family_name = [590, 600]
        self.bbox_parents_names = [590, 740]
        self.bbox_date_of_birth = [590, 860]
        self.bbox_sex = [1070, 860]
        self.bbox_pesel = [195, 66]
        self.bbox_nationality = [195, 135]
        self.bbox_place_of_birth = [35, 210]
        self.bbox_issuing_authority = [35, 285]
        self.bbox_id_card_number = [675, 85]
        self.bbox_date_of_issue = [635, 215]
        self.bbox_expiry_date = [635, 290]

        self.face_dataset_path = 'faces'
        self.face_dataset_images_paths = self._load_images(self.face_dataset_path)

        self.male_name_first_csv_path = os.path.join('first_name', 'lista_imion_męskich_os_żyjące_2020-01-21.csv')
        self.male_name_second_csv_path = os.path.join('second_name', 'lista_drugich_imion_męskich_os._żyjące_2020-01-21.csv')
        self.female_name_first_csv_path = os.path.join('first_name', 'lista_imion_żeńskich_os_żyjące_2020-01-21.csv')
        self.female_name_second_csv_path = os.path.join('second_name', 'lista_drugich_imion_żeńskich_os.żyjące_2020-01-21.csv')

        self.male_name_first = self._load_data_from_csv(self.male_name_first_csv_path)
        self.male_name_second = self._load_data_from_csv(self.male_name_second_csv_path)
        self.female_name_first = self._load_data_from_csv(self.female_name_first_csv_path)
        self.female_name_second_csv_path = self._load_data_from_csv(self.female_name_second_csv_path)

        self.font_path = os.path.join('font', 'Lato-Regular.ttf')

    def _load_images(self, path, name_format = "path"):
        # name_format - controla if u output full path to img or jast its name
        images = []
        valid_images = [".jpg", ".png", ".jpeg"]
        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            # full path
            if name_format == "path":
                images.append(os.path.join(path, f))
            # jast its name
            elif name_format == "name":
                images.append(f)
            else:
                raise ValueError("wrong format for parameter : name_format")
        return images

    def _load_csv_paths(self, path):
        csv_files = []
        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in ['.csv']:
                continue
            # full path
            if name_format == "path":
                images.append(os.path.join(path, f))
            # jast its name
            elif name_format == "name":
                images.append(f)
            else:
                raise ValueError("wrong format for parameter : name_format")
        return images

    def _load_data_from_csv(self, csv_path):
        data_in_list = []
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                data_in_list.append(row[0])
        return data_in_list



if __name__ == "__main__":
    kjn = Type2Generator()
    
    # import matplotlib.pyplot as plt
    # import cv2 
    # img = cv2.imread('data/type2_back.jpg')
    # plt.figure()
    # plt.imshow(img) 
    # plt.show() 