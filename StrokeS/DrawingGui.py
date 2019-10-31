import sys, os, json
from PyQt5.QtWidgets import QWidget, QComboBox, qApp, QLineEdit, QFileDialog, QToolTip, QHBoxLayout, QGridLayout, QLabel, QTextEdit, QPushButton, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from StrokeS import Drawing



class Specs(QWidget):
    def __init__(self, spec, lst=None):
        super().__init__()
        self.spec = spec
        self.lbl = QLabel(self.spec)
        self.lbl.setFixedSize(65, 20)
        if lst is None:
            self.editor = QLineEdit()
            self.editor.setToolTip("Enter a number")
            self.editor.textChanged[str].connect(self.given_text)
        else:
            self.editor = QComboBox()
            self.editor.addItems(lst)
            self.editor.activated[str].connect(self.given_text)


    def given_text(self, text):
        try: num = int(text)
        except:
            if len(text) == 0 and hasattr(self, 'input'): del self.input
            if len(text) > 0 and text != "Choose": self.input = text
        else:
            if num > 0: self.input = num



class NewJson(QWidget):
    def __init__(self, image, data):
        super().__init__()
        self.img = os.path.basename(image)
        self.img_full_path = image

        self.spec_dict = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.img)
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
        self.coord_btn.clicked.connect(self.save_data_and_preview)
        self.save_btn.clicked.connect(self.save_data_and_preview)
        self.preview_btn.clicked.connect(self.save_data_and_preview)
        self.setLayout(grid)

    def save_data_and_preview(self):
        sender = self.sender()
        chosen_specs = {self.img: {}}
        random = self.spec_list[1]
        for each in self.spec_list:
            if hasattr(each, 'input'): chosen_specs[self.img][each.spec] = each.input
            elif hasattr(random, 'input'):
                if random.input == "all": random_specs = ["size","position", "angle"]
                else: random_specs = random.input.split(",")
                if each.spec in random_specs:
                    if each.spec == "position": chosen_specs[self.img]["density"] = 0
                    else: chosen_specs[self.img][each.spec] = 0
            if not hasattr(each, 'input') and each.spec not in chosen_specs[self.img]:
                QMessageBox.information(self, "Warning", "Please make selection", QMessageBox.Ok)
                break
        if len(chosen_specs[self.img]) == 6:
            if sender == self.save_btn:
                self.spec_dict.update(chosen_specs)
            else:
                image = Drawing.Pattern([self.img_full_path], chosen_specs)
                if sender == self.preview_btn: image.draw_all()
                else: image.all_points(self.img + ".ped")


class BasicGui(QWidget):
    EXIT_CODE_REBOOT = -345

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        json_btn = QPushButton('Load Json File', self)
        png_btn = QPushButton('Choose Images', self)
        change_btn = QPushButton('Apply Changes', self)
        self.clear_btn = QPushButton('Restart', self)
        self.draw_button = QPushButton('Drawing Preview', self)
        self.coordinate_button = QPushButton('Get Coordinates', self)
        self.textbox = QTextEdit()
        self.textbox.setFixedSize(350, 450)

        hbox = QHBoxLayout()
        hbox.addWidget(self.coordinate_button)
        hbox.addWidget(self.clear_btn)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        grid_layout.addWidget(json_btn, 1, 0)
        grid_layout.addWidget(png_btn, 1, 1)
        grid_layout.addWidget(self.textbox, 2, 0)
        grid_layout.addWidget(change_btn, 3, 0)
        grid_layout.addWidget(self.draw_button, 4, 0)
        grid_layout.addLayout(hbox, 4, 1)

        self.setLayout(grid_layout)

# ACTIONS
        self.posx, self.posy = 390, 70
        self.data = {}
        self.images = []
        png_btn.clicked.connect(self.png_inputs)
        json_btn.clicked.connect(self.existing_json)
        self.draw_button.clicked.connect(self.draw_patterns_and_get_coordinates)
        self.coordinate_button.clicked.connect(self.draw_patterns_and_get_coordinates)
        change_btn.clicked.connect(self.change_json)
        self.clear_btn.clicked.connect(self.clear_all)

        self.setGeometry(300, 300, 800, 600)  # The first two parameters are the x and y positions of the window. The third is the width and the fourth is the height of the window.
        self.setFixedSize(800, 600)
        self.setWindowTitle('Images & Coordinates')
        self.show()


    def existing_json(self):
        file = QFileDialog.getOpenFileName(self, 'Open file', "","Json Files (*.json)", '/home')[0]
        try:
            with open(file, "r") as f:
                content = f.read()
                self.textbox.setText(content)
        except: pass
        else:
            try: self.data.update(json.loads(content))
            except: QMessageBox.information(self, "JSON Error", "Please fix the errors in your file", QMessageBox.Ok)


    def change_json(self):
        text = self.textbox.toPlainText()
        try: self.data.update(json.loads(text))
        except: QMessageBox.information(self, "JSON Error", "Please provide proper data", QMessageBox.Ok)


    def new_json(self, lst):
        self.popup = NewJson(lst[0], self.data)
        self.popup.setGeometry(400, 400, 400, 300)
        self.popup.show()
        helper_func = lambda i: (lambda: self.remove_image(i))
        self.popup.remove_btn.clicked.connect(helper_func(lst))
        self.popup.remove_btn.clicked.connect(self.popup.close)


    def remove_image(self, lst):
        lst[1].hide()
        self.images.remove(lst[0])
        if os.path.basename(lst[0]) in self.data: del self.data[os.path.basename(lst[0])]


    def png_inputs(self):
        chosen_pngs = QFileDialog.getOpenFileNames(self, 'Open file', "", "Png Files (*.png)", '/home')[0]  # notice the plural suffix "s" in ".getOpenFileNames", which enables selection of multiple files
        print(chosen_pngs)
        for png in chosen_pngs:
            if png not in self.images:
                self.images.append(png)
                image_btn = QPushButton(self)
                image_btn.setIcon(QIcon(png))
                image_btn.setIconSize(QSize(64, 40))
                image_btn.setFixedSize(70, 46)
                image_btn.setToolTip(os.path.basename(png) + "\n" + 'click to configure')
                helper_func = lambda i: (lambda: self.new_json(i))
                image_btn.clicked.connect(helper_func([png, image_btn]))
                image_btn.move(self.posx, self.posy)
                image_btn.show()
                self.posx += 80
                if self.posx == 790:
                    self.posy += 56
                    self.posx = 390


    def draw_patterns_and_get_coordinates(self):
        try: img = Drawing.Pattern(self.images, self.data)
        except: QMessageBox.information(self, "Data Error", "Please provide at least one image file and relevant data", QMessageBox.Ok)
        else:
            sender = self.sender()
            if sender == self.draw_button: img.draw_all()
            elif sender == self.coordinate_button:
                name = QFileDialog.getSaveFileName(self, 'Save File', "", "Ped Files (*.ped)")[0]
                img.all_points(name)
                QMessageBox.information(self, "Writing Coordinates", "Task completed!", QMessageBox.Ok)


    def clear_all(self):
        qApp.exit(BasicGui.EXIT_CODE_REBOOT)


if __name__ == '__main__':
    currentExitCode = BasicGui.EXIT_CODE_REBOOT
    while currentExitCode == BasicGui.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        w = BasicGui()
        currentExitCode = app.exec_()
        app = None

