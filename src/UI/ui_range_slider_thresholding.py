from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLabel, QVBoxLayout, QDialogButtonBox, QComboBox, QHBoxLayout, QSpinBox


class UiRangeSliderThresholding:
    def setup_ui(self, Dialog):
        Dialog.resize(289, 72)
        self.slider_max = QSlider(Qt.Horizontal)
        self.slider_max.setMinimum(0)
        self.slider_max.setMaximum(255)
        self.slider_max.setValue(127)


        self.label_max = QLabel()
        self.label_max.setText("Thresholding: 127")
        self.label_image = QLabel()

        self.cB_operations = QComboBox()
        self.empty_label1 = QLabel("Block Size: ")
        self.empty_label1.setAlignment(Qt.AlignCenter)
        self.cb_block_size = QSpinBox()
        self.cb_block_size.setMinimum(3)
        self.cb_block_size.setMaximum(255)
        self.cb_block_size.setValue(11)
        self.cb_block_size.setSingleStep(2)

        layout = QVBoxLayout()
        layout_box = QHBoxLayout()
        layout_box.addWidget(self.cB_operations)
        layout_box.addWidget(self.empty_label1)
        layout_box.addWidget(self.cb_block_size)
        layout.addLayout(layout_box)

        layout.addWidget(self.slider_max)
        layout.addWidget(self.label_max)
        layout.addWidget(self.label_image)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

