from PyQt5.QtWidgets import QDialog
from src.UI.ui_combo_boxes import ui_combo_boxes
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np

FORMATS = {
    1: QImage.Format_Grayscale8
}


def laplacian_edge_detection(image_origin, kernel):
    return cv2.Laplacian(image_origin, cv2.CV_8U, kernel)


def sobel_edge_detection(image_origin, kernel):
    sobelx = cv2.Sobel(image_origin, cv2.CV_8U, 1, 0, ksize=kernel)
    sobely = cv2.Sobel(image_origin, cv2.CV_8U, 0, 1, ksize=kernel)
    combined_gradient = cv2.addWeighted(sobelx.astype(np.float32), 0.5, sobely.astype(np.float32), 0.5, 0)
    combined_gradient = np.clip(combined_gradient, 0, 255).astype(np.uint8)
    return combined_gradient

def canny_edge_detection(image_origin, kernel):
    return cv2.Canny(image_origin, 100, 200)


EDGE_DETECTION_FUNCTIONS = {
    "Laplacian": laplacian_edge_detection,
    "Sobel": sobel_edge_detection,
    "Canny": canny_edge_detection
}


class EdgeDetection(QDialog, ui_combo_boxes):
    def __init__(self, image_data):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Edge Detection")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data
        self.fill_combo_boxes()
        self.edge_detection_fun()
        self.comboBoxTypes.currentIndexChanged.connect(self.edge_detection_fun)
        self.comboBoxKernelSize.currentIndexChanged.connect(self.edge_detection_fun)

    def fill_combo_boxes(self):
        for value in EDGE_DETECTION_FUNCTIONS.keys():
            self.comboBoxTypes.addItem(value)
        for value in range(3, 8, 2):
            self.comboBoxKernelSize.addItem(f"{value}")

    def update_window(self):
        height, width = self.image_data.shape[:2]
        if len(self.image_data.shape) < 3:
            image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        else:
            image = QImage(self.image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def edge_detection_fun(self):
        value = int(self.comboBoxKernelSize.currentText())
        self.image_data = EDGE_DETECTION_FUNCTIONS[self.comboBoxTypes.currentText()](self.image_origin, value)
        self.update_window()
