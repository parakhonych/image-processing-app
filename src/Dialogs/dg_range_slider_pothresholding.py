from PyQt5.QtWidgets import QDialog
from src.UI.ui_range_slider_thresholding import UiRangeSliderThresholding
from PyQt5.QtGui import QPixmap, QImage
import cv2

FORMATS = {
    1: QImage.Format_Grayscale8
}

OPERATIONS = {
    'Thresholding': 1,
    'Adaptive Thresholding': 2,
    "Otsu thresholding": 3,
}


def threshold_single_channel(channel, value, adaptive_method):
    _, channel_thresh = cv2.threshold(channel, value, 255, adaptive_method)
    return channel_thresh


def threshold_channels(image, value, adaptive_method):
    b, g, r = cv2.split(image)



class PointOperationThresholding(QDialog, UiRangeSliderThresholding):
    def __init__(self, image_data, gray):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Thresholding")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data
        self.gray = gray
        self.fill_combo_boxes()
        self.po_thresholding()
        self.cB_operations.currentIndexChanged.connect(self.po_thresholding)
        self.slider_max.valueChanged.connect(self.po_thresholding)
        #self.cb_block_size.currentIndexChanged.connect(self.po_thresholding)
        self.cb_block_size.valueChanged.connect(self.po_thresholding)

    def fill_combo_boxes(self):
        for key in OPERATIONS.keys():
            self.cB_operations.addItem(key)


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
        self.label_max.setText("Threshold: {0}".format(value))
        number_operation = OPERATIONS[self.cB_operations.currentText()]
        if not self.gray:
            b, g, r = cv2.split(self.image_origin)
            if number_operation == 1:
                self.cb_block_size.setEnabled(False)
                self.image_data = cv2.merge((threshold_single_channel(b, value, cv2.THRESH_BINARY),
                                            threshold_single_channel(g, value, cv2.THRESH_BINARY),
                                            threshold_single_channel(r, value, cv2.THRESH_BINARY)))
            elif number_operation == 2:
                self.cb_block_size.setEnabled(True)
                b_size = self.cb_block_size.value()
                if b_size % 2 == 0:
                    b_size = b_size + 1
                    self.cb_block_size.setValue(b_size)
                b_thresh = cv2.adaptiveThreshold(b, value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, b_size, 5)
                g_thresh = cv2.adaptiveThreshold(g, value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, b_size, 5)
                r_thresh = cv2.adaptiveThreshold(r, value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, b_size, 5)
                self.image_data = cv2.merge((b_thresh, g_thresh, r_thresh))
            elif number_operation == 3:
                self.cb_block_size.setEnabled(False)
                _, b_thresh = cv2.threshold(b, 0, value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                _, g_thresh = cv2.threshold(g, 0, value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                _, r_thresh = cv2.threshold(r, 0, value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                self.image_data = cv2.merge((b_thresh, g_thresh, r_thresh))
        else:
            if number_operation == 1:
                self.cb_block_size.setEnabled(False)
                _, self.image_data = cv2.threshold(self.image_origin, value, 255, cv2.THRESH_BINARY)
            elif number_operation == 2:
                self.cb_block_size.setEnabled(True)
                b_size = self.cb_block_size.value()
                if b_size % 2 == 0:
                    b_size = b_size + 1
                    self.cb_block_size.setValue(b_size)
                self.image_data = cv2.adaptiveThreshold(self.image_origin, value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                        cv2.THRESH_BINARY, b_size, 5)
            elif number_operation == 3:
                self.cb_block_size.setEnabled(False)
                _, self.image_data = cv2.threshold(self.image_origin, 0, value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.update_window()
