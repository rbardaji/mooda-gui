"""It contains the class DropWidget, that is a pyQT5 widget that show items
in a QListWidget with Checks."""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

from PyQt5.QtWidgets import (QWidget, QLabel, QListWidget, QPushButton,
                             QRadioButton, QSpinBox, QHBoxLayout, QVBoxLayout,
                             QCheckBox)
from PyQt5.QtCore import pyqtSignal, Qt


class DropWidget(QWidget):
    """
    Pyqt5 widget to show items in a QListWidget with Checks. It is used in
    PlotSplitter.
    """
    # Signals
    list2drop = pyqtSignal(list, list, bool)

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        """Layout and main functionality."""
        # Labels
        drop_label = QLabel("Delete parameter")

        # Lists
        self.drop_list = QListWidget(self)

        # Buttons
        apply_drop_button = QPushButton("Apply")
        apply_drop_button.clicked.connect(self.send_labels)
        hide_drop_button = QPushButton("Hide")
        hide_drop_button.clicked.connect(self.hide)

        # Radio buttons
        self.all_radio = QRadioButton("All", self)
        self.all_radio.setChecked(True)
        self.good_radio = QRadioButton("Use QC Flags = 0 and 1", self)
        self.one_radio = QRadioButton("Remove QC flag: ", self)

        # Check box
        self.drop_nan_check = QCheckBox("Drop NaN", self)
        self.drop_nan_check.setChecked(True)

        # Spin inputs
        self.qc_spin_box = QSpinBox(self)
        self.qc_spin_box.setMinimum(0)
        self.qc_spin_box.setMaximum(9)
        self.qc_spin_box.setValue(0)

        # Layout
        # - Horizontal Layout for one_radio -
        h_one = QHBoxLayout()
        h_one.addWidget(self.one_radio)
        h_one.addWidget(self.qc_spin_box)
        # - General layout -
        v_drop = QVBoxLayout()
        v_drop.addWidget(drop_label)
        v_drop.addWidget(self.drop_list)
        v_drop.addWidget(self.all_radio)
        v_drop.addWidget(self.good_radio)
        v_drop.addLayout(h_one)
        v_drop.addWidget(self.drop_nan_check)
        v_drop.addWidget(apply_drop_button)
        v_drop.addWidget(hide_drop_button)
        self.setLayout(v_drop)

    def add_labels(self, labels):
        """Add items to self.drop_list"""
        # Clear the list
        self.drop_list.clear()
        # Add new items
        self.drop_list.addItems(labels)

        # Configure the items checkable
        for index in range(self.drop_list.count()):
            item = self.drop_list.item(index)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

    def send_labels(self):
        """
        It returns the list of checked items from self.drop_list. It also send
        the signal list2drop with the list.

        Returns
        -------
            (labels, flag_list): (list of str, list of int)
                (List with checked labels from self.drop_list, List of flags)
        """
        # Look for checked items and create the list
        labels = []
        for index in range(self.drop_list.count()):
            item = self.drop_list.item(index)
            if item.checkState():
                labels.append(item.text())

        # Flag lists
        flag_list = []
        if self.all_radio.isChecked():
            flag_list = [None]
        elif self.good_radio.isChecked():
            flag_list = [2, 3, 4, 5, 6, 7, 8, 9]
        elif self.one_radio.isChecked():
            flag_list = [self.qc_spin_box.value()]
        # Send the signal
        if labels:
            self.list2drop.emit(labels, flag_list, self.drop_nan_check.isChecked())
        return labels, flag_list
