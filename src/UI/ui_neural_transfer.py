from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox, QHBoxLayout, QComboBox, QPushButton


class UiNeuralTransfer:
    def setup_ui(self, Dialog):
        Dialog.resize(289, 72)
        layout_control = QVBoxLayout()

        layout1 = QHBoxLayout()
        label_text1 = QLabel("Image source")
        label_text2 = QLabel("Style")
        layout1.addWidget(label_text1)
        layout1.addWidget(label_text2)

        layout2 = QHBoxLayout()
        self.cB_image1 = QComboBox()
        self.cB_image2 = QComboBox()
        layout2.addWidget(self.cB_image1)
        layout2.addWidget(self.cB_image2)
        layout_control.addLayout(layout1)
        layout_control.addLayout(layout2)
        layout3 = QHBoxLayout()
        self.label_image1 = QLabel()
        self.label_image2 = QLabel()
        layout3.addWidget(self.label_image1)
        layout3.addWidget(self.label_image2)


        layout = QVBoxLayout()
        layout.addLayout(layout_control)
        layout.addLayout(layout3)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)
