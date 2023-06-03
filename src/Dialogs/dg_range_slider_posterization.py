from PyQt5.QtWidgets import QDialog
from src.UI.ui_range_slider import UiRangeSlider
from PyQt5.QtGui import QPixmap, QImage
from numpy import zeros_like, arange, round

FORMATS = {
    1: QImage.Format_Grayscale8
}


class PointOperationPosterization(QDialog, UiRangeSlider):
    def __init__(self, image_data):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Point Operation Posterization")
        self.pixmap = None
        self.image_data = image_data
        self.slider_max.setValue(8)
        self.po_posterization()
        self.slider_max.valueChanged.connect(self.po_posterization)

    def update_window(self):
        height, width = self.image_data.shape[:2]
        image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def po_posterization(self):
        value = self.slider_max.value()
        self.label_max.setText("Numbers of bins: {0}".format(value))
        bins_table = arange(0, 255, round(255 / value))
        img_out = zeros_like(self.image_data)
        for h in range(self.image_data.shape[0]):
            for w in range(self.image_data.shape[1]):
                pixel = self.image_data[h, w]
                for bin_value in range(value):
                    if pixel > bins_table[bin_value]:
                        img_out[h, w] = bins_table[bin_value]
                if pixel > bins_table[-1]:
                    img_out[h, w] = 255
        self.image_data = img_out
        self.update_window()
