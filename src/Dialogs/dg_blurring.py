from PyQt5.QtWidgets import QDialog
from src.UI.ui_combo_boxes import ui_combo_boxes
from PyQt5.QtGui import QPixmap, QImage
import cv2

FORMATS = {
    1: QImage.Format_Grayscale8
}


def blur(image_origin, kernel):
    return cv2.blur(image_origin, kernel)


def gaussian_blur(image_origin, kernel):
    return cv2.GaussianBlur(image_origin, kernel, 0)


def median_blur(image_origin, kernel):
    return cv2.medianBlur(image_origin, kernel[0])


BLUR_TYPES = {
    "Blur": blur,
    "Gaussian Blur": gaussian_blur,
    "Median Blur": median_blur
}


class Blurring(QDialog, ui_combo_boxes):
    def __init__(self, image_data):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Blurring")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data
        self.fill_combo_boxes()
        self.blurring()
        self.comboBoxTypes.currentIndexChanged.connect(self.blurring)
        self.comboBoxKernelSize.currentIndexChanged.connect(self.blurring)

    def fill_combo_boxes(self):
        for value in BLUR_TYPES.keys():
            self.comboBoxTypes.addItem(value)
        for value in range(3, 10, 2):
            self.comboBoxKernelSize.addItem(f"({value} x {value})")

    def update_window(self):
        height, width = self.image_data.shape[:2]
        image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def blurring(self):
        value = int(self.comboBoxKernelSize.currentText()[1])
        self.image_data = BLUR_TYPES[self.comboBoxTypes.currentText()](self.image_origin, (value, value))
        self.update_window()
