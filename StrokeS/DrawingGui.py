import sys, os, json, shutil
from PyQt5.QtWidgets import QWidget, QComboBox, qApp, QLineEdit, QFileDialog, QToolTip, QHBoxLayout, QGridLayout, QLabel, QTextEdit, QPushButton, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from StrokeS import Drawing


class Specs(QWidget):   # contents of the pop-up configuration window for customization of each image's stroke data(specs and values) without using a json file
    def __init__(self, spec, lst=None):
        super().__init__()
        self.spec = spec
        self.lbl = QLabel(self.spec)
        self.lbl.setFixedSize(65, 20)
        self.lst = lst
        if lst is None:
            self.editor = QLineEdit()  # One-line box to enter size, density and angle values in digits
            self.editor.setToolTip("Enter a number")
            self.editor.textChanged[str].connect(self.given_text)  # When a digit is entered, it gets saved as stroke data for relevant specification, e.g. size : 4.
        else:
            self.editor = QComboBox()  # Drop-down list to choose values for such specs as random, pattern and color.
            self.editor.addItems(lst)
            self.editor.activated[str].connect(self.given_text)  # When a value is picked from a drop-down list, it gets saved as stroke data for relevant specification title, e.g. random : "all".


    def given_text(self, text):  # This function saves the above mentioned values given by the user as input.
        if self.lst is None:
            try: num = int(text)
            except:
                if hasattr(self, 'input'): del self.input  # deletes the previous input when it's deleted or replaced by the user on the line edit box.
            else:
                if num > 0: self.input = num
        else:
            if text in self.lst[1:]: self.input = text



class NewData(QWidget):  # Pop-up window for the user to enter new values to be assembled as stroke data in a dictionary
    def __init__(self, image, data):
        super().__init__()
        self.img = os.path.basename(image)
        self.spec_dict = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.img)
# Layout of the pop-up window:
        grid = QGridLayout()
        hbox1 = QHBoxLayout()
        self.save_btn = QPushButton("Save Data")
        self.preview_btn = QPushButton("Preview")
        self.coord_btn = QPushButton("Save Coordinates")
        self.remove_btn = QPushButton('Remove', self)
        self.spec_list = [ Specs("pattern", ["Choose", "lines","circles","dots"]),
                           Specs("random", ["Choose", "false", "all", "size", "position", "angle", "size, positions", "size, angle", "position, angle"]),
                           Specs("color", ["Choose", "black", "white", "blue", "green", "red", "yellow", "brown", "gray", "orange", "pink", "purple", "dark blue"]),
                           Specs("size"), Specs("density"), Specs("angle") ]
        positions = [(i,j) for i in [0, 2] for j in range(3)]
        for pos, spec in zip(positions, self.spec_list):
            grid.addWidget(spec.lbl, *pos)
            grid.addWidget(spec.editor, pos[0]+1, pos[1])
        hbox1.addWidget(self.preview_btn)
        hbox1.addWidget(self.remove_btn)
        grid.addWidget(self.coord_btn, 4, 0)
        grid.addWidget(self.save_btn, 4, 1)
        grid.addLayout(hbox1, 4, 2)
        self.setLayout(grid)

