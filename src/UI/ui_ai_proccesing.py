import sys
from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
import time
class UiProgressBarDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.progress = 0
        self.progress_bar = QProgressBar(self)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(self.cancel_button)
        self.setLayout(vbox)

        self.timer = QTimer(self)
        #self.timerEvent()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)

        self.setGeometry(100, 100, 300, 100)
        self.setWindowTitle('ProgressBar Example')

    def timerEvent(self):
        if self.progress >= 100:
            self.timer.stop()
        else:
            self.progress += 1
            self.progress_bar.setValue(self.progress)




