import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QListWidget, QListWidgetItem, QLabel, QPushButton, QApplication


class exampleWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        listWidget = QListWidget(self)
        listWidget.itemDoubleClicked.connect(self.buildExamplePopup)

        names = ["Jack", "Chris", "Joey", "Kim", "Duncan"]

        for n in names:
            QListWidgetItem(n, listWidget)

        self.setGeometry(100, 100, 100, 100)
        self.show()

    #@staticmethod
    def buildExamplePopup(self, item):
        name = item.text()
        self.exPopup = examplePopup(name)
        self.exPopup.setGeometry(100, 200, 100, 100)
        self.exPopup.show()


class examplePopup(QWidget):
    def __init__(self, name):
        super().__init__()

        self.name = name

        self.initUI()

    def initUI(self):
        lblName = QLabel(self.name, self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = exampleWidget()
    sys.exit(app.exec_())