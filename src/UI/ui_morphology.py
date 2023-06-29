from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox, QHBoxLayout, QComboBox, QPushButton


class UIMorphology:
    def setup_ui(self, Dialog):
        Dialog.resize(289, 72)
        layout_control = QVBoxLayout()

        layout1 = QHBoxLayout()
        label_text1 = QLabel("Operation:")
        self.cB_operations = QComboBox()
        label_text2 = QLabel("Shape of Kernel:")
        self.cB_shape_kernel = QComboBox()

        layout1.addWidget(label_text1)
        layout1.addWidget(self.cB_operations)
        layout1.addWidget(label_text2)
        layout1.addWidget(self.cB_shape_kernel)

        layout2 = QHBoxLayout()
        label_text3 = QLabel("Border Type:")
        self.cB_border_type = QComboBox()
        label_text4 = QLabel("Kernel size:")
        self.cB_kernel_size = QComboBox()

        layout2.addWidget(label_text3)
        layout2.addWidget(self.cB_border_type)
        layout2.addWidget(label_text4)
        layout2.addWidget(self.cB_kernel_size)

        layout_control.addLayout(layout1)
        layout_control.addLayout(layout2)

        self.label_image = QLabel()

        layout = QVBoxLayout()
        layout.addLayout(layout_control)
        layout.addWidget(self.label_image)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)
