from numpy import zeros
from PyQt5.QtWidgets import QMdiSubWindow, QTableWidgetItem
from src.UI.ui_histogram import UiHistogram, UiHistogramList

COLORS = {
    'b': 'blue',
    'g': 'green',
    'r': 'red',
    'black': 'black'
}


def calc_hist_gray(image):
    histogram = zeros(256)
    for height in range(image.shape[0]):
        for weight in range(image.shape[1]):
            pixel = image[height, weight]
            histogram[pixel] += 1
    return {'black': histogram}


def calc_hist_color(image):
    histogram = [zeros(256), zeros(256), zeros(256)]
    for i in range(image.shape[0]):
        for k in range(image.shape[1]):
            for j in range(image.shape[2]):
                pixel = image[i][k][j]
                histogram[j][pixel] += 1

    return {'b': histogram[0], 'g': histogram[1], 'r': histogram[2]}


class SubHistogram(QMdiSubWindow, UiHistogram):
    def __init__(self, window_id, image, *args, **kwargs):
        super(SubHistogram, self).__init__(*args, **kwargs)
        self.name = "Histogram of " + image.name
        self.setup_ui(self)
        self.setWindowTitle(self.name)
        self.window_id = window_id
        self.image = image
        self.histogram_list = SubHistogramList(self.window_id + 1)

        if self.image.gray:
            self.button_all_colors.setEnabled(False)
            self.button_blue.setEnabled(False)
            self.button_green.setEnabled(False)
            self.button_red.setEnabled(False)
            self.histogram = calc_hist_gray(image.data)
            self.show_single_channel(self.histogram, 'black')
        else:
            self.histogram = calc_hist_color(image.data)
            self.show_all_channel(self.histogram)
            self.button_all_colors.pressed.connect(lambda: self.show_all_channel(self.histogram))
            self.button_blue.pressed.connect(lambda: self.show_single_channel(self.histogram, 'b'))
            self.button_red.pressed.connect(lambda: self.show_single_channel(self.histogram, 'r'))
            self.button_green.pressed.connect(lambda: self.show_single_channel(self.histogram, 'g'))
        self.button_list.pressed.connect(lambda: self.show_histogram_list(self.histogram, image))

    def show_all_channel(self, histogram):
        self.plot.axes.clear()
        for color in histogram.keys():
            self.plot.axes.bar(range(256), histogram[color], color=COLORS[color])
        self.plot.draw()

    def show_single_channel(self, histogram, color):
        self.plot.axes.clear()
        self.plot.axes.bar(range(256), histogram[color], color=COLORS[color])
        self.plot.draw()

    def show_histogram_list(self, histogram, image):
        if image.gray:
            self.histogram_list.calc_histogram_list(histogram['black'], image.name)
        else:
            maximum = [max(i) for i in zip(*histogram.values())]
            self.histogram_list.calc_histogram_list(maximum, image.name)
        self.histogram_list.show()


class SubHistogramList(QMdiSubWindow, UiHistogramList):
    def __init__(self, window_id, *args, **kwargs):
        super(SubHistogramList, self).__init__(*args, **kwargs)
        self.window_id = window_id

    def calc_histogram_list(self, histogram, name):
        self.setWindowTitle("Histogram list of " + name)
        self.setup_ui(self)
        header_number = self.widget_list.horizontalHeaderItem(0)
        header_count = self.widget_list.horizontalHeaderItem(1)
        for value, count in enumerate(histogram):
            self.widget_list.setItem(value, 0, QTableWidgetItem(str(value)))
            self.widget_list.setItem(value, 1, QTableWidgetItem(str(count)))
        header_number.setText("Nr")
        header_count.setText("Count")