# Function(s) to be called when the buttons are clicked:
        self.coord_btn.clicked.connect(self.save_data_and_preview)
        self.save_btn.clicked.connect(self.save_data_and_preview)
        self.preview_btn.clicked.connect(self.save_data_and_preview)


    def save_data_and_preview(self): # this function may be called by any of the three buttons above.
        sender = self.sender()  # yields which button gets clicked.
        chosen_specs = {self.img: {}}  # contains values entered by the user together with their corresponding spec title.
        random = self.spec_list[1]
        for each in self.spec_list:
            if hasattr(each, 'input'): chosen_specs[self.img][each.spec] = each.input  # if there is an input for the respective spec title, it gets contained temporarily by chosen_specs.
            elif hasattr(random, 'input'):  # if the user provides no input for a spec, the value is determined automatically depending on the value of spec "random":
                if random.input == "all": random_specs = ["size","position", "angle"]
                else: random_specs = random.input.split(",")
                if each.spec in random_specs:
                    if each.spec == "position": chosen_specs[self.img]["density"] = 0
                    else: chosen_specs[self.img][each.spec] = 0
            if not hasattr(each, 'input') and each.spec not in chosen_specs[self.img]:  # In case of no value input/selection or randomization on a particular spec, the user is urged to enter a number or select from the list.
                QMessageBox.information(self, "Warning", "Please make selection", QMessageBox.Ok)
                break
        if len(chosen_specs[self.img]) == 6: # When all necessary data is given, button clicks yield results.
            if sender == self.save_btn: self.spec_dict.update(chosen_specs)  # if the button clicked is save button, the main data dictionary gets updated by the values in chosen_specs.
            else:
                image = Drawing.Strokes([self.img_full_path], chosen_specs)
                if sender == self.preview_btn: image.draw_all()  # when preview button is clicked, an image is drawn according to the data in chosen_specs and shown by a pop-up window.
                else: image.all_points(self.img + ".ped")  # when coordinate button is clicked, a ped file containing the stroke coordinates of an image according to the data in chosen_specs

