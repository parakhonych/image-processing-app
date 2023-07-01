from PyQt5.QtWidgets import QDialog
from src.UI.ui_object_details import UiObjectDetails, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QImage
from numpy import min, max, zeros_like, uint8
import numpy as np
import cv2

FORMATS = {
    1: QImage.Format_Grayscale8
}


class ObjectDetails(QDialog, UiObjectDetails):
    def __init__(self, image_data):
        super().__init__()
        self.setup_ui(self)
        self.setWindowTitle("Object Details")
        self.pixmap = None
        self.image_data = image_data
        self.image_origin = image_data

        self.objects = self.count_objects()
        self.to_fill()
        self.show()
        self.cb_objects.currentIndexChanged.connect(self.show)

    def to_fill(self):
        for key in range(0, self.objects):
            self.cb_objects.addItem("Object " + str(key))

    def count_objects(self):
        _, thresh = cv2.threshold(self.image_origin, 127, 255, 0)
        self.contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return len(self.contours)

    def update_window(self):
        height, width = self.image_data.shape[:2]
        if len(self.image_data.shape) < 3:
            image = QImage(self.image_data, width, height, width, FORMATS[self.image_data.dtype.itemsize])
        else:
            image = QImage(self.image_data, width, height, 3 * width, QImage.Format_BGR888)
        self.pixmap = QPixmap(image)
        self.setFixedSize(self.pixmap.width() + 320, self.pixmap.height() + 30)
        self.label_image.setPixmap(self.pixmap)

    def show(self):
        self.image_data = cv2.cvtColor(self.image_origin, cv2.COLOR_GRAY2BGR)
        index = int(self.cb_objects.currentText()[-1])
        cnt = self.contours[index]
        cv2.drawContours(self.image_data, [cnt], 0, (0, 0, 255), 3)

        M_img = cv2.moments(cnt)
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        x, y, w, h = cv2.boundingRect(cnt)
        rect_area = w * h
        extent = float(area) / rect_area
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area
        area = cv2.contourArea(cnt)
        equi_diameter = np.sqrt(4 * area / np.pi)
        self.widget_list.setItem(0, 0, QTableWidgetItem('area'))
        self.widget_list.setItem(0, 1, QTableWidgetItem(str(area)))
        self.widget_list.setItem(1, 0, QTableWidgetItem('aspect_ratio'))
        self.widget_list.setItem(1, 1, QTableWidgetItem(str(aspect_ratio)))
        self.widget_list.setItem(2, 0, QTableWidgetItem('extent'))
        self.widget_list.setItem(2, 1, QTableWidgetItem(str(extent)))
        self.widget_list.setItem(3, 0, QTableWidgetItem('solidity'))
        self.widget_list.setItem(3, 1, QTableWidgetItem(str(solidity)))
        self.widget_list.setItem(4, 0, QTableWidgetItem('equi_diameter'))
        self.widget_list.setItem(4, 1, QTableWidgetItem(str(equi_diameter)))

        for i, key in enumerate(M_img.keys()):
            self.widget_list.setItem(i+5, 0, QTableWidgetItem(key))
            self.widget_list.setItem(i+5, 1, QTableWidgetItem(str(M_img[key])))

        self.update_window()

