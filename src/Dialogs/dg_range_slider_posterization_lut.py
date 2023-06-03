from PyQt5.QtWidgets import QDialog
from src.UI.ui_range_slider import UiRangeSlider
from PyQt5.QtGui import QPixmap, QImage
from numpy import round, ones, hstack, arange

FORMATS = {
    1: QImage.Format_Grayscale8
}


class PointOperationPosterizationLut(QDialog, UiRangeSlider):
    def __init__(self, image_data):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Point Operation Posterization LUT")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data
        self.slider_max.setMinimum(1)
        self.slider_max.setValue(8)
        self.slider_max.setMaximum(32)
        self.po_posterization_lut()
        self.slider_max.valueChanged.connect(self.po_posterization_lut)

    def update_window(self):
        height, width = self.image_data.shape[:2]
        image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def po_posterization_lut(self):
        value = self.slider_max.value()
        self.label_max.setText("Numbers of bins: {0}".format(value))
        bin_length = round(255 / value).astype(int)
        bins_table = arange(0, 255, round(255 / value))
        lut = []
        for bin in range(value):
            temp = ones(bin_length, ) * bins_table[bin]
            lut = hstack((lut, temp))
        lut = hstack((lut, ones(bin_length, ) * 255))
        img_out = lut[self.image_origin].astype('uint8')

        self.image_data = img_out
        self.update_window()
