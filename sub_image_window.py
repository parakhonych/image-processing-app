from PyQt5.QtWidgets import QLabel, QMdiSubWindow
from PyQt5.QtGui import QPixmap, QImage
from sub_histogram_window import calc_hist_color
FORMATS = {
    1: QImage.Format_Grayscale8
}
import cv2


class Image:
    def __init__(self, window_id, image_name, image_data):
        self.window_id = window_id
        self.name = image_name
        self.data = image_data
        self.gray = self.__is_gray()
        self.sub_window = ImageSubWindow(window_id, image_name, image_data, self.gray)

    def __is_gray(self) -> bool:
        if len(self.data.shape) < 3:
            return True
        elif len(self.data.shape) == 3:
            histogram = calc_hist_color(self.data)
            if (histogram['b'] == histogram['r']).all() and (histogram['r'] == histogram['g']).all():
                self.data = cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
                return True
        return False


class ImageSubWindow(QMdiSubWindow):
    def __init__(self, window_id, image_name, image_data, gray, parent=None):
        super().__init__(parent)
        self.window_id = window_id
        self.label_image = QLabel()
        self.pixmap = None
        self.image_data = image_data
        self.gray = gray
        self.scale = 1
        self.setWidget(self.label_image)
        self.setWindowTitle(image_name)
        self.update_window()

    def update_window(self):
        height, width = self.image_data.shape[:2]
        if self.gray and len(self.image_data.shape) < 3:
            image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        else:
            image = QImage(self.image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.pixmap = self.pixmap.scaled(self.scale * self.pixmap.size())
        self.setFixedSize(self.pixmap.width() + 10, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)
