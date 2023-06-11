from PyQt5.QtWidgets import QDialog
from src.UI.ui_range_slider import UiRangeSlider
from PyQt5.QtGui import QPixmap, QImage
from numpy import min, max, zeros_like, uint8
import numpy as np
import cv2

FORMATS = {
    1: QImage.Format_Grayscale8
}


def linear_stretch(img, value):
    stretched_channels = [np.zeros_like(channel) for channel in cv2.split(img)]

    for i, channel in enumerate(cv2.split(img)):
        min_val = np.min(channel)
        max_val = np.max(channel)
        stretched_channels[i] = ((channel - min_val) / (max_val - min_val)) * value
    stretched_img = cv2.merge(stretched_channels).astype(np.uint8)

    return stretched_img


class HistogramManipulationStretching(QDialog, UiRangeSlider):
    def __init__(self, image_data):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Stretching")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data
        self.count_stretching()
        self.slider_max.valueChanged.connect(self.count_stretching)

    def update_window(self):
        height, width = self.image_data.shape[:2]
        if len(self.image_data.shape) < 3:
            image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        else:
            image = QImage(self.image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def count_stretching(self):
        value = self.slider_max.value()
        self.label_max.setText("Max: {0}".format(value))
        if len(self.image_origin.shape) < 3:
            image_stretching = linear_stretch(self.image_origin, value)
        else:
            image_stretching = linear_stretch(self.image_origin, value)
        self.image_data = image_stretching
        self.update_window()

