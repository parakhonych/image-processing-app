import cv2
from os import path as os_path
from sys import argv, path

import matplotlib.pyplot as plt

path.append(os_path.abspath(os_path.join(os_path.dirname(__file__), os_path.pardir)))
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from src.UI.ui_main_window import UiMainWindow
from src.subWindows.sub_image_window import Image
from src.Dialogs import TextInput
from src.subWindows.sub_histogram_window import SubHistogram
from src.Dialogs import HistogramManipulationStretching
from numpy import zeros, array
import numpy as np
from numpy.ma import masked_equal
from src.Dialogs import PointOperationThresholding
from src.Dialogs import PointOperationPosterization
from src.Dialogs import Blurring
from src.Dialogs import EdgeDetection
from src.Dialogs import LinearSharpening
from src.Dialogs import UniversalMask
from src.Dialogs import ImageCalculator
from src.Dialogs import Morphological
from src.Dialogs import ObjectDetails
from src.Dialogs import NeuralTransfer

def check_color_window(method):
    def wrapper(self):
        if self.active_window.gray:
            message = "Only color images are required for this function.\n" \
                      "You can open it with the following steps: File -> Open"
            QMessageBox.warning(self, "Warning", message)
            return
        method(self)
    return wrapper


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
        # Conversion
        self.actionBGR_Grayscale.triggered.connect(self.bgr2grayscale)
        self.actionBGR_RGB.triggered.connect(self.bgr2rgb)
        self.actionBGR_HSV.triggered.connect(self.bgr2hsv)

        self.actionResize.triggered.connect(self.resizing)

        self.actionSplitting_into_channels.triggered.connect(self.splitting)

        # Histogram manipulation

        self.actionStretching.triggered.connect(self.stretching)
        self.actionEqualization.triggered.connect(self.equalization)

        # Point operation

        self.actionNegation.triggered.connect(self.negation)
        self.actionThresholding.triggered.connect(self.point_operation_thresholding)
        self.actionPosterize.triggered.connect(self.point_operation_posterization)

        # Local operation
        self.actionBlur.triggered.connect(self.blurring_image)
        self.actionEdgeDetection.triggered.connect(self.edge_detection)
        self.actionLinearSharpening.triggered.connect(self.linear_sharpening_image)
        self.actionUniversal.triggered.connect(self.universal_mask)
        self.actionMorphology.triggered.connect(self.morphology)

        self.actionImage_calculator.triggered.connect(self.image_calculation)
        self.actionWatershed.triggered.connect(self.watershed)
        # Analyzing menu
        self.actionHistogram.triggered.connect(self.histogram)
        self.actionObjectDetails.triggered.connect(self.finding_object_details)

        # AI
        self.actionNeural_transfer_of_style.triggered.connect(self.neural_transfer)

        # Info menu
        self.actionAbout.triggered.connect(self.about_program)
        self.actionAuthor.triggered.connect(self.author)
        self.actionHelp.triggered.connect(self.helping)

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
        while True:
            _, image = cap.read()
            if cv2.waitKey(30) & 0xFF == ord('k'):
                self.__add_window("Photo number" + str(self.window_id + 1), image)
                break
            cv2.imshow('live mode', image)
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

    @staticmethod
    def __conversiton_to_grayscale(image_data):
        return cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)

    @check_active_window
    def bgr2grayscale(self):
        self.__add_window("BGR to Grayscale " + self.active_window.name,
                          self.__conversiton_to_grayscale(self.active_window.data))

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
        self.__add_window("Size 224 x 224 " + self.active_window.name, cv2.resize(self.active_window.data, (224, 224)))

    @check_active_window
    @check_color_window
    def splitting(self):
        blue, green, red = cv2.split(self.active_window.data)
        self.__add_window("Blue channel " + self.active_window.name, blue)
        self.__add_window("Green channel " + self.active_window.name, green)
        self.__add_window("Red channel " + self.active_window.name, red)

    @check_active_window
    def stretching(self):
        image_data = self.active_window.data
        range_slider = HistogramManipulationStretching(image_data)
        if range_slider.exec_():
            self.__add_window("Stretching " + self.active_window.name, range_slider.image_data)

    @check_active_window
    def equalization(self):
        image_data = self.active_window.data
        if self.active_window.gray:
            hist = zeros(256)
            for h in range(image_data.shape[0]):
                for w in range(image_data.shape[1]):
                    pixel = image_data[h, w]
                    hist[pixel] += 1
            hist = iter(hist)
            new_hist = [next(hist)]
            for value in hist:
                new_hist.append(new_hist[-1] + value)
            new_hist = array(new_hist)
            cumulative_sum = masked_equal(new_hist, 0)
            cumulative_sum_min = cumulative_sum.min()
            cumulative_sum_max = cumulative_sum.max()
            new_hist = ((new_hist - cumulative_sum_min) * 255) / (cumulative_sum_max - cumulative_sum_min)
            new_hist = new_hist.astype('uint8')
            self.__add_window("Equalization of " + self.active_window.name, new_hist[image_data])
        else:
            b, g, r = cv2.split(image_data)
            b_eq = cv2.equalizeHist(b)
            g_eq = cv2.equalizeHist(g)
            r_eq = cv2.equalizeHist(r)
            equalized_image = cv2.merge((b_eq, g_eq, r_eq))
            self.__add_window("Equalization of " + self.active_window.name, equalized_image)


    @check_active_window
    def negation(self):
        image_data = self.active_window.data
        if len(self.active_window.data.shape) > 2:
            image_data = self.__conversiton_to_grayscale(image_data)
        self.__add_window("Negation of" + self.active_window.name, 255-image_data)

    @check_active_window
    def point_operation_thresholding(self):
        image_data = self.active_window.data
        range_slider = PointOperationThresholding(image_data, self.active_window.gray)
        if range_slider.exec_():
            self.__add_window("Thresholding " + self.active_window.name, range_slider.image_data)

    @check_active_window
    def point_operation_posterization(self):
        image_data = self.active_window.data
        range_slider = PointOperationPosterization(image_data, self.active_window.gray)
        if range_slider.exec_():
            self.__add_window("Point operation posterization " + self.active_window.name, range_slider.image_data)

    @check_active_window
    def blurring_image(self):
        image_data = self.active_window.data
        blur = Blurring(image_data)
        if blur.exec_():
            self.__add_window("Blurring " + self.active_window.name, blur.image_data)

    @check_active_window
    def edge_detection(self):
        image_data = self.active_window.data
        edge_detect = EdgeDetection(image_data)
        if edge_detect.exec_():
            self.__add_window("Edge detection " + edge_detect.comboBoxTypes.currentText() + self.active_window.name, edge_detect.image_data)

    @check_active_window
    def linear_sharpening_image(self):
        image_data = self.active_window.data
        lin_sharp = LinearSharpening(image_data)
        if lin_sharp.exec_():
            self.__add_window("Linear sharpening  " + lin_sharp.comboBoxTypes.currentText() + " "
                              + self.active_window.name, lin_sharp.image_data)

    @check_active_window
    def universal_mask(self):
        image_data = self.active_window.data
        UniMask = UniversalMask(image_data, self.active_window.gray)
        if UniMask.exec_():
            self.__add_window("Universal mask" + self.active_window.name, UniMask.image_data)

    @check_active_window
    def image_calculation(self):
        ImageCal = ImageCalculator(self.windows)
        if ImageCal.exec_():
            self.__add_window("Image calculator " + self.active_window.name, ImageCal.image_data)

    @check_active_window
    def morphology(self):
        ImageCal = Morphological(self.active_window.data)
        if ImageCal.exec_():
            self.__add_window("Morph " + self.active_window.name, ImageCal.image_data)

    @check_active_window
    @check_color_window
    def watershed(self):
        gray_image = cv2.cvtColor(self.active_window.data, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        distance_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, thresholding = cv2.threshold(distance_transform, 0.5 * distance_transform.max(), 255, 0)
        thresholding = np.uint8(thresholding)
        substraction = cv2.subtract(cv2.dilate(opening, kernel, iterations=1), thresholding)
        _, marks = cv2.connectedComponents(thresholding)
        marks = marks + 1
        marks[substraction == 255] = 0
        markers2 = cv2.watershed(self.active_window.data, marks)
        gray_image[markers2 == -1] = 255
        self.active_window.data[markers2 == -1] = [255, 0, 0]
        self.__add_window("Watershed " + self.active_window.name,
                          cv2.convertScaleAbs(cv2.applyColorMap(np.uint8(markers2 * 10), cv2.COLORMAP_JET)))
        QMessageBox.information(self, "Info", str(np.max(markers2)) + " objects have been found")

    @check_active_window
    def finding_object_details(self):
        if self.active_window.gray:
            ObjDet = ObjectDetails(self.active_window.data)
        else:
            ObjDet = ObjectDetails(self.__conversiton_to_grayscale(self.active_window.data))
        ObjDet.exec_()

    @check_active_window
    def neural_transfer(self):
        NeuralTransferStyle = NeuralTransfer(self.windows)
        if NeuralTransferStyle.exec_():
            self.__add_window("Transfer style.jpg", NeuralTransferStyle.image_result)

    def helping(self):
        text = """              
                <p style="text-align: center">
                    <table>
                        <tr><td>Application to proccesing image</td></tr>
                        <tr><td></td></tr>
                        <tr><td></td></tr>
                        <tr><td></td></tr>
                        <tr><td> </td></tr>
                        <tr><td></td></tr>     
                    </table>
               """
        QMessageBox.information(self, "About", text)

    def about_program(self):
        text = """              
                                                    <p style="text-align: center">
                                                  <table>
                                                     <tr><td>Program name:</td><td>Image processing app</td></tr>
                                                     <tr><td>Version:</td><td>1.0.0</td></tr>
                                                     <tr><td>Icons:</td><td>link</td></tr>
                                                     <tr><td>License:</td><td><a href=''>Apache 2.0</a></td</tr>
                                                     </table>
                                                 """

        QMessageBox.information(self, "About", text)

    def author(self):
        text = """              
                                        <p style="text-align: center">
                                       <table>
                                           <tr><td>Author:</td><td>Volodymyr Parakhonych</td></tr>
                                           <tr><td>GitHub:</td><td><a href='https://github.com/parakhonych'> parakhonych </a></td></tr>
                                           <tr><td>Linkedin:</td><td><a href='https://www.linkedin.com/in/parakhonych/'>parakhonych</a></td></tr>
                                       </table>
                                      """

        QMessageBox.information(self, "Author", text)


if __name__ == '__main__':
    app = QApplication(argv)
    UIWindow = MainWindow()
    UIWindow.show()
    app.exec_()
