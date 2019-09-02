"""ZetCode PyQt5 tutorial"""
import sys
from PyQt5.QtWidgets import (QWidget, QFileDialog, QCheckBox, QGridLayout, QToolBar, QToolTip, QFrame, QListWidget, QListWidgetItem, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication, QMessageBox, QAction, qApp, QMainWindow, QDesktopWidget, QTextEdit, QMenu)  # QDesktopWidget class provides information about the user's desktop, including the screen size.
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import pyqtSignal, QObject, Qt

class MyPopup(QWidget):
    def __init__(self):
        super().__init__()

    #     self.name = name
    #
    #     self.initUI()
    #
    # def initUI(self):
    #     lblName = QLabel(self.name, self)


class Communicate(QObject):  # EMITTING SIGNALS   (A signal is created with the pyqtSignal() as a class attribute of the external Communicate class.)
    '''We create a new signal called closeApp. This signal is emitted during a mouse press event.
       The signal is connected to the close() slot of the QMainWindow.'''
    closeApp = pyqtSignal()


class Example(QMainWindow):
    '''The previous example (see Bookmark 1) was coded in a procedural style. Python programming language supports both procedural and OOP styles.
    Programming in PyQt5 means programming in OOP. Three important things in OOP are classes, data, and methods. Here we create a new class called Example.
    The Example class inherits from the QMainWindow class. This means that we call two constructors: the first one for the Example class and the second one for the inherited class.
    The super() method returns the parent object of the Example class and we call its constructor. The __init__() method is a constructor method in Python language.'''

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.c = Communicate()
        self.c.closeApp.connect(self.close)

        self.w = MyPopup()
        self.w.setGeometry(100, 100, 400, 200)
        self.w.show()


# CHECKBOXES
        self.cb = QCheckBox('Show Title', self)
        #self.cb.toggle()
        self.cb.stateChanged.connect(self.changeTitle)

# BUTTONS
        qbtn = QPushButton('Quit', self)  # constructor of a QPushButton widget: QPushButton(string text, QWidget parent = None). The parent is a widget on which we place our button. In our case it will be a QWidget. Here the parent widget is the Example widget, which is a QWidget by inheritance.
        qbtn.setToolTip('<b>click to close</b>')  # Widgets of an application form a hierarchy. In this hierarchy, most widgets have their parents. Widgets without parents are top level windows.
        qbtn.resize(qbtn.sizeHint())  # The sizeHint() method gives a recommended size for the button. qbtn.move(200, 170) can move the button on the window.a
        qbtn.clicked.connect(QApplication.instance().quit)  # QCoreApplication, which is retrieved with QApplication.instance(), contains the main event loop—it processes and dispatches all events.
        qbtn.clicked.connect(self.buttonClicked)  # EVENT SENDER

# LABELS, TEXT AND LINE EDITS
        title = QLabel('Title')
        title.setFont(QFont('Calibri', 13))
        titleEdit = QLineEdit()
        self.editor = QTextEdit()
        self.editor.setAutoFormatting(QTextEdit.AutoAll)  # Setup the QTextEdit editor configuration
        font = QFont('Times', 12)
        self.editor.setFont(font)
        self.editor.setFontPointSize(12)  # We need to repeat the size to init the current format.
        self.lbl = QLabel('mel')
        titleEdit.textChanged[str].connect(self.onChanged)  # If the text in the line edit widget changes, we call the onChanged() method.


        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        positions = [(i, j) for i in range(5) for j in range(4)]


# OTHER WIDGETS
#         self.listWidget = QListWidget(self)
#         self.listWidget.itemDoubleClicked.connect(self.buildExamplePopup)
#         self.listWidget.show()
#
#         names = ["Jack", "Chris", "Joey", "Kim", "Duncan"]
#
#         for n in names:
#             QListWidgetItem(n, self.listWidget)


# LAYOUTS
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        grid = QGridLayout()

        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)

        hbox.addWidget(title)
        hbox.addWidget(titleEdit)
        hbox.addWidget(self.cb)

        hbox2.addStretch(1)
        hbox2.addWidget(qbtn)
        hbox2.addWidget(self.lbl)
        hbox2.addStretch(1)

        #vbox.addStretch(1)
        vbox.addLayout(grid)
        vbox.addWidget(self.editor)
        #vbox.addWidget(self.listWidget)
        #vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)

# STATUSBAR
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')  # we call the statusBar() method from QMainWindow class.

        QToolTip.setFont(QFont('SansSerif', 10))  # This static method sets a font used to render tooltips. We use a 10pt SansSerif font.
        self.setToolTip('This is a <b>QWidget</b> widget')  # To create a tooltip, we call the setTooltip() method. We can use rich text formatting.

