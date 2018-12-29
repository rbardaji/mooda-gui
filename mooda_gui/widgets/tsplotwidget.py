"""Here you have the widget show time series"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

import os
from numpy import timedelta64
import seaborn as sms
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QComboBox, QLabel, QSpinBox, QToolBar,
                             QVBoxLayout, QWidget)


class TSPlotWidget(QWidget):
    """
    Pyqt5 widget to show plots. It is used in PlotSplitter.
    """

    # Signals
    msg2statusbar = pyqtSignal(str)

    def __init__(self, wf, keys, right=None):  # pylint: disable=C0103
        """
        Constructor
        :param wf: inWater WaterFrame object
        :param keys: keys of wf.data to plot
        """
        super().__init__()

        # Instance variables
        self.wf = wf  # pylint: disable=C0103
        self.key = keys
        # Name of this object
        self.name = "_".join(keys)
        # List of keys in right position
        self.right = right

        # Calculate average_time of plot
        # Calculation of max size of dataframe and number of hours
        max_size = 0
        max_hour = 0
        for key in self.key:
            size = len(self.wf.data[key].dropna().index)
            date_period = self.wf.data[key].index[-1] - self.wf.data[
                key].index[0]
            date_period = date_period / timedelta64(1, 'h')  # pylint: disable=E1121
            if max_size < size:
                max_size = size
            if max_hour < date_period:
                max_hour = date_period
        average_text = 'None'
        average_time = None
        if max_size > 1000:
            if max_hour > 3360:  # More time than 20 weeks
                average_time = 'W'
                average_text = "Weekly"
            elif max_hour > 480:  # More than 20 days
                average_time = 'D'
                average_text = "Daily"
            elif max_hour > 20:  # More than 20 hours
                average_time = 'H'
                average_text = "Hourly"
            elif max_hour > 0.33:  # More than 20 minutes
                average_time = 'T'
                average_text = "Minutely"

        # Creation of the figure
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        if len(self.key) > 1:
            for key in self.key:
                self.axes = self.wf.tsplot(key, ax=self.axes,
                                           average_time=average_time)
        else:
            key = self.key[0]
            if "_QC" in key:
                self.axes = self.wf.qcplot(key[:-3], ax=self.axes)
            else:
                self.axes = self.wf.tsplot(key, ax=self.axes,
                                           average_time=average_time)
        # Plot custom view
        plt.tight_layout()
        if self.right is None:
            sms.despine()

        self.init_ui()

        self.average.setCurrentText(average_text)

    def init_ui(self):
        """Layout and main functionalities"""
        path_icon = str(
            os.path.dirname(os.path.abspath(__file__))) + "\\..\\icon\\"

        # Canvas
        self.plot_canvas = FigureCanvas(self.fig)
        self.plot_canvas.draw()

        # Matplotlib toolbar
        plot_toolbar = NavigationToolbar(self.plot_canvas, self)

        # Custom Toolbar
        action_toolbar = QToolBar(self)
        # - Labels -
        rolling_label = QLabel("Moving window: ")
        average_label = QLabel("  Average time: ")
        # - Spin Box -
        self.rolling = QSpinBox(self)
        self.rolling.setMinimum(0)
        self.rolling.setMaximum(1000)
        self.rolling.setValue(0)
        self.rolling.setToolTip(
            "Size of the moving window.\n"
            "This is the number of observations used for calculating"
            " the statistic.\n0 = Auto")
        self.average = QComboBox(self)
        self.average.addItems(
            ["None", "Minutely", "Hourly", "Daily", "Weekly"])
        self.average.setToolTip("")
        # - Actions -
        apply_act = QAction(QIcon(path_icon+"apply.png"), 'Apply', self)
        apply_act.triggered.connect(self.refresh_plot)
        close_act = QAction(QIcon(path_icon+"close.png"), 'Close', self)
        close_act.triggered.connect(self.hide)
        # - Format -
        action_toolbar.addWidget(rolling_label)
        action_toolbar.addWidget(self.rolling)
        action_toolbar.addWidget(average_label)
        action_toolbar.addWidget(self.average)
        action_toolbar.addAction(apply_act)
        action_toolbar.addSeparator()
        action_toolbar.addAction(close_act)

        # Layout
        # - For the Widget
        v_plot = QVBoxLayout()
        v_plot.addWidget(self.plot_canvas)
        v_plot.addWidget(plot_toolbar)
        v_plot.addWidget(action_toolbar)
        self.setLayout(v_plot)

    def refresh_plot(self):
        """
        It refresh the plot according to the actions of the action_toolbar
        :return:
        """

        self.msg2statusbar.emit("Making figure")

        # Remove previous axes from the figure
        self.axes.cla()

        # Rol value
        rol = self.rolling.value()
        if rol == 0:
            rol = None

        # Average value
        average = None
        if self.average.currentText() == 'Minutely':
            average = "T"
        elif self.average.currentText() == 'Hourly':
            average = "H"
        elif self.average.currentText() == 'Daily':
            average = "D"
        elif self.average.currentText() == 'Weekly':
            average = "W"

        if len(self.key) > 1:
            for key in self.key:
                second_y = False
                if key == self.right:
                    second_y = True
                self.axes = self.wf.tsplot(keys=key, ax=self.axes,
                                           secondary_y=second_y,
                                           average_time=average,
                                           rolling=rol)
        else:
            key = self.key[0]
            if "_QC" in key:
                self.axes = self.wf.qcplot(key[:-3], ax=self.axes)
            else:
                self.axes = self.wf.tsplot(keys=key, rolling=rol, ax=self.axes,
                                           average_time=average,
                                           secondary_y=False)
        # Plot custom view
        plt.tight_layout()
        if self.right is None:
            sms.despine()

        self.plot_canvas.draw()

        self.msg2statusbar.emit("Ready")

        print("Done")
