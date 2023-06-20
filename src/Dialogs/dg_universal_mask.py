from PyQt5.QtWidgets import QDialog
from src.UI.ui_universal_mask import UiUniversalMask
from PyQt5.QtGui import QPixmap, QImage
import cv2
from numpy import zeros, int64, sum

FORMATS = {
    1: QImage.Format_Grayscale8
}

class UniversalMask(QDialog, UiUniversalMask):
    def __init__(self, image_data, gray):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Universal Mask")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data
        self.gray = gray
        self.apply_mask()
        self.spin1.valueChanged.connect(self.apply_mask)
        self.spin2.valueChanged.connect(self.apply_mask)
        self.spin3.valueChanged.connect(self.apply_mask)
        self.spin4.valueChanged.connect(self.apply_mask)
        self.spin5.valueChanged.connect(self.apply_mask)
        self.spin6.valueChanged.connect(self.apply_mask)
        self.spin7.valueChanged.connect(self.apply_mask)
        self.spin8.valueChanged.connect(self.apply_mask)
        self.spin9.valueChanged.connect(self.apply_mask)
        self.buttons.accepted.connect(self.accept)

    def update_window(self):
        height, width = self.image_data.shape[:2]
        if len(self.image_data.shape) < 3:
            image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        else:
            image = QImage(self.image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def apply_mask(self):
        kernel = zeros((3, 3))
        kernel[0, 0] = self.spin1.value()
        kernel[0, 1] = self.spin2.value()
        kernel[0, 2] = self.spin3.value()

        kernel[1, 0] = self.spin4.value()
        kernel[1, 1] = self.spin5.value()
        kernel[1, 2] = self.spin6.value()

        kernel[2, 0] = self.spin7.value()
        kernel[2, 1] = self.spin8.value()
        kernel[2, 2] = self.spin9.value()

        kernel = int64(kernel) / sum(kernel)

        img_filtered = cv2.filter2D(self.image_origin, cv2.CV_8U, kernel, borderType=cv2.BORDER_REPLICATE)
        self.image_data = img_filtered
        self.update_window()
