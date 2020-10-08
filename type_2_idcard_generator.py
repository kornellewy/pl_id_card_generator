import os 
import random
import csv
from PIL import Image,ImageDraw,ImageFont
import datetime
import string

class Type2Generator(object):
    def __init__(self):
        self.front_base_mask_path = os.path.join('data','type2_front.jpg')
        self.back_base_mask_path = os.path.join('data','type2_back.jpg')
        # bbox are bound to images, change if images change
        # [x1, y1, x2, y2]
        self.bbox_front_img_big = [50, 300, 500, 875]
        self.bbox_front_img_big_size = (self.bbox_front_img_big[2]-self.bbox_front_img_big[0],
                                        self.bbox_front_img_big[3]-self.bbox_front_img_big[1])
        self.bbox_front_img_small = [1250, 655, 1430, 870]
        self.bbox_front_img_small_size = (self.bbox_front_img_small[2] - self.bbox_front_img_small[0],
                                        self.bbox_front_img_small[3] - self.bbox_front_img_small[1])
        self.bbox_back_img = [845, 180, 970, 345]
        self.bbox_back_img_size = (self.bbox_back_img[2] - self.bbox_back_img[0],
                                        self.bbox_back_img[3] - self.bbox_back_img[1])
        self.bbox_surname = (593, 310)
        self.bbox_first_name = (593,455)
        self.bbox_family_name = (593, 580)
        self.bbox_parents_names = (593, 715)
        self.bbox_date_of_birth = (593, 850)
        self.bbox_sex = (1070, 850)
        self.bbox_pesel = (205, 60)
        self.bbox_nationality = (205, 150)
        self.bbox_place_of_birth = (40, 225)
        self.bbox_issuing_authority = (40, 300)
        self.bbox_id_card_number = (720, 100)
        self.bbox_date_of_issue = (670, 222)
        self.bbox_expiry_date = (670, 300)

        self.face_dataset_path = 'faces'
        self.face_dataset_images_paths = self._load_images(self.face_dataset_path)

        self.male_name_first_csv_path = os.path.join('first_name', 'lista_imion_męskich_os_żyjące_2020-01-21.csv')
        self.male_name_second_csv_path = os.path.join('second_name', 'lista_drugich_imion_męskich_os._żyjące_2020-01-21.csv')
        self.female_name_first_csv_path = os.path.join('first_name', 'lista_imion_żeńskich_os_żyjące_2020-01-21.csv')
        self.female_name_second_csv_path = os.path.join('second_name', 'lista_drugich_imion_żeńskich_os.żyjące_2020-01-21.csv')

        self.male_names_first = self._load_data_from_csv(self.male_name_first_csv_path)
        self.male_names_second = self._load_data_from_csv(self.male_name_second_csv_path)
        self.female_names_first = self._load_data_from_csv(self.female_name_first_csv_path)
        self.female_names_second = self._load_data_from_csv(self.female_name_second_csv_path)

        self.all_names = self.male_names_first + self.male_names_second + self.female_names_first + self.female_names_second

        self.female_surname_csv_path = os.path.join('surnames', 'Wykaz_nazwisk_żeńskich_uwzgl_os__zmarłe_2020-01-22.csv')
        self.male_surname_csv_path = os.path.join('surnames', 'Wykaz_nazwisk_męskich_uwzgl_os__zmarłe_2020-01-22.csv')
        self.female_surnames = self._load_data_from_csv(self.female_surname_csv_path)
        self.male_surnames = self._load_data_from_csv(self.male_surname_csv_path)

        self.font_path = os.path.join('font', 'Lato-Bold.ttf')
        self.font = ImageFont.truetype(self.font_path, 16)

        # self.issuing_authority_csv_path = os.path.join('issuing_authority', 'places.csv')
        # self.issuing_authority = self._load_data_from_csv(self.issuing_authority_csv_path)

        self.bbox_back_end_code_line1 = (55, 420)
        self.bbox_back_end_code_line2 = (55, 470)
        self.bbox_back_end_code_line3 = (55, 520)

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

    def _generate_single_front_idcard(self):
        base_img = Image.open(self.front_base_mask_path)
        face_img_path = random.choice(self.face_dataset_images_paths)
        face_img = Image.open(face_img_path).convert('LA')
        big_front_face_img = face_img.resize(self.bbox_front_img_big_size)
        small_front_face_img = face_img.resize(self.bbox_front_img_small_size)
        sex_type = random.choice(['M', 'K'])
        first_name = random.choice(self.all_names)
        if random.uniform(0, 1) > 0.5:
            second_name = random.choice(self.all_names)
        else:
            second_name = ' '
        names = first_name + ' ' + second_name
        surname = random.choice(self.male_surnames)
        father_name = random.choice(self.male_names_first)
        mather_name = random.choice(self.female_names_first)
        parents_names = father_name + ' ' + mather_name
        date_of_birth = self._generate_fake_date_if_birth()
        draw = ImageDraw.Draw(base_img)
        self.font = ImageFont.truetype(self.font_path, 50, encoding="unic")
        draw.text(self.bbox_surname, surname, 'black', self.font)
        draw.text(self.bbox_first_name, names, 'black', self.font)
        self.font = ImageFont.truetype(self.font_path, 35, encoding="unic")
        draw.text(self.bbox_family_name, surname, 'black', self.font)
        draw.text(self.bbox_parents_names, parents_names, 'black', self.font)
        draw.text(self.bbox_date_of_birth, date_of_birth, 'black', self.font)
        draw.text(self.bbox_sex, sex_type, 'black', self.font)
        base_img.paste(big_front_face_img, (self.bbox_front_img_big[0], self.bbox_front_img_big[1]))
        base_img.paste(small_front_face_img, (self.bbox_front_img_small[0], self.bbox_front_img_small[1]))
        return base_img

    def _generate_fake_date_if_birth(self):
        start_date = datetime.date(1900, 1, 1)
        end_date = datetime.date(2020, 2, 1)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        random_date = random_date.strftime('%d.%m.%Y')
        return random_date

    def _generate_single_back_idcard(self):
        base_img = Image.open(self.back_base_mask_path)
        face_img_path = random.choice(self.face_dataset_images_paths)
        face_img = Image.open(face_img_path).convert('LA')
        face_img = face_img.resize(self.bbox_back_img_size)
        base_img.paste(face_img, (self.bbox_back_img[0], self.bbox_back_img[1]))
        draw = ImageDraw.Draw(base_img)
        pesel_as_string = self._generate_random_pesel()
        self.font = ImageFont.truetype(self.font_path, 45, encoding="unic")
        draw.text(self.bbox_pesel, pesel_as_string, 'black', self.font)
        self.font = ImageFont.truetype(self.font_path, 25, encoding="unic")
        place = random.choice(self.all_names)
        draw.text(self.bbox_nationality, 'POLSKIE', 'black', self.font)
        draw.text(self.bbox_place_of_birth, place, 'black', self.font)
        name = random.choice(self.all_names)
        name = place + ' ' + name
        draw.text(self.bbox_issuing_authority, name, 'black', self.font)
        idcard_number = self._genetrate_random_idcard_number()
        draw.text(self.bbox_id_card_number, idcard_number, 'gray', self.font)
        date = self._generate_fake_date_if_birth()
        draw.text(self.bbox_date_of_issue, date, 'black', self.font)
        date = self._generate_fake_date_if_birth()
        draw.text(self.bbox_expiry_date, date, 'black', self.font)
        self.font = ImageFont.truetype(self.font_path, 40, encoding="unic")
        back_code1 = self._genetrate_random_back_code()
        draw.text(self.bbox_back_end_code_line1, back_code1, 'black', self.font)
        back_code2 = self._genetrate_random_back_code()
        draw.text(self.bbox_back_end_code_line2, back_code2, 'black', self.font)
        back_code3 = self._genetrate_random_back_code()
        draw.text(self.bbox_back_end_code_line3, back_code3, 'black', self.font)
        return base_img

    def _generate_random_pesel(self):
        year = random.randint(1900, 2099)
        if year <= 1999:
            month = random.randint(1, 12)
        elif year >= 2000:
            month = random.randint(1, 12) + 20  # to distinguish between centuries
        # I need to put months in a category to choose correct range of possible days for each one
        odd_months = (1, 3, 5, 7, 8, 10, 12, 21, 23, 25, 27, 28, 30, 32)
        even_months = (4, 6, 9, 11, 24, 26, 29, 31)
        if month in odd_months:
            day = random.randint(1, 31)

        elif month in even_months:
            day = random.randint(1, 30)
            # this is for february
        else:
            if year % 4 == 0 and year != 1900:
                day = random.randint(1, 29)  # leap year
            else:
                day = random.randint(1, 28)  # usual year
        four_random = random.randint(1000, 9999)
        four_random = str(four_random)
        # here comes the equation part, it calculates the last digit
        y = '%02d' % (year % 100)
        m = '%02d' % month
        dd = '%02d' % day
        a = y[0]
        a = int(a)
        b = y[1]
        b = int(b)
        c = m[0]
        c = int(c)
        d = m[1]
        d = int(d)
        e = dd[0]
        e = int(e)
        f = dd[1]
        f = int(f)
        g = four_random[0]
        g = int(g)
        h = four_random[1]
        h = int(h)
        i = four_random[2]
        i = int(i)
        j = four_random[3]
        j = int(j)
        check = a + 3 * b + 7 * c + 9 * d + e + 3 * f + 7 * g + 9 * h + i + 3 * j
        if check % 10 == 0:
            last_digit = 0
        else:
            last_digit = 10 - (check % 10)
        pesel = str(year % 100) + str(month) + str(day) + str(four_random) + str(last_digit)
        return pesel

    def _genetrate_random_idcard_number(self):
        chars = string.ascii_uppercase
        digits = string.digits
        front = ''.join(random.choice(chars) for _ in range(3))
        back = ''.join(random.choice(digits) for _ in range(6))
        idcard_number = front + '   ' + back
        return idcard_number

    def _genetrate_random_back_code(self, lenght=32):
        chars = string.ascii_uppercase
        code = ''.join(random.choice(chars) for _ in range(lenght))
        return code


if __name__ == "__main__":
    kjn = Type2Generator()
    for i in range(20):
        img = kjn._generate_single_front_idcard()
        img.save('dataset/front_' + str(i) + '.jpg')
        img = kjn._generate_single_back_idcard()
        img.save('dataset/back_'+str(i)+'.jpg')




    # import matplotlib.pyplot as plt
    # import cv2
    # img = cv2.imread('data/type2_back.jpg')
    # plt.figure()
    # plt.imshow(img)
    # plt.show()