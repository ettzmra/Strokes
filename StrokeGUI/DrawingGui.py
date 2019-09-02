import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QFileDialog, QCheckBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QAction, QApplication
import os
from StrokeS import Drawing

class Basic(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.json_data = QPushButton('Load Json', self)
        self.load_png = QPushButton('Choose PNGs', self)
        # self.name_output = QLabel('Output Image Name (optional):')
        # self.output_image_name = QLineEdit()
        # self.name_ped = QLabel('Ped File Name (optional):')
        # self.ped_file_name = QLineEdit()
        self.draw_button = QPushButton('Draw All', self)
        self.coordinate_button = QPushButton('Get Coordinates', self)




# LAYOUTS
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        hlayout3 = QHBoxLayout()
        hlayout4 = QHBoxLayout()

        hlayout.addWidget(self.json_data)
        hlayout.addWidget(self.load_png)
        vlayout.addLayout(hlayout)
        vlayout.addStretch(1)

        # hlayout2.addWidget(self.name_output)
        # hlayout2.addWidget(self.output_image_name)
        # #hlayout2.addWidget(self.cb)
        # vlayout.addLayout(hlayout2)
        #
        # hlayout3.addWidget(self.name_ped)
        # hlayout3.addWidget(self.ped_file_name)
        # vlayout.addLayout(hlayout3)
        # vlayout.addStretch(1)

        hlayout4.addWidget(self.draw_button)
        hlayout4.addWidget(self.coordinate_button)
        vlayout.addLayout(hlayout4)

        self.setLayout(vlayout)

# ACTIONS
        self.png_names = []
        self.load_png.clicked.connect(self.open_files)
        self.json_data.clicked.connect(self.pattern_data)
        self.draw_button.clicked.connect(self.patterns_and_coordinates)
        self.coordinate_button.clicked.connect(self.patterns_and_coordinates)
        #self.outputs()


        self.setGeometry(300, 300, 400, 200)  # The first two parameters are the x and y positions of the window. The third is the width and the fourth is the height of the window.
        self.setWindowTitle('Images & Coordinates')
        self.show()


    def pattern_data(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.json_file = file_name


    def open_files(self):
        png_name = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.png_names.append(os.path.basename(png_name))
        print(self.png_names)

    # def outputs(self):
    #     if self.output_image_name.textChanged[str]:
    #         self.output_img = self.output_image_name.text() + ".png"
    #     else: self.output_img = "ResultingImage.png"
    #
    #     if self.ped_file_name.textChanged[str]:
    #         self.output_ped = self.ped_file_name.text() + ".ped"
    #     else: self.output_ped = "Result.ped"

    def patterns_and_coordinates(self):
        img = Drawing.Pattern(self.json_file, "resultimage.png", *self.png_names)
        buttonClicked = self.sender()
        if buttonClicked == self.draw_button:
            img.draw_all()
        if buttonClicked == self.coordinate_button:
            img.all_points("resultcoords.ped")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    BasicWidget = Basic()
    sys.exit(app.exec_())