# ACTIONS
        open_file_action = QAction(QIcon('/home/mel/Downloads/Telegram Desktop/Strokes/StrokeGUI/dolphin.png'), "Open file...", self)  # QAction is an abstraction for actions performed with a menubar, toolbar, or with a custom keyboard shortcut.
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)

        save_file_action = QAction(QIcon('/home/mel/Downloads/Telegram Desktop/Strokes/StrokeGUI/balls.png'), "Save", self)
        save_file_action.setStatusTip("Save current page")
        #save_file_action.triggered.connect(self.file_save)

        save_As_action = QAction("Save As...", self)
        save_As_action.setStatusTip("Save current page to specified file")
        #save_As_action.triggered.connect(self.file_saveas)

        undo_action = QAction("Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)

        redo_action = QAction("Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)

        exit_act = QAction(QIcon('/home/mel/Downloads/Telegram Desktop/Strokes/StrokeGUI/icon.png'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)

        viewStatAct = QAction('View statusbar', self, checkable=True)  # With the checkable option we create a checkable menu.
        viewStatAct.setStatusTip('View statusbar')
        viewStatAct.setChecked(True)  # Since the statusbar is visible from the start, we check the action with setChecked() method.
        viewStatAct.triggered.connect(self.toggleMenu)

# MENUS
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')

        viewMenu = QMenu('View', self)
        viewMenu.addAction(viewStatAct)

        fileMenu.addAction(open_file_action)
        fileMenu.addAction(save_file_action)
        fileMenu.addAction(save_As_action)
        fileMenu.addSeparator()
        fileMenu.addMenu(viewMenu)
        fileMenu.addAction(exit_act)
        editMenu.addAction(undo_action)
        editMenu.addSeparator()
        editMenu.addAction(redo_action)



# TOOLBARS
        self.toolbar = QToolBar("Edit")
        self.addToolBar(self.toolbar)
        #self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(open_file_action)
        self.toolbar.addAction(save_file_action)
        self.toolbar.addAction(exit_act)
        self.toolbar.addSeparator()
        self.toolbar.addAction(viewStatAct)
        self.toolbar.addSeparator()


# APP WINDOW
        # First 3 methods below are inherited from the QWidget class. setGeometry() locates the window on the screen and sets it size, combining the resize() and move() methods in one method. (see Bookmark 1 for resize() and move())
        self.setGeometry(300, 300, 800, 700)  # The first two parameters are the x and y positions of the window. The third is the width and the fourth is the height of the window.
        self.setWindowTitle(' ')
        self.setWindowIcon(QIcon('/home/mel/Downloads/Telegram Desktop/Strokes/StrokeGUI/diamond.png'))
        self.center()  # The code that will center the window.
        self.show()  # The show() method displays the widget on the screen. A widget is first created in memory and later shown on the screen.


    def mousePressEvent(self, event):  # EMITTING SIGNALS
        '''When we click on the window with a mouse pointer, the closeApp signal is emitted. The application terminates.'''
        self.c.closeApp.emit()


    def onChanged(self, text):

        self.lbl.setText(text)
        self.lbl.adjustSize()



    def buttonClicked(self):  # EVENT SENDER  !!!!
        '''We determine the signal source by calling the sender() method. In the statusbar of the application, we show the label of the button being pressed.'''
        sender = self.sender()
        if sender == self.qbtn:
            print(sender.text())
        self.statusBar().showMessage(sender.text() + ' was pressed')


    def toggleMenu(self, state):   # Depending on the state of the action, we show or hide the statusbar.

        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()


    def file_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                self.editor.setText(data)


    def changeTitle(self, state):
        if state == Qt.Checked: self.setWindowTitle('QCheckBox')
        else: self.setWindowTitle('Sample')


    def contextMenuEvent(self, event):
        '''The context menu is displayed with the exec_() method. It gets the coordinates of the mouse pointer from the event object. The mapToGlobal() method translates the widget coordinates to the global screen coordinates'''
        cmenu = QMenu(self)
        cmenu.addAction("New")
        cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            qApp.quit()


    def closeEvent(self, event):
        '''If we close a QWidget, the QCloseEvent is generated. To modify the widget behaviour we need to reimplement the closeEvent() event handler.'''
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #  The first string appears on the titlebar. The second string is the message text displayed by the dialog. The third argument specifies the combination of buttons appearing in the dialog.
        # The last parameter is the default button. It is the button which has initially the keyboard focus. The return value is stored in the reply variable.
        if reply == QMessageBox.Yes: event.accept()
        else: event.ignore()



    def center(self):  # The QDesktopWidget class provides information about the user's desktop, including the screen size.
        qr = self.frameGeometry()  # We get a rectangle specifying the geometry of the main window.
        center_point = QDesktopWidget().availableGeometry().center()  # We figure out the screen resolution of our monitor. And from this resolution, we get the center point.
        qr.moveCenter(center_point)  # Our rectangle has already its width and height. Now we set the center of the rectangle to the center of the screen.
        self.move(qr.topLeft())  # We move the top-left point of the application window to the top-left point of the qr rectangle, thus centering the window on our screen.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = Example()
    # w = QWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    # w.show()
    sys.exit(app.exec_()) # Finally, we enter the mainloop of the application. The event handling starts from this point. The mainloop receives events from the window system and dispatches them to the application widgets. The mainloop ends if we call the exit() method or the main widget is destroyed. The sys.exit() method ensures a clean exit. The environment will be informed how the application ended.