class MainApp(QWidget):  # Main application and window
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
    # Widgets on the main window -buttons and text edit box :
        json_btn = QPushButton('Load Json File', self)
        png_btn = QPushButton('Choose Images', self)
        change_btn = QPushButton('Apply Changes', self)  # used to save a present json file after the user alters the contents of it by editing the text on self.textbox.
        clear_btn = QPushButton('Restart', self)  # clears the window, resets all data.
        self.draw_button = QPushButton('Drawing Preview', self)
        self.coordinate_button = QPushButton('Get Coordinates', self)
        self.textbox = QTextEdit()  # shows the contents of a loaded json file, enabling alterations in the file.
        self.textbox.setFixedSize(350, 450)

    # Layout of the main window:
        hbox = QHBoxLayout()
        hbox.addWidget(self.coordinate_button)
        hbox.addWidget(clear_btn)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        grid_layout.addWidget(json_btn, 1, 0)
        grid_layout.addWidget(png_btn, 1, 1)
        grid_layout.addWidget(self.textbox, 2, 0)
        grid_layout.addWidget(change_btn, 3, 0)
        grid_layout.addWidget(self.draw_button, 4, 0)
        grid_layout.addLayout(hbox, 4, 1)
        self.setLayout(grid_layout)

    # Buttons and their connected functions:
        self.posx, self.posy = 390, 70  # used to position image buttons to be created when the user opens images by clicking png_btn.
        self.data = {}  # reserves updated/final stroke data (specs and values) given by the user by loading a json or configuring chosen images one by one.
        self.images = []  # saves images chosen by the user to draw on.
        png_btn.clicked.connect(self.png_inputs)
        json_btn.clicked.connect(self.existing_json)
        self.draw_button.clicked.connect(self.draw_patterns_and_get_coordinates)
        self.coordinate_button.clicked.connect(self.draw_patterns_and_get_coordinates)
        change_btn.clicked.connect(self.change_json)
        clear_btn.clicked.connect(self.clear_all)

        self.setGeometry(300, 300, 800, 600)  # The first two parameters are the x and y positions of the window. The third is the width and the fourth is the height of the window.
        self.setFixedSize(800, 600)
        self.setWindowTitle('Images & Coordinates')
        self.show()


    def existing_json(self):  # opens a json file selected by the user and shows its contents on the sef.textbox.
        file = QFileDialog.getOpenFileName(self, 'Open file', "","Json Files (*.json)", '/home')[0]
        try:
            with open(file, "r") as f:
                content = f.read()
                self.textbox.setText(content)
        except: pass
        else:
            try: self.data.update(json.loads(content))
            except: QMessageBox.information(self, "JSON Error", "Please fix the errors in your file", QMessageBox.Ok)


    def change_json(self):  # enables an already opened json file to be changed using the self.textbox as well as self.data to be updated by the altered content.
        text = self.textbox.toPlainText()
        try: self.data.update(json.loads(text))
        except: QMessageBox.information(self, "JSON Error", "Please provide proper data", QMessageBox.Ok)


    def new_data(self, lst):  # pop-up window for entering new stroke data for an image.
        self.popup = NewData(lst[0], self.data)  # lst[0] is the full path to the image in question.
        self.popup.setGeometry(400, 400, 400, 300)
        self.popup.show()
        helper_func = lambda i: (lambda: self.remove_image(i))  # lambda function to enable button click connection to functions requiring argument(s).
        self.popup.remove_btn.clicked.connect(helper_func(lst))  # removes the already opened image.
        self.popup.remove_btn.clicked.connect(self.popup.close)  # remove button also closes the pop-up window for that particular image.


    def remove_image(self, lst):  #connected to the remove button above.
        lst[1].hide()  # lst[1] refers to the image button. This method removes the image button from the main window.
        self.images.remove(lst[0]) # removes the saved image from self.images


    def png_inputs(self):
        chosen_pngs = QFileDialog.getOpenFileNames(self, 'Open file', "", "Png Files (*.png)", '/home')[0]  # Enables the selection of image file(s), gathering in a list.
        for png in chosen_pngs:
            if png not in self.images:  # if the image is not already opened(shown on the main window as an image button)
                self.images.append(png)
                # creating image buttons for each image:
                image_btn = QPushButton(self)
                image_btn.setIcon(QIcon(png))
                image_btn.setIconSize(QSize(64, 40))
                image_btn.setFixedSize(70, 46)
                image_btn.setToolTip(os.path.basename(png) + "\n" + 'click to configure')
                helper_func = lambda i: (lambda: self.new_data(i))  # lambda function to enable button click connection to functions requiring argument(s).
                image_btn.clicked.connect(helper_func([png, image_btn]))  # when an image button is clicked, new_data method is called and its pop-up window appears.
                image_btn.move(self.posx, self.posy)
                image_btn.show()
                # positioning newly created image buttons.
                self.posx += 80
                if self.posx == 790:
                    self.posy += 56
                    self.posx = 390


    def draw_patterns_and_get_coordinates(self): # this method is connected to self.draw_button and self.coordinate_button, gets called when at least one of them are clicked.
        img = Drawing.Strokes(self.images, self.data)  # creates an instance of Strokes class.
        sender = self.sender()  # returns which button gets clicked.
        if sender == self.draw_button: # when self.draw_button is clicked, an image is drawn according to the data in the created instance above and shown on a new window.
            try: img.draw_all()
            except: QMessageBox.information(self, "Data Error", "Please provide at least one image file and relevant data")
            else: QMessageBox.information(self, "Drawing", "Task completed!")
        elif sender == self.coordinate_button:  # when self.coordinate_button is clicked, coordinates of all strokes in the resulting image are written and saved in a ped file.
            try: img.all_points()
            except: QMessageBox.information(self, "Data Error", "Please provide at least one image file and relevant data")
            else:
                name = QFileDialog.getSaveFileName(self, 'Save File', "", "Ped Files (*.ped)")[0] + ".ped"
                shutil.copy(os.path.abspath(img.filename), name)
                if os.path.basename(name) != img.filename: os.remove(img.filename)
                QMessageBox.information(self, "Writing Coordinates", "Task completed!")
        failed_images = []
        for image in self.images:
            if os.path.basename(image) not in self.data:
                failed_images.append(os.path.basename(image))
        if len(failed_images) > 0: QMessageBox.information(self, "Failed", "Image(s) were discarded due to lack of relevant stroke data")


    EXIT_CODE_REBOOT = -345  # used for restarting the app, clearing all previous images and data.
    @staticmethod
    def clear_all():  # restarts the application, connected to clear_btn.
        qApp.exit(MainApp.EXIT_CODE_REBOOT)


if __name__ == '__main__':
    currentExitCode = MainApp.EXIT_CODE_REBOOT
    while currentExitCode == MainApp.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        w = MainApp()
        currentExitCode = app.exec_()
        app = None

