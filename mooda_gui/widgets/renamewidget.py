"""Module to create a Widget"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox,
                             QLineEdit, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import pyqtSignal


class RenameWidget(QWidget):
    """Widget to rename keys from a WaterFrame"""
    # Signals
    key2change = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        """Layout and main functionalities of the Widget"""
        # Labels
        rename_label = QLabel("Rename:")
        to_label = QLabel("to")

        # ComboBox
        self.key_combo_box = QComboBox()

        # Line edit
        self.new_name_line_edit = QLineEdit()

        # Buttons
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.send_labels)
        hide_button = QPushButton("Hide")
        hide_button.clicked.connect(self.hide)

        # Layouts
        # - Horizontal for rename
        h_rename = QHBoxLayout()
        h_rename.addWidget(self.key_combo_box)
        h_rename.addWidget(to_label)
        h_rename.addWidget(self.new_name_line_edit)
        h_rename.addStretch()
        # - Vertical for self
        v_widget = QVBoxLayout()
        v_widget.addWidget(rename_label)
        v_widget.addLayout(h_rename)
        v_widget.addWidget(apply_button)
        v_widget.addWidget(hide_button)
        self.setLayout(v_widget)

    def add_labels(self, labels):
        """Add items to self.dropList"""
        # Clear the ComboBox
        self.key_combo_box.clear()
        # Clear the input box
        self.new_name_line_edit.clear()
        # Add new items
        self.key_combo_box.addItems(labels)

    def send_labels(self):
        """Emit a signal with the name of parameters to change"""
        if self.new_name_line_edit.text():
            self.key2change.emit(self.key_combo_box.currentText(),
                                 self.new_name_line_edit.text())
