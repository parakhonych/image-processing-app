from PyQt5.QtWidgets import QDialog
from src.UI.ui_range_slider import UiRangeSlider
from PyQt5.QtGui import QPixmap, QImage
from numpy import zeros, zeros_like, arange, round, uint8
import cv2

FORMATS = {
    1: QImage.Format_Grayscale8
}


class PointOperationPosterization(QDialog, UiRangeSlider):
    def __init__(self, image_data, gray):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Point Operation Posterization")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data
        self.gray = gray
        self.slider_max.setMinimum(1)
        self.slider_max.setValue(8)
        self.slider_max.setMaximum(32)
        self.po_posterization()
        self.slider_max.valueChanged.connect(self.po_posterization)

    def update_window(self):
        height, width = self.image_data.shape[:2]
        if len(self.image_data.shape) < 3:
            image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        else:
            image = QImage(self.image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def po_posterization(self):
        value = self.slider_max.value()
        self.label_max.setText("Numbers of bins: {0}".format(value))
        if self.gray:
            bins_table = arange(0, 255, round(255 / value))
            img_out = zeros_like(self.image_origin)
            for h in range(self.image_origin.shape[0]):
                for w in range(self.image_origin.shape[1]):
                    pixel = self.image_origin[h, w]
                    for bin_value in range(value):
                        if pixel > bins_table[bin_value]:
                            img_out[h, w] = bins_table[bin_value]
                    if pixel > bins_table[-1]:
                        img_out[h, w] = 255
            self.image_data = img_out
        else:
            num_levels = value
            lut = zeros((256, 1), dtype=uint8)
            step = 256 // num_levels
            for i in range(256):
                lut[i] = (i // step) * step
            posterized_image = cv2.LUT(self.image_origin, lut)
            self.image_data = posterized_image
        self.update_window()
