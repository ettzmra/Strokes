from PIL import Image, ImageDraw
import json, math


def compatible_pngs(*pngs):  # any number of png files can be written as arguments which shall be gathered in a tuple)
    for indx in range(len(pngs) - 1):
        png, next_png = pngs[indx], pngs[indx + 1]
        try:
            img1 = Image.open(png)
            img2 = Image.open(next_png)
        except IOError:
            print("couldn't open the file, write arguments and their extensions inside quotes")
        if img1.size != img2.size: raise ValueError("different png sizes")
        else: return True


def black_area(png):
    img = Image.open(png)
    pix = img.load()  # gives pixel color
    black_pxls = []
    for x in range(img.size[0]):  # looping through all coordinates
        for y in range(img.size[1]):
            if pix[x, y] == (0, 0, 0, 255):  # if a pixel is black, its coordinate is saved to the black_pxls list.
                black_pxls.append((x, y))
    return black_pxls


class Pattern:
    def __init__(self, json_data, png):
        with open(json_data, "r") as db:
            self.__dict__ = json.load(db)  # loading json file as the class dictionary
        self.png = png
        self.area = black_area(png)

    def draw_lines(self):
        img = Image.open(self.png)
        draw = ImageDraw.Draw(img)
        specs = self.__dict__[self.png]   #this is the dictionary of specifications belonging to the png name.
        for start_point in self.area:  # looping all coordinate points in black area of the png
            x1, y1 = start_point
            length = specs["size"]  # length of the line as specified for the png name in json file
            ang = specs["angle"]
            end_point = (x1 + length * math.cos(ang), y1 + length * math.sin(ang))
            if end_point in self.area:
                draw.line([start_point, end_point], fill=specs["color"], width=specs["density"])




