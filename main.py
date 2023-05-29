import cv2
from sys import argv
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from ui_main_window import UiMainWindow
from sub_image_window import Image
from d_text_input import TextInput
from sub_histogram_window import SubHistogram


def check_active_window(method):
    def wrapper(self):
        if not self.active_window:
            message = "To perform this function, you should first open any picture. \n Follow these steps File -> Open"
            QMessageBox.warning(self, "Warning", message)
            return
        method(self)
    return wrapper


def check_active_window_lambda(method):
    def wrapper(self, scale):
        if not self.active_window:
            message = "To perform this function, you should first open any picture. \n Follow these steps File -> Open"
            QMessageBox.warning(self, "Warning", message)
            return
        method(self, scale)
    return wrapper


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
        self.actionZoom_In.triggered.connect(lambda: self.zoom(0.1))
        self.actionZoom_Out.triggered.connect(lambda: self.zoom(-0.1))
        self.actionZoom_Off.triggered.connect(lambda: self.zoom(0))

        # Processing menu
        self.actionBGR_Grayscale.triggered.connect(self.bgr2grayscale)
        self.actionBGR_RGB.triggered.connect(self.bgr2rgb)
        self.actionBGR_HSV.triggered.connect(self.bgr2hsv)
        self.actionResize.triggered.connect(self.resizing)
        #self.actionSplitting_into_channels.triggered.connect(self.splitting)

        # Analyzing menu
        self.actionHistogram.triggered.connect(self.histogram)

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

    @check_active_window
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

    @check_active_window
    def rename_window(self):
        rename_dialog = TextInput(self.active_window.name, "Rename")
        self.setDisabled(True)
        if rename_dialog.exec():
            self.active_window.sub_window.setWindowTitle(rename_dialog.new_name)
            self.active_window.name = rename_dialog.new_name
        self.setDisabled(False)

    @check_active_window
    def duplicate_window(self):
        duplicate_dialog = TextInput(self.active_window.name, "Duplicate")
        self.setDisabled(True)
        if duplicate_dialog.exec():
            self.__add_window(duplicate_dialog.new_name, self.active_window.data)
        self.setDisabled(False)

    @check_active_window_lambda
    def zoom(self, scale):
        if self.active_window.sub_window.scale + scale == self.active_window.sub_window.scale:
            self.active_window.sub_window.scale = 1
        else:
            self.active_window.sub_window.scale = self.active_window.sub_window.scale + scale
        self.active_window.sub_window.update_window()

    @check_active_window
    def histogram(self):
        hist = SubHistogram(self.window_id + 1, self.active_window)
        self.mdiArea.addSubWindow(hist)
        self.window_id = self.window_id + 2
        self.mdiArea.addSubWindow(hist.histogram_list)
        hist.show()

    @check_active_window
    def bgr2grayscale(self):
        self.__add_window("BGR to Grayscale " + self.active_window.name,
                          cv2.cvtColor(self.active_window.data, cv2.COLOR_BGR2GRAY))

    @check_active_window
    def bgr2rgb(self):
        self.__add_window("BGR to Grayscale " + self.active_window.name,
                          cv2.cvtColor(self.active_window.data, cv2.COLOR_BGR2RGB))

    @check_active_window
    def bgr2hsv(self):
        self.__add_window("BGR to Grayscale " + self.active_window.name,
                          cv2.cvtColor(self.active_window.data, cv2.COLOR_BGR2HSV))

    @check_active_window
    def resizing(self):
        self.__add_window("Size 256 x 256 " + self.active_window.name, cv2.resize(self.active_window.data, (256, 256)))

    @check_active_window
    def splitting(self):
        blue, green, red = cv2.split(self.active_window.data)
        self.add_window("Blue channel " + self.active_window.name, blue)
        self.add_window("Green channel " + self.active_window.name, green)
        self.add_window("Red channel " + self.active_window.name, red)


if __name__ == '__main__':
    app = QApplication(argv)
    UIWindow = MainWindow()
    UIWindow.show()
    app.exec_()
