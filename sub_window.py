from PyQt5.QtWidgets import QLabel, QMdiSubWindow
from PyQt5.QtGui import QPixmap, QImage

BYTES_FORMAT = {
    1: QImage.Format_Grayscale8,
    2: QImage.Format_Grayscale16,
}


class Image:
    def __init__(self, window_id, image_name, image_data):
        self.window_id = window_id
        self.name = image_name
        self.data = image_data
        self.gray = self.__is_gray()
        self.sub_window = ImageSubWindow(window_id, image_name, image_data, self.gray)

    def __is_gray(self) -> bool:
        return len(self.data.shape) == 2


class ImageSubWindow(QMdiSubWindow):
    def __init__(self, window_id, image_name, image_data, gray, parent=None):
        super().__init__(parent)
        self.window_id = window_id
        self.label_image = QLabel()
        self.pixmap = None
        self.setWidget(self.label_image)
        self.setWindowTitle(image_name)
        self.update_window(image_data, gray)

    def update_window(self, image_data, gray):
        height, width = image_data.shape[:2]
        if gray:
            pixel_bytes = image_data.dtype.itemsize
            image = QImage(image_data, width, height, width, BYTES_FORMAT[pixel_bytes])
        else:
            image = QImage(image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 20, self.pixmap.height() + 40)
        self.label_image.setPixmap(self.pixmap)
