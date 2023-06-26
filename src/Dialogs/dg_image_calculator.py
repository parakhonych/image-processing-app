from PyQt5.QtWidgets import QDialog
from src.UI.ui_image_calculator import UiImageCalculator
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2

FORMATS = {
    1: QImage.Format_Grayscale8
}


def adding(image1, image2):
    return cv2.add(image1, image2)


def blending(image1, image2):
    return cv2.addWeighted(image1, 0.7, image2, 0.5, -100)


def bit_not(image1, image2):
    return cv2.bitwise_not(image1)


def bit_and(image1, image2):
    return cv2.bitwise_and(image1, image2)

def bit_or(image1, image2):
    return cv2.bitwise_or(image1, image2)

def bit_xor(image1, image2):
    return cv2.bitwise_xor(image1, image2)




OPERATIONS = {
    "ADD": adding,
    "BLENDING": blending,
    "NOT": bit_not,
    "AND": bit_and,
    "OR": bit_or,
    "XOR": bit_xor,
}


class ImageCalculator(QDialog, UiImageCalculator):
    def __init__(self, windows):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Image Calculator")
        self.pixmap = None
        self.windows = windows
        self.fill_combo_boxes()
        self.calculation()
        self.image_data = None
        self.image_name = None
        self.cB_image1.currentIndexChanged.connect(self.calculation)
        self.cB_operations.currentIndexChanged.connect(self.calculation)
        self.cB_image2.currentIndexChanged.connect(self.calculation)

    def fill_combo_boxes(self):
        for key in OPERATIONS.keys():
            self.cB_operations.addItem(key)
        for key in self.windows:
            self.cB_image1.addItem(str(key) + " " + self.windows[key].name)
            self.cB_image2.addItem(str(key) + " " + self.windows[key].name)

    def update_window(self):
        height, width = self.image_data.shape[:2]
        if len(self.image_data.shape) < 3:
            image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        else:
            image = QImage(self.image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def calculation(self):
        image1 = self.windows[int(self.cB_image1.currentText()[0])]
        image2 = self.windows[int(self.cB_image2.currentText()[0])]
        operation = self.cB_operations.currentText()

        if image1.gray and image2.gray or not image1.gray and not image2.gray:
            h1, w1 = image1.data.shape[:2]
            h2, w2 = image2.data.shape[:2]
            if h1+w1 > h2+w2:
                image2.data = cv2.resize(image2.data, image1.data.shape[:2])
                self.image_data = OPERATIONS[operation](image1.data, image2.data)
            elif h1+w1 < h2+w2:
                image1.data = cv2.resize(image1.data, image2.data.shape[:2])
                self.image_data = OPERATIONS[operation](image2.data, image1.data)
            else:
                self.image_data = OPERATIONS[operation](image1.data, image2.data)
            self.update_window()

        else:
            self.image_data = image1.data
            self.label_image.setText("Images must be of the same color type")
            self.setFixedSize(300, 150)
            self.label_image.setAlignment(Qt.AlignCenter)


