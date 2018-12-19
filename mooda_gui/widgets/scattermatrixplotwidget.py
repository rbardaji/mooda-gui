"""Widget module"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg \
    as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT \
    as NavigationToolbar
from PyQt5.QtWidgets import QWidget, QToolBar, QAction, QVBoxLayout
from PyQt5.QtGui import QIcon
import seaborn as sms


class ScatterMatrixPlotWidget(QWidget):
    """
    Pyqt5 widget to show plots. It is used in PlotSplitter.
    """

    def __init__(self, wf, keys):  # pylint: disable=C0103
        """
        Constructor
        :param wf: inWater WaterFrame object
        :param key: key of wf.data to plot
        """
        super().__init__()

        # Instance variables
        self.wf = wf  # pylint: disable=C0103

        # Creation of the figure
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
        self.wf.scatter_matrix(keys=keys, ax=self.axes)
        # Plot custom view
        plt.tight_layout()
        sms.despine()

        self.init_ui()

    def init_ui(self):
        """Layout and main functionalities"""

        # Canvas
        self.plot_canvas = FigureCanvas(self.fig)
        self.plot_canvas.draw()

        # Matplotlib toolbar
        plot_toolbar = NavigationToolbar(self.plot_canvas, self)

        # Custom Toolbar
        action_toolbar = QToolBar(self)
        # - Actions -
        close_act = QAction(QIcon('oceanobs//app//mooda//icon//close.png'), 'Close', self)
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
