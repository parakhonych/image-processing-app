from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

class UiRename:
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(289, 72)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 40, 271, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(50, 20, 231, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText("dfsj")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 41, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Title:"))

class Rename(QDialog, UiRename):
    def __init__(self, name, number):
        super().__init__()
        self.setupUi(self)
        self.new_name = name

        self.buttonBox.accepted.connect(self.change_name)
        self.buttonBox.rejected.connect(self.reject)
        if number == 0:
            self.setWindowTitle("Rename")
            self.lineEdit.setText(name)
        else:
            self.setWindowTitle("Duplicate")
            self.lineEdit.setText("Duplicate " + name)

    def change_name(self):

        self.new_name = self.lineEdit.text()
        self.accept()

