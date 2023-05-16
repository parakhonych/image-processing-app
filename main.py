from sys import argv
from PyQt5.QtWidgets import QMainWindow, QApplication
from main_window import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow,  self).__init__()
        self.setupUi(self)
        self.show()

if __name__ == '__main__':
    app = QApplication(argv)
    UIWindow = MainWindow()
    app.exec_()