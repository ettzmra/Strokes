# import sys
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
#                              QVBoxLayout, QApplication)
#
#
# class Example(QWidget):  # SIGNALS AND SLOTS
#     '''In our example, we display a QtGui.QLCDNumber and a QtGui.QSlider. We change the lcd number by dragging the slider knob.
#        The sender is an object that sends a signal. The receiver is the object that receives the signal. The slot is the method that reacts to the signal.'''
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#     def initUI(self):
#         '''PyQt5 has a unique signal and slot mechanism to deal with events. Signals and slots are used for communication between objects.
#         A signal is emitted when a particular event occurs. A slot can be any Python callable. A slot is called when its connected signal is emitted.'''
#
#         lcd = QLCDNumber(self)
#         sld = QSlider(Qt.Horizontal, self)
#
#         vbox = QVBoxLayout()
#         vbox.addWidget(lcd)
#         vbox.addWidget(sld)
#         # vbox.addStretch(1)
#
#         self.setLayout(vbox)
#         sld.valueChanged.connect(lcd.display)  # Here we connect a valueChanged signal of the slider to the display slot of the lcd number.
#         #
#
#         self.setGeometry(300, 300, 250, 150)
#         self.setWindowTitle('Signal and slot')
#         self.show()


import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel


class Example(QWidget):
    '''Event object is a Python object that contains a number of attributes describing the event. Event object is specific to the generated event type.'''

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        x = 0
        y = 0

        self.text = "x: {0},  y: {1}".format(x, y)

        self.label = QLabel(self.text, self)
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)

        self.setMouseTracking(True)  # Mouse tracking is disabled by default, so the widget only receives mouse move events when at least one mouse button is pressed while the mouse is being moved. If mouse tracking is enabled, the widget receives mouse move events even if no buttons are pressed.

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 200)
        self.setWindowTitle('Event object')
        self.show()

    def mouseMoveEvent(self, e):  # EVENT OBJECT
        '''The e is the event object; it contains data about the event that was triggered; in our case, a mouse move event.
           With the x() and y() methods we determine the x and y coordinates of the mouse pointer. We build the string and set it to the label widget.'''
        x = e.x()
        y = e.y()

        text = "x: {0},  y: {1}".format(x, y)
        self.label.setText(text)

    def keyPressEvent(self, e):  # REIMPLEMENTING EVENT HANDLER
        '''In our example, we reimplement the keyPressEvent() event handler.'''
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())