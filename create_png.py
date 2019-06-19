from PIL import Image, ImageDraw
import json, random
import math


def compatible_files(png_array):
    for indx in range(len(png_array) - 1):
        try:
            im = Image.open(png_array[indx])
            next_im = Image.open(png_array[indx + 1])
            if im.size != next_im.size:
                raise ValueError("different png sizes")
        except IOError:
            print("couldn't open the file, write arguments and their extensions inside quotes")
        else: return png_array, im.size


def black_area(png_file):
    im = Image.open(png_file)
    pix = im.load()  # gives pixel color
    black_pxls = []
    for y in range(im.size[1]):  # looping through all coordinates
        for x in range(im.size[0]):
            if pix[x, y] == (0, 0, 0):  # if a pixel is black, its coordinate is saved to the black_pxls list.
                black_pxls.append((x, y))
    return black_pxls


class Pattern:
    def __init__(self, json_data, result_img, *pngs):  # any number of png files can be written as arguments,
        with open(json_data, "r") as db:   # which shall be gathered in a tuple
            data = json.load(db)  # loading json file as the class dictionary
        self.dict = data
        self.pngs = compatible_files(pngs)[0]  # takes a tuple of pngs as argument
        self.draw = {}
        self.area = {}
        for png in self.pngs:
            self.area[png] = black_area(png)
        Image.new('RGB', (compatible_files(pngs)[1]), color='white').save(result_img)
        self.result_img = result_img
        self.img = Image.open(result_img)
        self.img_draw = ImageDraw.Draw(self.img)

    def draw_lines(self, png):
        specs = self.dict[png]   # this is the dictionary of specifications given for the png in json file.
        coordinate_list = []
        # formulating the slope:
        angle_cos = round(math.cos(math.radians(specs["angle"])), 2)
        angle_sin = round(math.sin(math.radians(specs["angle"])), 2)
        # looping certain coordinate points in black area of the png in accordance with the density given:
        y1 = self.area[png][0][1]  # y coordinate of start_point
        while y1 <= max([point[1] for point in self.area[png]]):  # loops till the highest y coord. is processed.
            x1 = min([point[0] for point in self.area[png]])  # x coordinate of start_point
            while x1 <= max([point[0] for point in self.area[png]]):  # loops till the highest y coord. is processed.
                length = specs["size"]  # length of the line as specified for the png name in json file
                slope = length * angle_cos, length * angle_sin
                density = specs["density"]
                # randomization of features if it's specified in the specs dictionary:
                if specs["random"] == "all":
                    length = random.randint(0, math.ceil(specs["size"] * 3))
                    if specs["angle"] == 0:  # total randomization if the angle is 0.
                        slope = (random.randint(-50, 50), random.randint(-50, 50))
                    else:   # relative randomization if the angle is other than 0.
                        slope = (random.randint(0, math.ceil(length * angle_cos * 3)),
                                 random.randint(0, math.ceil(length * angle_sin * 3))
                                 )
                    density = random.randint(0, math.ceil(specs["density"] * 3))
                if "position" in specs["random"]:
                    density = random.randint(0, math.ceil(specs["density"] * 3))
                if "size" in specs["random"]:
                    length = random.randint(0, math.ceil(specs["size"] * 3))
                if "angle" in specs["random"]:
                    if specs["angle"] == 0:
                        slope = (random.randint(-50, 50), random.randint(-50, 50))
                    else:
                        slope = (random.randint(0, math.ceil(length * angle_cos * 3)),
                                 random.randint(0, math.ceil(length * angle_sin * 3))
                                 )
                x2, y2 = (x1 + slope[0]), (y1 + slope[1])  # end point coordinates of one line
                if (round(x1), round(y1)) and (round(x2), round(y2)) in self.area[png]:
                    coordinate_list.append((x1, y1))  # adds start point of one instance, e.g. one line, of the pattern.
                    coordinate_list.append((x2, y2))  # adds end point coordinates of each instance of the pattern.
                    self.img_draw.line([(x1, y1), (x2, y2)], fill=specs["color"])
                    self.img.save(self.result_img)
                else: pass
                x1 += density  # x coord of start point of each line based on density, whether randomized or not.
            y1 += density   # y coord of start point of each line based on density, whether randomized or not.
        return coordinate_list, specs["color"]

    def draw_circles(self, png):
        specs = self.dict[png]
        coordinate_list = []
        y1 = self.area[png][0][1]  # y coordinate of start_point
        while y1 <= max([point[1] for point in self.area[png]]):
            x1 = min([point[0] for point in self.area[png]])  # x coordinate of start_point
            while x1 <= max([point[0] for point in self.area[png]]):
                diameter = specs["size"] * 2
                density = specs["density"]
                if specs["random"] == "all":
                    diameter = random.uniform(0, specs["size"] * 6)
                    density = random.randint(0, math.ceil(specs["density"] * 3))
                if "position" in specs["random"]:
                    density = random.randint(0, math.ceil(specs["density"] * 3))
                if "size" in specs["random"]:
                    diameter = random.uniform(0, specs["size"] * 6)
                x2, y2 = (x1 + diameter), (y1 + diameter)
                if (round(x1), round(y1)) and (round(x2), round(y2)) in self.area[png]:
                    coordinate_list.append((x1, y1))
                    coordinate_list.append((x2, y2))
                    self.img_draw.ellipse((x1, y1, x2, y2), outline=specs["color"])
                    self.img.save(self.result_img)
                else: pass
                x1 += (diameter + density)
            y1 += (diameter + density)
        return coordinate_list, specs["color"]

    def draw_dots(self, png):
        specs = self.dict[png]
        coordinate_list = []
        # looping certain coordinate points in black area of the png in accordance with the density given:
        y1 = self.area[png][0][1]  # y coordinate of start_point
        while y1 <= max([point[1] for point in self.area[png]]):
            x1 = min([point[0] for point in self.area[png]])  # x coordinate of start_point
            while x1 <= max([point[0] for point in self.area[png]]):
                length = specs["size"]
                density = specs["density"]
                if specs["random"] == "all":
                    length = random.randint(0, math.ceil(specs["size"] * 3))
                    density = random.randint(0, math.ceil(specs["density"] * 3))
                if "position" in specs["random"]:
                    density = random.randint(0, math.ceil(specs["density"] * 3))
                if "size" in specs["random"]:
                    length = random.randint(0, math.ceil(specs["size"] * 3))
                x2, y2 = (x1 + length), (y1 + length)  # end point
                if (round(x1), round(y1)) and (round(x2), round(y2)) in self.area[png]:
                    coordinate_list.append((x1, y1))
                    coordinate_list.append((x2, y2))
                    self.img_draw.line([(x1, y1), (x2, y2)], fill=specs["color"])
                    self.img.save(self.result_img)
                else: pass
                x1 += density
            y1 += density
        return coordinate_list, specs["color"]

    def draw_all(self, result_ped):  # drawing all patterns at once and writing all pattern coordinates as command:
        with open(result_ped, "a+") as ped_file:
            ped_file.write("Stroke CoordinateSystem Origin (0, 0, 0) Max (640, 480, 1)")
            for png in self.pngs:
                ped_file.write("\n \n")
                if self.dict[png]["pattern"] == "lines":
                    coordinates, color = self.draw_lines(png)
                if self.dict[png]["pattern"] == "circles":
                    coordinates, color = self.draw_circles(png)
                if self.dict[png]["pattern"] == "dots":
                    coordinates, color = self.draw_dots(png)
                ped_file.write("Color Get " + color + "\n \n")
                for i in range(0, len(coordinates) - 1, 2):
                    ped_file.write(str(coordinates[i]) + str(coordinates[i+1]) + "\n")


img = Pattern("patterns.json", "python_result.png", "1.png", "2.png", "3.png", "4.png")
# img.draw_lines("1.png")
# img.draw_lines("2.png")
# img.draw_circles("3.png")
# img.draw_dots("4.png")
img.draw_all("python_result.ped")
