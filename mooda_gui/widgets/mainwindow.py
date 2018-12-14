"""Module that contains the layout and principal methods of the main window of the GUI"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

import os
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QSplitter,
                             QFileDialog, QMenu)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDateTime, Qt
from mooda import WaterFrame
from mooda_gui.widgets import (TextFrame, PlotSplitter, EgimDownloaderFrame)


class MOODA(QMainWindow):
    """It is the main window of the GUI"""

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        """Layout of the main window"""

        path_icon = str(os.path.dirname(os.path.abspath(__file__))) + "\\..\\icon\\"
        # Status bar
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        # Create text zone
        self.datalog = TextFrame()
        self.datalog.msg2Statusbar[str].connect(self.statusbar.showMessage)

        # Plot Area
        self.plot_area = PlotSplitter()
        self.plot_area.msg2Statusbar[str].connect(self.statusbar.showMessage)
        self.plot_area.msg2TextArea[str].connect(self.datalog.write)

        # EGIM Downloader
        self.egim_downloader = EgimDownloaderFrame()
        self.egim_downloader.msg2Statusbar[str].connect(self.statusbar.showMessage)
        self.egim_downloader.wf2plotSplitter[WaterFrame].connect(self.open_file)

        # Menu bar
        menubar = self.menuBar()
        # - Menu File -
        file_menu = menubar.addMenu('&File')
        # -- New project --
        new_act = QAction(QIcon(path_icon+'\\new.png'), '&New project', self)
        new_act.setShortcut('Ctrl+N')
        new_act.setStatusTip('Clear the actual data frame to start a new one')
        new_act.triggered.connect(self.plot_area.newWaterFrame)
        file_menu.addAction(new_act)
        # -- Open --
        open_act = QAction(QIcon(path_icon+'\\open.svg'), '&Open', self)
        open_act.setShortcut('Ctrl+O')
        open_act.setStatusTip('Open data files for analyzing')
        open_act.triggered.connect(self.open_file)
        file_menu.addAction(open_act)
        # -- Add --
        add_act = QAction(QIcon(path_icon+'\\add.svg'), '&Add', self)
        add_act.setStatusTip('Add data to the current dataset')
        add_act.triggered.connect(lambda: self.open_file(concat=True))
        file_menu.addAction(add_act)
        # --- EGIM downloader ---
        downloader_act = QAction(QIcon(path_icon+'\\cloud.png'), '&EGIM downloader', self)
        downloader_act.setStatusTip('Open and analyze data from EMSODEV servers')
        downloader_act.triggered.connect(self.open_egim_downloader)
        file_menu.addAction(downloader_act)
        # --- Separator ---
        file_menu.addSeparator()
        # --- Save as ---
        self.save_act = QAction(QIcon(path_icon+'\\save.png'), '&Save as...', self)
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.setStatusTip('Save current data into a pickle')
        self.save_act.triggered.connect(self.saveFile)
        file_menu.addAction(self.save_act)
        # --- Separator ---
        file_menu.addSeparator()
        # -- Exit --
        exit_act = QAction(QIcon(path_icon+'\\exit.svg'), 'E&xit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)
        file_menu.addAction(exit_act)

        # - Menu Data -
        data_menu = menubar.addMenu('&Data')
        # -- Submenu Quality control --
        qc_menu = QMenu('&QC', self)
        # --- Auto QC ---
        self.qc_auto_act = QAction(QIcon(path_icon+'\\qc.png'), '&Auto', self)
        self.qc_auto_act.triggered.connect(self.plot_area.qcWidget.apply)
        qc_menu.addAction(self.qc_auto_act)
        # --- Preferences QC ---
        self.qc_preferences_act = QAction('&Preferences...', self)
        self.qc_preferences_act.triggered.connect(self.plot_area.qcWidget.show)
        qc_menu.addAction(self.qc_preferences_act)
        data_menu.addMenu(qc_menu)
        # -- Delete parameters --
        self.delete_act = QAction(QIcon(path_icon+'\\delete.png'), '&Remove parameters', self)
        self.delete_act.triggered.connect(self.plot_area.drop_widget.show)
        data_menu.addAction(self.delete_act)
        # -- Rename parameters --
        self.rename_act = QAction(QIcon(path_icon+'\\rename.png'), 'Re&name parameters', self)
        self.rename_act.triggered.connect(self.plot_area.renameWidget.show)
        data_menu.addAction(self.rename_act)
        # -- Resample data --
        self.resample_act = QAction(QIcon(path_icon+'\\resample.png'), 'Resam&ple data', self)
        self.resample_act.triggered.connect(self.plot_area.resampleWidget.show)
        data_menu.addAction(self.resample_act)
        # -- Slice data --
        self.slice_act = QAction(QIcon(path_icon+'\\slice.png'), '&Slice data', self)
        self.slice_act.triggered.connect(self.plot_area.sliceWidget.show)
        data_menu.addAction(self.slice_act)

        # - Menu View -
        view_menu = menubar.addMenu('&View')
        # -- Datalog --
        datalog_act = QAction(QIcon(path_icon+'\\log.png'), '&Datalog', self)
        datalog_act.setShortcut('F1')
        datalog_act.setStatusTip('Show the text area')
        datalog_act.triggered.connect(
            lambda: self.datalog.setVisible(not self.datalog.isVisible()))
        view_menu.addAction(datalog_act)
        # -- Metadata --
        self.metadata_act = QAction(QIcon(path_icon+'\\metadata.png'), '&Metadata', self)
        self.metadata_act.setShortcut('F2')
        self.metadata_act.setStatusTip("Show metadata area")
        self.metadata_act.triggered.connect(
            lambda: self.plot_area.vMetadataWidget.setVisible(
                not self.plot_area.vMetadataWidget.isVisible()))
        view_menu.addAction(self.metadata_act)
        # -- Data --
        self.data_view_act = QAction(QIcon(path_icon+'\\graph.png'), '&Parameters', self)
        self.data_view_act.setShortcut('F3')
        self.data_view_act.setStatusTip("Show data area")
        self.data_view_act.triggered.connect(
            lambda: self.plot_area.vDataSplitter.setVisible(
                not self.plot_area.vDataSplitter.isVisible()))
        view_menu.addAction(self.data_view_act)

        # Splitter
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.egim_downloader)
        splitter.addWidget(self.plot_area)
        splitter.addWidget(self.datalog)

        # Main Window
        # self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('MOODA')
        self.setWindowIcon(QIcon(path_icon+'\\mooda.png'))
        self.setCentralWidget(splitter)
        self.show()

        # Initial configuration
        # - Hide components
        self.egim_downloader.hide()
        self.datalog.hide()
        self.plot_area.hide()
        # - Write date and time into 'text'
        datetime_ = QDateTime.currentDateTime()
        self.datalog.write(datetime_.toString(Qt.DefaultLocaleLongDate))
        # - Disable actions from menus
        self.delete_act.setEnabled(False)
        self.save_act.setEnabled(False)
        self.qc_auto_act.setEnabled(False)
        self.qc_preferences_act.setEnabled(False)
        self.metadata_act.setEnabled(False)
        self.data_view_act.setEnabled(False)
        self.rename_act.setEnabled(False)
        self.resample_act.setEnabled(False)
        self.slice_act.setEnabled(False)

    def open_egim_downloader(self):
        """It shows the EgimDownloaderFrame."""
        self.egim_downloader.show()
        if self.egim_downloader.egimList.count() == 0:
            # New frame
            self.egim_downloader.reload()

    def open_file(self, wf=None, concat=False):
        """
        It opens a QFileDialog and load the input file
        :param wf: WaterFrame object
        :param concat: It adds the new WaterFrame into the actual Dataframe
        """
        if wf:
            file_name = wf
        else:
            # Open the save file dialog
            file_name, _ = QFileDialog.getOpenFileName(
                caption="Open data file", directory="",
                filter="NetCDF (*.nc);;CSV (*.csv);;Pickle (*.pkl)")

        # Send the path to the PlotFrame to be opened
        if file_name:
            ok = self.plot_area.openData(file_name, concat)
            if ok:
                # Show plot area
                self.plot_area.show()
                # Enable actions
                self.delete_act.setEnabled(True)
                self.save_act.setEnabled(True)
                self.metadata_act.setEnabled(True)
                self.data_view_act.setEnabled(True)
                self.qc_preferences_act.setEnabled(True)
                self.qc_auto_act.setEnabled(True)
                self.rename_act.setEnabled(True)
                self.resample_act.setEnabled(True)
                self.slice_act.setEnabled(True)

    def saveFile(self):
        """
        It opens a QFileDialog and save current data.
        """
        # Open the save file dialog
        file_name, _ = QFileDialog.getSaveFileName(
            caption="Open data file", directory="",
            filter="Pickle (*.pkl);;CSV (*.csv)")
        if file_name:
            self.plot_area.saveData(file_name)
