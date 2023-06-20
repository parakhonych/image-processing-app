from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLabel, QVBoxLayout, QDialogButtonBox,QHBoxLayout

class UiUniversalMask(object):
    def setup_ui(self, Dialog):
        Dialog.resize(289, 72)
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        self.spin1 = QtWidgets.QSpinBox()
        self.spin1.setValue(1)
        self.spin1.setMinimum(-100)
        self.spin1.setMaximum(100)
        self.spin2 = QtWidgets.QSpinBox()
        self.spin2.setValue(1)
        self.spin2.setMinimum(-100)
        self.spin2.setMaximum(100)
        self.spin3 = QtWidgets.QSpinBox()
        self.spin3.setValue(1)
        self.spin3.setMinimum(-100)
        self.spin3.setMaximum(100)

        self.spin4 = QtWidgets.QSpinBox()
        self.spin4.setValue(1)
        self.spin4.setMinimum(-100)
        self.spin4.setMaximum(100)
        self.spin5 = QtWidgets.QSpinBox()
        self.spin5.setValue(1)
        self.spin5.setMinimum(-100)
        self.spin5.setMaximum(100)
        self.spin6 = QtWidgets.QSpinBox()
        self.spin6.setValue(1)
        self.spin6.setMinimum(-100)
        self.spin6.setMaximum(100)

        self.spin7 = QtWidgets.QSpinBox()
        self.spin7.setValue(1)
        self.spin7.setMinimum(-100)
        self.spin7.setMaximum(100)
        self.spin8 = QtWidgets.QSpinBox()
        self.spin8.setValue(1)
        self.spin8.setMinimum(-100)
        self.spin8.setMaximum(100)
        self.spin9 = QtWidgets.QSpinBox()
        self.spin9.setValue(1)
        self.spin9.setMinimum(-100)
        self.spin9.setMaximum(100)

        row1.addWidget(self.spin1)
        row1.addWidget(self.spin2)
        row1.addWidget(self.spin3)

        row2.addWidget(self.spin4)
        row2.addWidget(self.spin5)
        row2.addWidget(self.spin6)

        row3.addWidget(self.spin7)
        row3.addWidget(self.spin8)
        row3.addWidget(self.spin9)

        layout = QVBoxLayout()

        self.label_image = QLabel()

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)

        layout.addWidget(self.label_image)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))



