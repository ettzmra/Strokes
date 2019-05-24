from PIL import Image, ImageDraw
import json
# import math


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
        self.area = black_area(png)

    def draw_lines(self, sec_img):
        img = Image.open(self.name)
        draw = ImageDraw.Draw(img)
        specs = self.dict[self.name]   # this is the dictionary of specifications belonging to the png name.
        for start_point in self.area:  # looping all coordinate points in black area of the png
            x1, y1 = start_point
            length = specs["size"]  # length of the line as specified for the png name in json file
            # ang = specs["angle"]
            end_point = ((x1 + length), (y1 + length))
            if end_point in self.area:
                draw.line([start_point, end_point], fill=specs["color"], width=specs["density"])
                img.save(sec_img)


# print(compatible_pngs("1.png", "2.png", "3.png"))
img_2 = Pattern("patterns.json", "2.png")
print(img_2.dict)
print(img_2.area)
img_2.draw_lines("22.png")
