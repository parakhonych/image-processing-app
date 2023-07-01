from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QLabel, QVBoxLayout, QDialogButtonBox, QTableWidget, QHBoxLayout, QTableWidgetItem


class UiObjectDetails:
    def setup_ui(self, dialog):
        dialog.resize(289, 72)
        self.cb_objects = QComboBox()
        self.label_image = QLabel()
        self.widget_list = QTableWidget()
        self.widget_list.setColumnCount(2)
        self.widget_list.setRowCount(28)
        self.widget_list.setHorizontalHeaderItem(0, QTableWidgetItem())
        self.widget_list.setHorizontalHeaderItem(1, QTableWidgetItem())

        layout = QVBoxLayout()
        layout.addWidget(self.cb_objects)
        layout_show = QHBoxLayout()
        layout_show.addWidget(self.label_image)
        layout_show.addWidget(self.widget_list)
        layout.addLayout(layout_show)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)