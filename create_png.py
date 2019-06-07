from PIL import Image, ImageDraw
import json
import math


def compatible_pngs(*pngs):  # any number of png files can be written as arguments which shall be gathered in a tuple)
    for indx in range(len(pngs) - 1):
        # png, next_png = pngs[indx], pngs[indx + 1]
        try:
            img = Image.open(pngs[indx])
            next_img = Image.open(pngs[indx + 1])
            if img.size != next_img.size:
                raise ValueError("different png sizes")
            else:
                return True
        except IOError:
            print("couldn't open the file, write arguments and their extensions inside quotes")


def black_area(png_file):
    im = Image.open(png_file)
    pix = im.load()  # gives pixel color
    black_pxls = []
    for x in range(im.size[0]):  # looping through all coordinates
        for y in range(im.size[1]):
            if pix[x, y] == (0, 0, 0):  # if a pixel is black, its coordinate is saved to the black_pxls list.
                black_pxls.append((x, y))
    return black_pxls


class Pattern:
    def __init__(self, json_data, png):
        with open(json_data, "r") as db:
            data = json.load(db)  # loading json file as the class dictionary
        self.dict = data
        self.name = png
        self.img = Image.open(png)
        self.area = black_area(png)

    def draw_lines(self):
        draw = ImageDraw.Draw(self.img)
        specs = self.dict[self.name]   # this is the dictionary of specifications belonging to the png name.
        length = specs["size"]  # length of the line as specified for the png name in json file
        line_color = specs["color"]
        angle_cos = round(math.cos(math.radians(specs["angle"])), 2)
        angle_sin = round(math.sin(math.radians(specs["angle"])), 2)
        # looping all coordinate points in black area of the png:
        y1 = self.area[0][1]  # y coordinate of startpoint
        while y1 in [point[1] for point in self.area]:
            x1 = self.area[0][0]  # x coordinate of start_point
            while x1 <= self.area[-1][0]:
                end_point = (int(x1 + length * angle_cos), int(y1 + length * angle_sin))
                print(end_point)
                if end_point in self.area:
                    draw.line([(x1, y1), end_point], fill=line_color, width=specs["density"])
                    self.img.save(self.name)
                    x1 += 40
                else: x1 += 1
            y1 = int(y1 + (length * angle_sin * 3))



print(compatible_pngs("1.png", "2.png", "3.png"))
img_2 = Pattern("patterns.json", "2.png")
img_2.draw_lines()