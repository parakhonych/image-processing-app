import cv2
from sys import argv
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog,QDialog
from main_window import UiMainWindow
from sub_window import Image
from rename import Rename


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

        # File menu
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionExit.triggered.connect(self.close)
        self.actionLiveMode.triggered.connect(self.live)

        # Windows menu
        self.actionCascade.triggered.connect(self.mdiArea.cascadeSubWindows)
        self.actionDuplicate.triggered.connect(self.duplicate_window)
        self.actionRename.triggered.connect(self.rename_window)

    def __add_window(self, image_name, image_data):
        self.window_id += 1
        window = Image(self.window_id, image_name, image_data)
        self.windows[self.window_id] = window
        self.mdiArea.addSubWindow(window.sub_window)
        window.sub_window.show()

    def update_active_window(self, sub_window):
        if sub_window is not None and sub_window.window_id in self.windows:
            self.active_window = self.windows.get(sub_window.window_id)

    def open(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Open image", "", "(*.bmp *.jpeg *.jpg *.png);")
        if not file_paths:
            return
        for file_path in file_paths:
            image_name = file_path.split("/")[-1]
            image_data = cv2.imread(file_path, -1)
            self.__add_window(image_name, image_data)

    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save image", self.active_window.name, "All Files (*);;")
        if not file_path:
            return
        cv2.imwrite(file_path, self.active_window.data)

    def live(self):
        cap = cv2.VideoCapture(0)
        while(True):
            _, image = cap.read()
            if cv2.waitKey(30) & 0xFF == ord('k'):
                self.__add_window("Photo number" + str(self.window_id + 1), image)
                break
            cv2.imshow('img', image)
        cap.release()
        cv2.destroyAllWindows()

    def rename_window(self):
        rename_dialog = Rename(self.active_window.name, 0)
        self.setDisabled(True)
        if rename_dialog.exec():
            self.active_window.sub_window.setWindowTitle(rename_dialog.new_name)
        self.setDisabled(False)

    def duplicate_window(self):
        duplicate_dialog = Rename(self.active_window.name, 1)
        self.setDisabled(True)
        if duplicate_dialog.exec():
            self.__add_window(duplicate_dialog.new_name, self.active_window.data)
        self.setDisabled(False)









if __name__ == '__main__':
    app = QApplication(argv)
    UIWindow = MainWindow()
    UIWindow.show()
    app.exec_()
