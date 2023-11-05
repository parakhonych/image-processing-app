from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QProgressBar, QPushButton, QVBoxLayout
import numpy as np
import tensorflow as tf
from tensorflow import keras


class WorkerThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, image_matrix1, image_matrix2):
        super().__init__()
        self.source_image = image_matrix1
        self.style_image = image_matrix2
        self.best_image = None
        self.stop_request = False
        self.num_iterations = 100
        self.one_per_cent = self.num_iterations/100

    @staticmethod
    def gram_matrix(tensor):
        flattened = tf.reshape(tensor, shape=[-1, tf.shape(tensor)[-1]])
        gram = tf.matmul(flattened, flattened, transpose_a=True)
        num_pixels = tf.cast(tf.reduce_prod(tf.shape(tensor)[:-1]), tf.float32)
        gram /= num_pixels
        return gram

    def run(self):
        pass


class ProgressDialog(QDialog):
    def __init__(self, image_matrix1, image_matrix2):
        super().__init__()

        self.setWindowTitle("Progress image processing")
        self.setGeometry(100, 100, 300, 120)
        self.best_image = None
        self.layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)
        self.worker_thread = WorkerThread(image_matrix1, image_matrix2)
        self.worker_thread.start()
        self.start_button = QPushButton("Cancel")
        self.start_button.clicked.connect(self.stop_work)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)
        self.worker_thread.progress_signal.connect(self.update_progress)

    def stop_work(self):
        self.worker_thread.stop_request = True
        self.worker_thread.quit()
        self.reject()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value == 100:
            self.best_image = self.worker_thread.best_image
            self.accept()
            self.worker_thread.quit()



