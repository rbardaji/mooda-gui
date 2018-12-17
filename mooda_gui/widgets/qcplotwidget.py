"""It contains QCPlotWidget"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT \
    as NavigationToolbar
from PyQt5.QtWidgets import QWidget, QToolBar, QAction, QVBoxLayout
from PyQt5.QtGui import QIcon
import seaborn as sms


class QCPlotWidget(QWidget):
    """Pyqt5 widget to show plots. It is used in PlotSplitter."""

    def __init__(self, wf, key):  # pylint: disable=C0103
        """
        Constructor
        :param wf: inWater WaterFrame object
        :param key: key of wf.data to plot
        """
        super().__init__()

        # Instance variables
        self.wf = wf  # pylint: disable=C0103
        self.key = key
        # Name of this object
        self.name = "new"

        # Creation of the figure
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        # The name will be the key
        self.name = key
        if "_QC" in key:
            self.wf.qcplot(key[:-3], ax=self.axes)
        else:
            return
        # Plot custom view
        plt.tight_layout()
        sms.despine()

        self.init_ui()

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
        # - Actions -
        refresh_act = QAction(QIcon(path_icon+"refresh.png"), 'Refresh', self)
        refresh_act.triggered.connect(self.refresh_plot)
        close_act = QAction(QIcon(path_icon+"close.png"), 'Close', self)
        close_act.triggered.connect(self.hide)
        # - Format -
        action_toolbar.addAction(refresh_act)
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
        # Remove previous axes from the figure
        self.axes.clear()
        # Remake the plot
        self.wf.qcplot(self.key[:-3], ax=self.axes)

        plt.tight_layout()
        self.plot_canvas.draw()
