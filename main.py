import cv2
from sys import argv
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from main_window import UiMainWindow
from sub_window import Image


class MainWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        super(MainWindow,  self).__init__()
        self.setup_ui(self)
        self.window_id = 0
        self.active_window = None
        self.windows = dict()

        # Setting the mdi area as the center widget
        self.setCentralWidget(self.mdiArea)
        self.mdiArea.subWindowActivated.connect(self.update_active_window)

        self.actionOpen.triggered.connect(self.open)

    def open(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Open image", "", "(*.bmp *.jpeg *.jpg *.png);")
        if not file_paths:
            return
        for file_path in file_paths:
            image_name = file_path.split("/")[-1]
            image_data = cv2.imread(file_path, -1)
            self.__add_window(image_name, image_data)

    def __add_window(self, image_name, image_data):
        self.window_id += 1
        window = Image(self.window_id, image_name, image_data)
        self.windows[self.window_id] = window
        self.mdiArea.addSubWindow(window.sub_window)
        window.sub_window.show()

    def update_active_window(self, sub_window):
        if sub_window is not None and sub_window.window_id in self.windows:
            self.active_window = self.windows.get(sub_window.window_id)


if __name__ == '__main__':
    app = QApplication(argv)
    UIWindow = MainWindow()
    UIWindow.show()
    app.exec_()
