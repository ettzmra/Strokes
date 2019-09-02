from PIL import Image, ImageDraw
import json, random
import math
from math import pi


class Pattern:
    def __init__(self, json_data, result_img, *pngs):  # any number of png files can be written as arguments which shall be gathered in a tuple
        with open(json_data, "r") as db:
            data = json.load(db)  # loading json file as the class dictionary
        self.dict = data
        self.pngs = self.all_same_size(pngs)[0]  # returns all given pngs if they are fully compatible
        self.area = {}
        for png in self.pngs:
            self.area[png] = self.black_area(png)
        Image.new('RGB', (self.all_same_size(pngs)[1]), color='white').save(result_img)
        self.result_img = result_img
        self.img = Image.open(result_img)
        self.img_draw = ImageDraw.Draw(self.img)
        self.methods = {"lines": lambda png: self.lines(png), "circles": lambda png: self.circles(png), "dots": lambda png: self.dots(png)}

    def all_same_size(self, png_array):
        for indx in range(len(png_array) - 1):
            try:
                im = Image.open(png_array[indx])
                next_im = Image.open(png_array[indx + 1])
                if im.size != next_im.size:
                    raise ValueError("different png sizes")
            except IOError:
                print("couldn't open the file, write arguments and their extensions inside quotes")
            else:
                return png_array, im.size

    def black_area(self, png_file):
        im = Image.open(png_file)
        pix = im.load()  # gives pixel color
        black_pxls = []
        for y in range(im.size[1]):  # looping through all coordinates
            for x in range(im.size[0]):
                if pix[x, y] == (0, 0, 0):  # if a pixel is black, its coordinate is saved to the black_pxls list.
                    black_pxls.append((x, y))
        return black_pxls


    def lines(self, png):
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
                        slope = (random.randint(0, math.ceil(length * angle_cos * 3)), random.randint(0, math.ceil(length * angle_sin * 3)))
                    density = random.randint(0, math.ceil(specs["density"] * 3))
                if "position" in specs["random"]:
                    density = random.randint(0, math.ceil(specs["density"] * 3))
                if "size" in specs["random"]:
                    length = random.randint(0, math.ceil(specs["size"] * 3))
                if "angle" in specs["random"]:
                    if specs["angle"] == 0:
                        slope = (random.randint(-50, 50), random.randint(-50, 50))
                    else:
                        slope = (random.randint(0, math.ceil(length * angle_cos * 3)), random.randint(0, math.ceil(length * angle_sin * 3)))
                x2, y2 = (x1 + slope[0]), (y1 + slope[1])  # end point coordinates of one line
                if (round(x1), round(y1)) and (round(x2), round(y2)) in self.area[png]:
                    coordinate_list.append([(x1, y1), (x2, y2)])  # adds start and end points of one stroke, e.g. one line of the pattern.
                else: pass
                x1 += density  # x coord of start point of each line based on density, whether randomized or not.
            y1 += density   # y coord of start point of each line based on density, whether randomized or not.
        return coordinate_list, specs["color"]

    def circles(self, png):
        specs = self.dict[png]
        coordinate_list = []
        y1 = self.area[png][0][1]  # y coordinate of start_point
        while y1 <= max([point[1] for point in self.area[png]]):
            x1 = min([point[0] for point in self.area[png]])  # x coordinate of start_point
            while x1 <= max([point[0] for point in self.area[png]]):
                diameter = specs["size"]
                radius = diameter / 2
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
                    circle_center = (x1 + x2) / 2, (y1 + y2) / 2
                    multiple_points_of_a_circle = [(round(circle_center[0]+(math.cos(2 * pi / diameter * x) * radius)), round(circle_center[1] + (math.sin(2 * pi / diameter * x) * radius))) for x in range(0, round(diameter) + 1)]
                    coordinate_list.append(multiple_points_of_a_circle)
                else: pass
                x1 += (diameter + density)
            y1 += (diameter + density)
        return coordinate_list, specs["color"]

    def dots(self, png):
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
                    coordinate_list.append([(x1, y1), (x2, y2)])
                    # self.img_draw.line([(x1, y1), (x2, y2)], fill=specs["color"])
                    # self.img.save(self.result_img)
                else: pass
                x1 += density
            y1 += density
        return coordinate_list, specs["color"]

    def all_points(self, result_ped):  # drawing all patterns at once and writing all pattern coordinates as command:
        with open(result_ped, "a+") as ped_file:
            ped_file.write("Stroke CoordinateSystem Origin (0, 0, 0) Max (640, 480, 1)")
            for png in self.pngs:
                ped_file.write("\n \n")
                if self.dict[png]["pattern"] in self.methods:
                    list_of_coordinates, color = self.methods[self.dict[png]["pattern"]](png)
                    ped_file.write("Color Get " + color.capitalize() + "\n \n")
                    for each_stroke in list_of_coordinates:
                        for points in each_stroke:
                            ped_file.write(str(points) + " ")
                        ped_file.write("\n")

    def draw_all(self):
        for png in self.pngs:
            if self.dict[png]["pattern"] in self.methods:
                list_of_coordinates, color = self.methods[self.dict[png]["pattern"]](png)
                for points_list in list_of_coordinates:
                    if len(points_list) == 2:
                        self.img_draw.line((points_list[0], points_list[1]), fill=color)
                        self.img.save(self.result_img)
                    elif len(points_list) > 2:
                        for index in range(len(points_list)):
                            self.img_draw.line((points_list[index], points_list[index-1]), fill=color)
                            self.img.save(self.result_img)

#
# img = Pattern("patterns.json", "python_result_1.png", "1.png", "2.png", "3.png", "4.png")
# img.all_points("python_result_1.ped")
# img.draw_all()