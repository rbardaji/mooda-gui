"""Widget module"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

import os
import seaborn as sms
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QToolBar, QVBoxLayout, QWidget)


class HistoPlotWidget(QWidget):
    """
    Pyqt5 widget to show plots. It is used in PlotSplitter.
    """

    # Signals
    msg2Statusbar = pyqtSignal(str)

    def __init__(self, wf, keys):  # pylint: disable=C0103
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
        self.name = "hist_"+self.name

        # Creation of the figure
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        self.axes = self.wf.hist(self.key, mean_line=True, ax=self.axes)
        # Plot custom view
        plt.tight_layout()
        sms.despine()

        self.init_ui()

    def init_ui(self):
        """Layout and main functionality"""
        path_icon = str(os.path.dirname(os.path.abspath(__file__))) + "\\..\\icon\\"

        # Canvas
        self.plot_canvas = FigureCanvas(self.fig)
        self.plot_canvas.draw()

        # Matplotlib toolbar
        plot_toolbar = NavigationToolbar(self.plot_canvas, self)

        # Custom Toolbar
        action_toolbar = QToolBar(self)
        # - Actions -
        close_act = QAction(QIcon(path_icon+"close.png"), 'Close', self)
        close_act.triggered.connect(self.hide)
        # - Format -
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

        self.msg2Statusbar.emit("Making figure")

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

        self.msg2Statusbar.emit("Ready")

        print("Done")
