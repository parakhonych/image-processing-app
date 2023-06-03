from PyQt5.QtWidgets import QDialog
from src.UI.ui_range_slider import UiRangeSlider
from PyQt5.QtGui import QPixmap, QImage
from numpy import zeros_like

FORMATS = {
    1: QImage.Format_Grayscale8
}


class PointOperationThresholding(QDialog, UiRangeSlider):
    def __init__(self, image_data):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Point Operation Thresholding")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data
        self.po_thresholding()
        self.slider_max.valueChanged.connect(self.po_thresholding)

    def update_window(self):
        height, width = self.image_data.shape[:2]
        image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def po_thresholding(self):
        value = self.slider_max.value()
        self.label_max.setText("Max: {0}".format(value))
        img_th = zeros_like(self.image_origin)
        for h in range(self.image_origin.shape[0]):
            for w in range(self.image_origin.shape[1]):
                pixel = self.image_origin[h, w]
                if pixel > value:
                    img_th[h, w] = 1
        self.image_data = img_th*255
        self.update_window()
