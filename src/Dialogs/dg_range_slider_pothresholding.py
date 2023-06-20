from PyQt5.QtWidgets import QDialog
from src.UI.ui_range_slider import UiRangeSlider
from PyQt5.QtGui import QPixmap, QImage
from numpy import zeros_like
import cv2

FORMATS = {
    1: QImage.Format_Grayscale8
}


class PointOperationThresholding(QDialog, UiRangeSlider):
    def __init__(self, image_data, gray):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Point Operation Thresholding")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data
        self.gray = gray
        self.po_thresholding()
        self.slider_max.valueChanged.connect(self.po_thresholding)

    def update_window(self):
        height, width = self.image_data.shape[:2]
        if len(self.image_data.shape) < 3:
            image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        else:
            image = QImage(self.image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def po_thresholding(self):
        value = self.slider_max.value()
        self.label_max.setText("Max: {0}".format(value))
        if not self.gray:
            b, g, r = cv2.split(self.image_origin)

            _, b_thresh = cv2.threshold(b, value, 255, cv2.THRESH_TRUNC)
            _, g_thresh = cv2.threshold(g, value, 255, cv2.THRESH_TRUNC)
            _, r_thresh = cv2.threshold(r, value, 255, cv2.THRESH_TRUNC)
            img_th = cv2.merge((b_thresh, g_thresh, r_thresh))
            self.image_data = img_th
        else:
            _, img_th = cv2.threshold(self.image_origin, value, 255, cv2.THRESH_TRUNC)
            self.image_data = img_th
        self.update_window()
