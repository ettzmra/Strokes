import sys, os, json
from PIL import Image, ImageDraw
from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit, QMenuBar, QCheckBox, QFileDialog, QToolTip, QVBoxLayout, QHBoxLayout, QMainWindow, QAction, QGridLayout, QLabel, QTextEdit, QPushButton, QApplication, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QFileSystemWatcher, QSize
from StrokeS import Drawing



class Specs(QWidget):
    def __init__(self, spec, lst=None):
        super().__init__()
        self.spec = spec
        self.lbl = QLabel(self.spec)
        if lst is None:
            self.editor = QLineEdit()
            self.editor.setToolTip("Enter a number")
            self.editor.textChanged[str].connect(self.given_text)
        else:
            self.editor = QComboBox()
            self.editor.addItems(lst)
            self.editor.activated[str].connect(self.given_text)


    def given_text(self, text):
        try: self.input = int(text)
        except: self.input = text



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
        self.save_btn = QPushButton("Save")
        self.preview_btn = QPushButton("Preview")
        self.spec_list = [ Specs("pattern", ["Choose", "lines","circles","dots"]),
                           Specs("random", ["Choose", "false", "all", "size", "position", "angle", "size, positions", "size, angle", "position, angle"]),
                           Specs("color", ["Choose", "black", "white", "blue", "green", "red", "yellow", "brown", "gray", "orange", "pink", "purple", "dark blue"]),
                           Specs("size"), Specs("density"), Specs("angle") ]
        positions = [(i,j) for i in [0, 2] for j in range(3)]
        for pos, spec in zip(positions, self.spec_list):
            grid.addWidget(spec.lbl, *pos)
            grid.addWidget(spec.editor, pos[0]+1, pos[1])
        grid.addWidget(self.preview_btn, 4, 1)
        grid.addWidget(self.save_btn, 4, 2)
        #self.preview_btn.clicked.connect(PreviewWindow(image, self.spec_dict))
        #helper_func = lambda i: (lambda: self.data_input(i))
        self.save_btn.clicked.connect(self.save_data_and_preview)
        self.preview_btn.clicked.connect(self.save_data_and_preview)
        self.setLayout(grid)

    def save_data_and_preview(self):
        sender = self.sender()
        chosen_specs = {self.img: {}}
        for each in self.spec_list:
            try:
                chosen_specs[self.img][each.spec] = each.input
            except:
                QMessageBox.information(self, "Warning", "Please make selection", QMessageBox.Ok)
                break
        if len(chosen_specs[self.img]) == 6:
            if sender == self.save_btn:
                self.spec_dict.update(chosen_specs)
            elif sender == self.preview_btn:
                self.image = Drawing.Pattern([self.img_full_path], chosen_specs)
                self.result = self.image.draw_all()
                self.preview = PreviewWindow("resulting image.png")

                #self.preview.setGeometry(300, 300, 800, 700)
                #self.preview.show()


class PreviewWindow(QMainWindow):
    def __init__(self, img):
        super().__init__()
        self.setWindowTitle("Preview")

        # save_file_act = QAction("Save", self)
        # save_file_act.setStatusTip("Save current page")
        # save_file_act.triggered.connect(self.file_save)

        # save_As_act = QAction("Save As...", self)
        # save_As_act.setStatusTip("Save current page to specified file")
        # save_As_act.triggered.connect(self.file_save)

        exit_act = QAction(QIcon('/home/mel/Downloads/Telegram Desktop/Strokes/StrokeGUI/icon.png'), 'Exit', self)
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        #fileMenu.addAction(save_file_act)
        #fileMenu.addAction(save_As_act)
        fileMenu.addAction(exit_act)

        # self.image = Drawing.Pattern([img], data)
        # self.result = self.image.draw_all()
        #pixmap = QPixmap.fromImage(ImageQt(img))
        #pixmap = qtimage.scaled(256, 160, Qt.KeepAspectRatio, Qt.FastTransformation)
        pixmap = QPixmap(img) #.scaled(256, 160, Qt.KeepAspectRatio, Qt.FastTransformation)
        label = QLabel(self)
        label.setPixmap(pixmap)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(label)
        self.setCentralWidget(container)
        self.resize(pixmap.width(), pixmap.height())
        #self.setGeometry(300, 300, 800, 700)  # The first two parameters are the x and y positions of the window. The third is the width and the fourth is the height of the window.
        #self.center()  # The code that will center the window.
        self.show()

    # def file_save(self):
    #     name = QFileDialog.getSaveFileName(self, 'Save File')
    #     self.result.save(name)
        # file = open(name, 'w')
        # text = self.textEdit.toPlainText()
        # file.write(text)
        # file.close()







class BasicGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('Load Json File', self)
        btn2 = QPushButton('Choose Images', self)
        btn3 = QPushButton('Apply Changes', self)
        self.textbox = QTextEdit()
        self.textbox.setFixedSize(350, 450)
        self.draw_button = QPushButton('Drawing Preview', self)
        self.coordinate_button = QPushButton('Get Coordinates', self)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(btn1, 1, 0)
        self.grid.addWidget(btn2, 1, 1)
        self.grid.addWidget(self.textbox, 2, 0)
        self.grid.addWidget(btn3, 3, 0)
        self.grid.addWidget(self.draw_button, 4, 0)
        self.grid.addWidget(self.coordinate_button, 4, 1)

        self.setLayout(self.grid)

# ACTIONS
        self.posx, self.posy = 390, 70
        self.data = {}
        self.images = []
        btn2.clicked.connect(self.png_inputs)
        btn1.clicked.connect(self.existing_json)
        self.draw_button.clicked.connect(self.draw_patterns)
        self.coordinate_button.clicked.connect(self.get_coordinates)
        btn3.clicked.connect(self.change_json)

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
        else: self.data.update(json.loads(content))


    def change_json(self):
        text = self.textbox.toPlainText()
        try: self.data.update(json.loads(text))
        except: pass
        print(self.data)


    def new_json(self, png):
        self.popup = NewJson(png, self.data)
        self.popup.setGeometry(400, 400, 400, 300)
        self.popup.show()


    def png_inputs(self):
        chosen_pngs = QFileDialog.getOpenFileNames(self, 'Open file', "", "Png Files (*.png)", '/home')[0]  # notice the plural suffix "s" in ".getOpenFileNames", which enables selection of multiple files
        print(chosen_pngs)
        for png in chosen_pngs:
            if png not in self.images:
                self.label = QPushButton(self)
                self.label.setIcon(QIcon(png))
                self.label.setIconSize(QSize(64, 40))
                self.label.setFixedSize(70, 46)
                self.label.setToolTip(os.path.basename(png) + "\n" + 'click to configure')
                helper_func = lambda i: (lambda: self.new_json(i))
                self.label.clicked.connect(helper_func(png))
                self.label.move(self.posx, self.posy)
                self.label.show()
                self.posx += 80
                if self.posx == 790:
                    self.posy += 56
                    self.posx = 390


    def draw_patterns(self):
        img = Drawing.Pattern(self.images, self.json_file)
        result = img.draw_all()
        pixmap = QPixmap(result).scaled(256, 160, Qt.KeepAspectRatio, Qt.FastTransformation)
        QLabel().setPixmap(pixmap).show()


    def get_coordinates(self):
        img = Drawing.Pattern(self.images, self.json_file,)
        img.all_points()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    BasicWidget = BasicGui()
    sys.exit(app.exec_())
