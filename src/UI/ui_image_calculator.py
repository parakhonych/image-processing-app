from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox, QHBoxLayout, QComboBox, QPushButton

class UiImageCalculator:
    def setup_ui(self, Dialog):
        Dialog.resize(289, 72)
        layout_control = QVBoxLayout()

        layout1 = QHBoxLayout()
        label_text1 = QLabel("Image 1")
        label_text2 = QLabel("Operations")
        label_text3 = QLabel("Image 2")
        layout1.addWidget(label_text1)
        layout1.addWidget(label_text2)
        layout1.addWidget(label_text3)

        layout2 = QHBoxLayout()
        self.cB_image1 = QComboBox()
        self.cB_operations = QComboBox()
        self.cB_image2 = QComboBox()
        layout2.addWidget(self.cB_image1)
        layout2.addWidget(self.cB_operations)
        layout2.addWidget(self.cB_image2)


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
