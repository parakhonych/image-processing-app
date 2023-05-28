from PyQt5.QtWidgets import QDialog
from ui_text_input import UiTextInput


class TextInput(QDialog, UiTextInput):
    def __init__(self, name, text):
        super().__init__()
        self.setupUi(self)
        self.new_name = name
        self.buttonBox.accepted.connect(self.change_name)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle(text)
        self.lineEdit.setText(name)

    def change_name(self):
        self.new_name = self.lineEdit.text()
        self.accept()

