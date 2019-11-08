from PIL import Image, ImageDraw
import math, os, random
from math import pi


class Strokes:
    def __init__(self, pngs, data):
        self.dict = data
        size_variations = set([Image.open(png).size for png in pngs])
        if len(size_variations) == 1:
            self.area = {os.path.basename(png): self.black_area(png) for png in pngs}
            self.png_list = [os.path.basename(png) for png in pngs]
            self.img_size = next(iter(size_variations))
        self.methods = {"lines": lambda png: self.lines(png), "circles": lambda png: self.circles(png), "dots": lambda png: self.dots(png)}


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
                # randomization of features if it's specified in the specs dictionary:
                if specs["random"] == "all" or "size" in specs["random"]:
                    if specs["size"] > 0 : length = random.randint(1, math.ceil(specs["size"] * 3))
                    else: length = random.randint(1, 20)
                else: length = specs["size"]  # length of the line as specified for the png name in json file
                if specs["random"] == "all" or "angle" in specs["random"]:
                    if specs["angle"] == 0: slope = (random.randint(-50, 50), random.randint(-50, 50)) # total randomization if the angle is 0.
                    else: slope = (random.randint(0, math.ceil(length * angle_cos * 3)), random.randint(0, math.ceil(length * angle_sin * 3))) # relative randomization if the angle is other than 0.
                else: slope = length * angle_cos, length * angle_sin
                if specs["random"] == "all" or "position" in specs["random"]:
                    if specs["density"] > 0 : density = random.randint(0, math.ceil(specs["density"] * 3))
                    else: density = random.randint(0, 10)
                else: density = specs["density"]
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
                if specs["random"] == "all" or "size" in specs["random"]:
                    if specs["size"] > 0: diameter = random.uniform(1, specs["size"] * 6)
                    else: diameter = random.uniform(1, 50)
                else: diameter = specs["size"]
                if specs["random"] == "all" or "position" in specs["random"]:
                    if specs["density"] > 0: density = random.randint(0, math.ceil(specs["density"] * 3))
                    else: density = random.randint(0, 10)
                else: density = specs["density"]
                radius = diameter / 2
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
                if specs["random"] == "all" or "size" in specs["random"]:
                    if specs["size"] > 0: length = random.randint(1, math.ceil(specs["size"] * 3))
                    else: length = random.uniform(0.5, 3)
                else: length = specs["size"]
                if specs["random"] == "all" or "position" in specs["random"]:
                    if specs["density"] > 0: density = random.randint(0, math.ceil(specs["density"] * 3))
                    else: density = random.randint(0, 10)
                else: density = specs["density"]
                x2, y2 = (x1 + length), (y1 + length)  # end point
                if (round(x1), round(y1)) and (round(x2), round(y2)) in self.area[png]:
                    coordinate_list.append([(x1, y1), (x2, y2)])
                else: pass
                x1 += density
            y1 += density
        return coordinate_list, specs["color"]


    def all_points(self):
        images_matching_data = list(set(self.png_list).intersection(self.dict))
        if len(images_matching_data) > 0:
            all_points = []
            for png in images_matching_data:
                if self.dict[png]["pattern"] in self.methods:
                    list_of_coordinates, color = self.methods[self.dict[png]["pattern"]](png)
                    all_points.append((list_of_coordinates, color))
        return all_points


    def coordinate_file(self, name, coord_lst):  # writing all stroke coordinates in a ped file:
        with open(name, "w") as ped_file:
            ped_file.write("Stroke CoordinateSystem Origin (0, 0, 0) Max (640, 400, 1)" + "\n")
            ped_file.write("Tool Get davinci_college_12")
            for coordinates, color in coord_lst:
                ped_file.write("\n \n")
                ped_file.write("Color Get " + color.capitalize() + "\n \n")
                for each_stroke in coordinates:
                    for points in each_stroke:
                        ped_file.write(str(points) + " ")
                    ped_file.write("\n")


    def draw_all(self, coord_lst):  # drawing the resulting image depending on the given data in a created instance.
        img = Image.new('RGB', self.img_size, color='white')
        img_draw = ImageDraw.Draw(img) 
        for coordinates, color in coord_lst:
            for points_list in coordinates:
                if len(points_list) == 2:
                    img_draw.line((points_list[0], points_list[1]), fill=color)
                elif len(points_list) > 2:
                    for index in range(len(points_list)):
                        img_draw.line((points_list[index], points_list[index-1]), fill=color)
        img.show()
