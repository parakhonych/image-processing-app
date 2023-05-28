from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtCore import QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = figure.add_subplot(111)
        super(MplCanvas, self).__init__(figure)


class UiHistogram:
    def setup_ui(self, window):
        self.layout = QVBoxLayout()
        self.plot = MplCanvas(window)
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.layout()

        self.button_all_colors = QPushButton(self)
        self.button_blue = QPushButton(self)
        self.button_green = QPushButton(self)
        self.button_red = QPushButton(self)
        self.button_list = QPushButton(self)

        self.button_all_colors.setAutoDefault(True)
        self.button_blue.setAutoDefault(True)
        self.button_green.setAutoDefault(True)
        self.button_red.setAutoDefault(True)

        self.layout_buttons.addWidget(self.button_all_colors)
        self.layout_buttons.addWidget(self.button_red)
        self.layout_buttons.addWidget(self.button_green)
        self.layout_buttons.addWidget(self.button_blue)
        self.layout_buttons.addWidget(self.button_list)

        self.layout.addWidget(self.plot)
        self.layout.addLayout(self.layout_buttons)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        window.setWidget(self.widget)
        self.__translate_ui(window.name)
        QMetaObject.connectSlotsByName(window)

    def __translate_ui(self, title):
        _translate = QCoreApplication.translate
        self.button_all_colors.setText(_translate(title, "All Colors"))
        self.button_blue.setText(_translate(title, "Blue"))
        self.button_green.setText(_translate(title, "Green"))
        self.button_red.setText(_translate(title, "Red"))
        self.button_list.setText(_translate(title, "List"))


class UiHistogramList:
    def setup_ui(self, window_table):
        self.widget_list = QTableWidget()
        self.widget_list.setColumnCount(2)
        self.widget_list.setRowCount(256)
        for row in range(256):
            self.widget_list.setVerticalHeaderItem(row, QTableWidgetItem())
        self.widget_list.setHorizontalHeaderItem(0, QTableWidgetItem())
        self.widget_list.setHorizontalHeaderItem(1, QTableWidgetItem())
        window_table.setWidget(self.widget_list)
        window_table.resize(230, 450)
