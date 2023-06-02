from PyQt5.QtWidgets import QDialog
from ui_range_slider import UiRangeSlider
from PyQt5.QtGui import QPixmap, QImage
from numpy import min, max, zeros_like

FORMATS = {
    1: QImage.Format_Grayscale8
}


class HistogramManipulationStretching(QDialog, UiRangeSlider):
    def __init__(self, image_data):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Stretching")
        self.pixmap = None
        self.image_data = image_data
        self.count_stretching()
        self.slider_max.valueChanged.connect(self.count_stretching)

    def update_window(self):
        height, width = self.image_data.shape[:2]
        image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def count_stretching(self):
        value = self.slider_max.value()
        self.label_max.setText("Max: {0}".format(value))
        image_min = min(self.image_data)
        image_max = max(self.image_data)
        image_stretching = zeros_like(self.image_data)
        for h in range(self.image_data.shape[0]):
            for w in range(self.image_data.shape[1]):
                pixel = self.image_data[h, w]
                image_stretching[h, w] = ((pixel - image_min) * value) / (image_max - image_min)
        self.image_data = image_stretching
        self.update_window()

