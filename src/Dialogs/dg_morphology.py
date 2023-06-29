from PyQt5.QtWidgets import QDialog
from src.UI.ui_morphology import UIMorphology
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np


def kt_square(i):
    return cv2.getStructuringElement(cv2.MORPH_RECT,(i,i))


def kt_ellipse(i):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (i, i))


def kt_cross(i):
    return cv2.getStructuringElement(cv2.MORPH_CROSS, (i, i))


def kt_diamond(i):
    return np.uint8(np.add.outer(*[np.r_[:i, i:-1:-1]] * 2) >= i)


def erosion(data_img, kernel, border_type):
    return cv2.erode(data_img, kernel, iterations=2, borderType=border_type)


def dilation(data_img, kernel, border_type):
    return cv2.dilate(data_img, kernel, iterations=2, borderType=border_type)


def morph_open(data_img, kernel, border_type):
    return cv2.morphologyEx(data_img, cv2.MORPH_OPEN, kernel, borderType=border_type)


def morph_close(data_img, kernel, border_type):
    return cv2.morphologyEx(data_img, cv2.MORPH_CLOSE, kernel, borderType=border_type)


FORMATS = {
    1: QImage.Format_Grayscale8
}


KERNEL_TYPES = {
    "Square": kt_square,
    "Ellipse": kt_ellipse,
    "Cross": kt_cross,
    "Diamond": kt_diamond,
}

OPERATIONS = {
    "Erode": erosion,
    "Dilate": dilation,
    "Morph Open": morph_open,
    "Morph Close": morph_close,
}
BORDERS = {
    'BORDER_REPLICATE': cv2.BORDER_REPLICATE,
    'BORDER_CONSTANT': cv2.BORDER_CONSTANT,
    'BORDER_REFLECT': cv2.BORDER_REFLECT,
}


class Morphological(QDialog, UIMorphology):
    def __init__(self, image_data):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Morphology")
        self.pixmap = None
        self.origin_data = image_data
        self.fill_combo_boxes()

        self.image_data = image_data
        self.image_name = None
        self.kernel = self.kernel_create()
        self.processing_image()
        self.cB_operations.currentIndexChanged.connect(self.processing_image)
        self.cB_kernel_size.currentIndexChanged.connect(self.kernel_create)
        self.cB_shape_kernel.currentIndexChanged.connect(self.kernel_create)
        self.cB_border_type.currentIndexChanged.connect(self.processing_image)

    def kernel_create(self):
        self.kernel = KERNEL_TYPES[self.cB_shape_kernel.currentText()](int(self.cB_kernel_size.currentText()[0]))
        self.processing_image()

    def fill_combo_boxes(self):
        for key in OPERATIONS.keys():
            self.cB_operations.addItem(key)

        for key in KERNEL_TYPES.keys():
            self.cB_shape_kernel.addItem(key)

        for key in BORDERS.keys():
            self.cB_border_type.addItem(key)

        for key in range(3, 10):
            self.cB_kernel_size.addItem(f"{key} x {key}")

    def update_window(self):
        height, width = self.image_data.shape[:2]
        if len(self.image_data.shape) < 3:
            image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        else:
            image = QImage(self.image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def processing_image(self):
        border_type = BORDERS[self.cB_border_type.currentText()]
        self.image_data = OPERATIONS[self.cB_operations.currentText()](self.origin_data, self.kernel, border_type)
        self.update_window()


