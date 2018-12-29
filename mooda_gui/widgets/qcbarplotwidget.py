"""Module that creates a QWidget to show the qcbarplot() of mooda"""

# pylint: disable=no-name-in-module
# pylint: disable=import-error

import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT \
    as NavigationToolbar
from PyQt5.QtWidgets import QWidget, QToolBar, QVBoxLayout, QAction
from PyQt5.QtGui import QIcon
import seaborn as sms


class QCBarPlotWidget(QWidget):
    """
    Pyqt5 widget to show plots. It is used in PlotSplitter.
    """

    def __init__(self, wf):  # pylint: disable=C0103
        """
        :param wf: inWater WaterFrame object
        """
        super().__init__()

        # Instance variables
        self.wf = wf  # pylint: disable=C0103
        self.name = "QC"
        self.key = "all"

        # Creation of the figure
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        self.wf.qcbarplot(ax=self.axes)
        # Plot custom view
        plt.tight_layout()
        sms.despine()

        self.init_ui()

    def init_ui(self):
        """Layout and connections"""

        path_icon = str(os.path.dirname(os.path.abspath(__file__))) + "\\..\\icon\\"
        # Canvas
        self.plot_canvas = FigureCanvas(self.fig)
        self.plot_canvas.draw()

        # Matplotlib toolbar
        plot_toolbar = NavigationToolbar(self.plot_canvas, self)

        # Custom Toolbar
        action_toolbar = QToolBar(self)
        # - Actions -
        apply_act = QAction(QIcon(path_icon+"refresh.png"), 'Refresh', self)
        apply_act.triggered.connect(self.refresh_plot)
        close_act = QAction(QIcon(path_icon+"close.png"), 'Close', self)
        close_act.triggered.connect(self.hide)
        # - Format -
        action_toolbar.addAction(apply_act)
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
        self.wf.qcbarplot(ax=self.axes)
        plt.tight_layout()
        self.plot_canvas.draw()
