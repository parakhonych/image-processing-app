import matplotlib.pyplot as plt
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QProgressBar, QPushButton, QVBoxLayout
import numpy as np
import tensorflow as tf
from tensorflow import keras


def count_gram_matrix(tensor):
    flattened = tf.reshape(tensor, shape=[-1, tf.shape(tensor)[-1]])
    gram = tf.matmul(flattened, flattened, transpose_a=True)
    num_pixels = tf.cast(tf.reduce_prod(tf.shape(tensor)[:-1]), tf.float32)
    gram /= num_pixels
    return gram


class WorkerThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, image_matrix1, image_matrix2):
        super().__init__()
        self.source_image = image_matrix1
        self.style_image = image_matrix2
        self.best_image = None
        self.stop_request = False
        self.epoch = 1000
        self.one_per_cent = self.epoch / 100

    def run(self):
        vgg19 = keras.applications.vgg19.VGG19(include_top=False, weights='imagenet')
        vgg19.trainable = False

        content_layer = 'block5_conv4'

        list_style_layers = ['block1_conv1', 'block1_conv2',
                             'block2_conv1', 'block2_conv2',
                             'block3_conv1', 'block3_conv2', 'block3_conv3', 'block3_conv4',
                             'block4_conv1', 'block4_conv2', 'block4_conv3', 'block4_conv4',
                             'block5_conv1', 'block5_conv2', 'block5_conv3']

        count_list_of_style_layers = len(list_style_layers)
        outputs = [vgg19.get_layer(elem).output for elem in list_style_layers] + [vgg19.get_layer(content_layer).output]
        model = keras.models.Model(vgg19.input, outputs)
        for layer in model.layers:
            layer.trainable = False

        alpha = 1000
        beta = 0.01

        processed_image_content = keras.applications.vgg19.preprocess_input(np.expand_dims(self.source_image, axis=0))
        processed_image_style = keras.applications.vgg19.preprocess_input(np.expand_dims(self.style_image, axis=0))

        map_style_features = [layer[0] for layer in model(processed_image_style)[:count_list_of_style_layers]]
        map_content_features = [layer[0] for layer in model(processed_image_content)[count_list_of_style_layers:]]

        gram_matrix_style_image = [count_gram_matrix(style_feature) for style_feature in map_style_features]

        working_image = tf.Variable(np.copy(processed_image_content), dtype=tf.float32)

        opt = tf.compat.v1.train.AdamOptimizer(learning_rate=2, beta1=0.99, epsilon=1e-1)
        j_min = float('inf')
        min_values = -np.array([103.939, 116.779, 123.68])
        max_values = 255 - np.array([103.939, 116.779, 123.68])

        for i in range(1, self.epoch):
            if self.stop_request:
                break
            with tf.GradientTape() as tape:
                target_image_features = model(working_image)

                style_target_image_features = target_image_features[:count_list_of_style_layers]
                content_target_image_features = target_image_features[count_list_of_style_layers:]

                j_style = 0
                j_content = 0

                # Count loss in style
                lambda_j_s = 1.0 / float(count_list_of_style_layers)
                for G_S, G_P in zip(gram_matrix_style_image, style_target_image_features):
                    j_style += lambda_j_s * tf.reduce_mean(tf.square(count_gram_matrix(G_P[0]) - G_S))

                # Count loss in content
                lambda_j_c = 1.0
                j_content += lambda_j_c * tf.reduce_mean(
                    tf.square(content_target_image_features[0] - map_content_features))

                j_style *= beta
                j_content *= alpha

                j_main = j_style + j_content

            grads = tape.gradient(j_main, working_image)
            opt.apply_gradients([(grads, working_image)])
            clipped = tf.clip_by_value(working_image, min_values, max_values)
            working_image.assign(clipped)
            if j_main < j_min:
                j_min = j_main
                self.best_image = working_image
                print(f'iter {i}')

            per_cent = int(i // self.one_per_cent)
            self.progress_signal.emit(per_cent)


        self.best_image = np.squeeze(self.best_image.numpy(), 0)
        self.best_image[:, :, 0] += 103.939
        self.best_image[:, :, 1] += 116.779
        self.best_image[:, :, 2] += 123.68
        self.best_image = np.clip(self.best_image, 0, 255).astype('uint8')

        self.progress_signal.emit(100)
        self.finished.emit()


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
