"""It contains the QC Widget"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

from PyQt5.QtWidgets import (QWidget, QLabel, QListWidget, QPushButton,
                             QSpinBox, QHBoxLayout, QVBoxLayout, QCheckBox,
                             QDoubleSpinBox)
from PyQt5.QtCore import pyqtSignal, Qt


class QCWidget(QWidget):
    """QC Preferences Widget"""

    # Signals
    list2qc = pyqtSignal(list)

    def __init__(self):
        """Constructor"""

        super().__init__()

        self.init_ui()

    def init_ui(self):
        """Layout and main functionalities"""

        # Labels
        qc_label = QLabel("QC procedures")
        reset_label = QLabel("Reset QC: ")
        to_label = QLabel("->")
        bad_range_label = QLabel("- Bad QC: ")
        bad_flat_label = QLabel("- Bad QC: ")
        bad_spike_label = QLabel("- Bad QC: ")
        rolling_label = QLabel("Rolling window: ")
        threshold_label = QLabel("Threshold: ")
        parameter_label = QLabel("Parameters: ")

        # Lists
        self.key_list = QListWidget(self)
        self.key_list.setEnabled(False)

        # Check Box
        self.reset_check = QCheckBox("Reset QC", self)
        self.reset_check.setChecked(True)
        self.range_check = QCheckBox("Range test", self)
        self.range_check.setChecked(True)
        self.flat_check = QCheckBox("Flat test", self)
        self.flat_check.setChecked(True)
        self.spike_check = QCheckBox("Spike test", self)
        self.spike_check.setChecked(True)
        self.flag2flag_check = QCheckBox("Change flags", self)
        self.flag2flag_check.setChecked(True)
        self.all_check = QCheckBox("All", self)
        self.all_check.setChecked(True)
        self.all_check.toggled.connect(self.key_list.setDisabled)

        # Spin box
        self.original_spin_box = QSpinBox(self)
        self.original_spinBox.setMinimum(0)
        self.original_spin_box.setMaximum(9)
        self.original_spin_box.setValue(0)
        # -
        self.translated_spin_box = QSpinBox(self)
        self.translated_spin_box.setMinimum(0)
        self.translated_spin_box.setMaximum(9)
        self.translated_spin_box.setValue(1)
        # -
        self.bad_range_spin_box = QSpinBox(self)
        self.bad_range_spin_box.setMinimum(0)
        self.bad_range_spin_box.setMaximum(9)
        self.bad_range_spin_box.setMinimum(0)
        self.bad_range_spin_box.setValue(4)
        # -
        self.flat_spin_box = QSpinBox(self)
        self.flat_spin_box.setMinimum(0)
        self.flat_spin_box.setMaximum(9)
        self.flat_spin_box.setMinimum(0)
        self.flat_spin_box.setValue(4)
        # -
        self.spike_spin_box = QSpinBox(self)
        self.spike_spin_box.setMinimum(0)
        self.spike_spin_box.setMaximum(9)
        self.spike_spin_box.setMinimum(0)
        self.spike_spin_box.setValue(4)
        # -
        self.rolling_spin_box = QSpinBox(self)
        self.rolling_spin_box.setValue(0)
        self.rolling_spin_box.setToolTip(
            "Size of the moving window.\n"
            "This is the number of observations used for calculating"
            " the mean.\n0 = Auto")
        # -
        self.reset_spin_box = QSpinBox(self)
        self.reset_spin_box.setMinimum(0)
        self.reset_spin_box.setMaximum(9)
        self.reset_spin_box.setMinimum(0)
        self.reset_spin_box.setValue(0)
        # -
        self.threshold_spin_box = QDoubleSpinBox(self)
        self.threshold_spin_box.setValue(2.00)
        self.threshold_spin_box.setToolTip(
            "Maximum difference between the value analyzed and the average of"
            " the rolling window.")

        # Button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply)
        close_button = QPushButton("Hide")
        close_button.clicked.connect(self.hide)

        # Layouts
        # - Horizontal Layout for reset
        h_reset = QHBoxLayout()
        h_reset.addWidget(reset_label)
        h_reset.addWidget(self.reset_spin_box)
        h_reset.addStretch()
        # - Horizontal Layout for ranges
        hRanges = QHBoxLayout()
        hRanges.addWidget(bad_range_label)
        hRanges.addWidget(self.bad_range_spin_box)
        hRanges.addStretch()
        # hRanges.addStretch()
        # - Horizontal Layout for flat
        hFlat = QHBoxLayout()
        hFlat.addWidget(bad_flat_label)
        hFlat.addWidget(self.flat_spin_box)
        hFlat.addStretch()
        # hFlat.addStretch()
        # - Horizontal Layout for spikes
        h_spikes = QHBoxLayout()
        h_spikes.addWidget(bad_spike_label)
        h_spikes.addWidget(self.spike_spin_box)
        h_spikes.addStretch()
        # - Horizontal Layout for threshold
        hThreshold = QHBoxLayout()
        hThreshold.addWidget(threshold_label)
        hThreshold.addWidget(self.threshold_spin_box)
        hThreshold.addStretch()
        # - Horizontal Layout for rolling window
        hRolling = QHBoxLayout()
        hRolling.addWidget(rolling_label)
        hRolling.addWidget(self.rolling_spin_box)
        hRolling.addStretch()
        # - Horizontal Layout for flag2flag -
        hFlag2flag = QHBoxLayout()
        hFlag2flag.addWidget(self.original_spin_box)
        hFlag2flag.addWidget(to_label)
        hFlag2flag.addWidget(self.translated_spin_box)
        hFlag2flag.addStretch()
        # - Vertical Layout for the Widget
        vQC = QVBoxLayout()
        vQC.addWidget(parameter_label)
        vQC.addWidget(self.all_check)
        vQC.addWidget(self.key_list)
        vQC.addWidget(qc_label)
        vQC.addWidget(self.reset_check)
        vQC.addLayout(h_reset)
        vQC.addWidget(self.range_check)
        vQC.addLayout(hRanges)
        vQC.addWidget(self.flat_check)
        vQC.addLayout(hFlat)
        vQC.addWidget(self.spike_check)
        vQC.addLayout(h_spikes)
        vQC.addLayout(hThreshold)
        vQC.addLayout(hRolling)
        vQC.addWidget(self.flag2flag_check)
        vQC.addLayout(hFlag2flag)
        vQC.addWidget(apply_button)
        vQC.addWidget(close_button)
        vQC.addStretch()
        self.setLayout(vQC)

    def apply(self):
        """
        Emit a signal with the current QC settings
        """
        settings = []
        if self.reset_check.isChecked():
            settings.append(self.reset_spin_box.text())
        else:
            settings.append(None)
        if self.rangeCheck.isChecked():
            settings.append(self.bad_range_spin_box.text())
        else:
            settings.append(None)
        if self.flat_check.isChecked():
            settings.append(self.flat_spin_box.text())
        else:
            settings.append(None)
        if self.spike_check.isChecked():
            settings.append(self.spike_spin_box.text())
        else:
            settings.append(None)
        settings.append(self.threshold_spin_box.text())
        settings.append(self.rolling_spin_box.text())
        if self.flag2flag_check.isChecked():
            settings.append(self.original_spin_box.text())
            settings.append(self.translated_spin_box.text())
        else:
            settings.append(None)
            settings.append(None)
        if self.all_check.isChecked():
            settings.append("all")
        else:
            for index in range(self.key_list.count()):
                item = self.key_list.item(index)
                if item.checkState():
                    settings.append(item.text())

        self.list2qc.emit(settings)

    def addLabels(self, labels):
        """
        Add items to self.dropList
        """
        # Clear the list
        self.key_list.clear()
        # Add new items
        self.key_list.addItems(labels)
        # Configure the items checkable
        for index in range(self.key_list.count()):
            item = self.key_list.item(index)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
