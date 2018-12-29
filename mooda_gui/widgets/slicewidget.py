"""Widget module"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QDateTimeEdit,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import pyqtSignal


class SliceWidget(QWidget):
    """Custom widget to slice data"""
    # Signals
    sliceTimes = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        """Layout and main functionalities"""

        # Labels
        slice_label = QLabel("Slicing")
        start_label = QLabel("Start: ")
        end_label = QLabel("End: ")

        # DateTimeEdit
        self.start_date_time_edit = QDateTimeEdit()
        self.end_date_time_edit = QDateTimeEdit()

        # Buttons
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.send_times)
        hide_button = QPushButton("Hide")
        hide_button.clicked.connect(self.hide)

        # Layouts
        # - Horizontal for start
        h_start = QHBoxLayout()
        h_start.addWidget(start_label)
        h_start.addWidget(self.start_date_time_edit)
        # - Horizontal for end
        h_end = QHBoxLayout()
        h_end.addWidget(end_label)
        h_end.addWidget(self.end_date_time_edit)

        # - Vertical for self
        v_widget = QVBoxLayout()
        v_widget.addWidget(slice_label)
        v_widget.addLayout(h_start)
        v_widget.addLayout(h_end)
        v_widget.addWidget(apply_button)
        v_widget.addWidget(hide_button)
        self.setLayout(v_widget)

    def send_times(self):
        """It emits a signal with start and end dates"""
        debug = True
        if debug:
            print("- In SliceWidget.send_times()")

        start = self.start_date_time_edit.dateTime()
        end = self.end_date_time_edit.dateTime()
        start_string = start.toString("yyyyMMddhhmmss")
        end_string = end.toString("yyyyMMddhhmmss")

        if debug:
            print("sliceTimes emit:", start_string, end_string)

        self.sliceTimes.emit(start_string, end_string)

    def refresh(self, start, end):
        """It refresh the parameters of self.start_date_time_edit and
        self.end_date_time_edit"""
        self.start_date_time_edit.setMinimumDateTime(start)
        self.start_date_time_edit.setMaximumDateTime(end)
        self.start_date_time_edit.setDateTime(start)
        self.end_date_time_edit.setMinimumDateTime(start)
        self.end_date_time_edit.setMaximumDateTime(end)
        self.end_date_time_edit.setDateTime(end)
