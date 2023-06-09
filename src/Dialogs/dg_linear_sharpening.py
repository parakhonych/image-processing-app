from PyQt5.QtWidgets import QDialog
from src.UI.ui_combo_boxes_mask_lap import UIComboBoxSharpening
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np

FORMATS = {
    1: QImage.Format_Grayscale8
}


MASK = {
    "Mask Sharpening 1": np.array([[ 0,-1, 0],[-1, 5,-1],[ 0,-1, 0]]),
    "Mask Sharpening 2": np.array([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]]),
    "Mask Sharpening 3": np.array([[ 1,-2, 1],[-2, 5,-2],[ 1,-2, 1]])
}


class LinearSharpening(QDialog, UIComboBoxSharpening):
    def __init__(self, image_data):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Linear Sharpening")
        self.labelType.setText("Choose mask")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data
        self.fill_combo_boxes()
        self.linear_sharpening_action()
        self.comboBoxTypes.currentIndexChanged.connect(self.linear_sharpening_action)


    def fill_combo_boxes(self):
        for value in MASK.keys():
            self.comboBoxTypes.addItem(value)


    def update_window(self):
        height, width = self.image_data.shape[:2]
        if len(self.image_data.shape) < 3:
            image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        else:
            image = QImage(self.image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def linear_sharpening_action(self):
        current_mask = MASK.get(self.comboBoxTypes.currentText())
        show_mask = ""
        for row in range(3):
            for col in range(3):
               show_mask = show_mask + " " + str(current_mask[row, col]) + " "
            show_mask = show_mask + "\n"
        self.label_kernel_size.setText(show_mask)
        self.image_data = cv2.filter2D(self.image_origin, cv2.CV_8U, current_mask, borderType = cv2.BORDER_REPLICATE)

        self.update_window()
