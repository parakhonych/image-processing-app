from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from src.UI.ui_neural_transfer import UiNeuralTransfer
from PyQt5.QtGui import QPixmap, QImage
from src.UI.ui_ai_proccesing import ProgressDialog
import cv2


FORMATS = {
    1: QImage.Format_Grayscale8
}


class NeuralTransfer(QDialog, UiNeuralTransfer):
    def __init__(self, windows):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Image Calculator")
        self.pixmap1 = None
        self.pixmap2 = None
        self.windows = windows
        self.fill_combo_boxes()
        self.calculation()
        self.image_data1 = None
        self.image_data2 = None
        self.image_name = None
        self.image_result = None
        self.calculation()
        self.cB_image1.currentIndexChanged.connect(self.calculation)
        self.cB_image2.currentIndexChanged.connect(self.calculation)
        self.buttons.accepted.connect(self.transfer)
        self.buttons.rejected.connect(self.reject)

    def fill_combo_boxes(self):
        for key in self.windows:
            self.cB_image1.addItem(str(key) + " " + self.windows[key].name)
            self.cB_image2.addItem(str(key) + " " + self.windows[key].name)

    def update_window(self):
        height, width = self.image_data1.shape[:2]
        if len(self.image_data1.shape) < 3:
            image = QImage(self.image_data1, width, height, width, FORMATS[self.image_data1.dtype.itemsize])
        else:
            image = QImage(self.image_data1, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap1 = QPixmap(image)
        self.label_image1.setPixmap(self.pixmap1)

        height, width = self.image_data2.shape[:2]
        if len(self.image_data2.shape) < 3:
            image = QImage(self.image_data2, width, height, width, FORMATS[self.image_data2.dtype.itemsize])
        else:
            image = QImage(self.image_data2, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap2 = QPixmap(image)
        self.setFixedSize(self.pixmap1.width() + self.pixmap2.width() + 10, self.pixmap2.height() + 30)
        self.label_image2.setPixmap(self.pixmap2)

    def calculation(self):
        image_data1 = self.windows[int(self.cB_image1.currentText()[0])].data
        image_data2 = self.windows[int(self.cB_image2.currentText()[0])].data
        self.image_name = self.cB_image1.currentText()[2:]
        if image_data1.shape[:2] == (224, 224) and image_data2.shape[:2] == (224, 224):
            self.image_data1 = image_data1
            self.image_data2 = image_data2
            self.update_window()
            self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.label_image1.setText("The picture must have a size of 224x224")
            self.label_image2.setText("Use the resize function")
            self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)

    def transfer(self):
        source_image = cv2.cvtColor(self.image_data1, cv2.COLOR_BGR2RGB)
        style_image = cv2.cvtColor(self.image_data2, cv2.COLOR_BGR2RGB)
        style_transfer = ProgressDialog(source_image, style_image)
        if style_transfer.exec_():
            self.image_result = style_transfer.best_image
            self.accept()

