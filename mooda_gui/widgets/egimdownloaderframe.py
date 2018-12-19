"""Here you have the widget that control the EGIM Download stuff"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

import datetime
from PyQt5.QtWidgets import (QFrame, QPushButton, QListWidget,
                             QAbstractItemView, QLabel, QDateEdit, QSpinBox,
                             QWidget, QVBoxLayout, QHBoxLayout, QInputDialog,
                             QLineEdit)
from PyQt5.QtCore import pyqtSignal, QThread, QTime, QDateTime, QDate
from mooda import WaterFrame
from mooda.access import EGIM


class EgimDownloaderFrame(QFrame):
    """Frame to download data from EMSODEV servers"""

    # Signals
    msg2Statusbar = pyqtSignal(str)
    wf2plotSplitter = pyqtSignal(WaterFrame)

    class DownloadParameterThread(QThread):
        """
        The process to download data from the API is very slow.
        We are going to use this thread to download data without block the app.
        """
        def __init__(self, downloader):
            QThread.__init__(self)

            self.downloader = downloader

        def __del__(self):
            self.wait()

        def run(self):
            """Thread main function"""

            if self.downloader.instrument_list.currentItem().text() \
               == "icListen-1636":
                date = datetime.datetime.strptime(
                    self.downloader.date_list.currentItem().text(),
                    "%Y-%m-%d").strftime("%d/%m/%Y")
                self.downloader.download_acoustic(
                    date, self.downloader.hour_minute_list.currentItem().text())
            else:
                parameters = [item.text() for item in
                              self.downloader.parameter_list.selectedItems()]
                for parameter in parameters:
                    self.downloader.download_parameter(parameter)

    def __init__(self):
        super().__init__()

        # Instance variables
        self.downloader = EGIM()
        self.wf = WaterFrame()  # pylint: disable=C0103
        self.metadata = dict()
        self.dates = []
        self.my_thread = None
        # Save the login of the EMSODEV API
        self.downloader.login = "emsodev"
        self.downloader.password = ""

        self.init_ui()

    def init_ui(self):
        """Layout and main functionalities"""

        # Buttons
        download_button = QPushButton("Download", self)
        download_button.clicked.connect(self.download_click)
        download_button.setEnabled(False)
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.hide)

        # Lists
        self.egim_list = QListWidget(self)
        self.egim_list.itemClicked.connect(self.load_instruments)
        self.egim_list.setMaximumWidth(200)

        self.instrument_list = QListWidget(self)
        self.instrument_list.itemClicked.connect(self.load_parameters)
        self.instrument_list.setMaximumWidth(290)

        self.metadata_list = QListWidget(self)

        self.parameter_list = QListWidget(self)
        self.parameter_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.parameter_list.itemClicked.connect(lambda: download_button.setEnabled(True))

        self.date_list = QListWidget(self)
        self.date_list.itemClicked.connect(self.load_times)
        self.date_list.setMaximumWidth(150)
        self.hour_minute_list = QListWidget(self)
        self.hour_minute_list.itemClicked.connect(lambda: download_button.setEnabled(True))
        self.hour_minute_list.setMaximumWidth(150)

        # Labels
        egim_label = QLabel("EGIM", self)
        instrument_label = QLabel("Instrument", self)
        metadata_label = QLabel("Metadata", self)
        parameter_label = QLabel("Parameter", self)
        start_date_label = QLabel("Start date", self)
        end_date_label = QLabel("End date", self)
        limit_label = QLabel("Get last X values", self)
        hour_label = QLabel("Hour and minute (HHmm)", self)
        date_label = QLabel("Available dates", self)

        # Date edit
        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDateTime(QDateTime(QDate(2017, 1, 27), QTime(0, 0, 0)))
        self.start_date_edit.setMinimumDateTime(QDateTime(QDate(2017, 1, 27), QTime(0, 0, 0)))
        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDateTime(QDateTime(QDate(2017, 1, 27), QTime(0, 0, 0)))
        self.end_date_edit.setMinimumDateTime(QDateTime(QDate(2017, 1, 27), QTime(0, 0, 0)))

        # Spin box
        self.limit_spin_box = QSpinBox(self)
        self.limit_spin_box.setMinimum(0)
        self.limit_spin_box.setMaximum(9999999999)
        self.limit_spin_box.setSingleStep(100)
        self.limit_spin_box.valueChanged.connect(self.enable_date)

        # Custom Widgets

        # Widget for dates of the acoustic data
        self.acoustic_date_widget = QWidget(self)
        # - Layout
        v_acoustic_date = QVBoxLayout()
        v_acoustic_date.addWidget(date_label)
        v_acoustic_date.addWidget(self.date_list)
        v_acoustic_date.addWidget(hour_label)
        v_acoustic_date.addWidget(self.hour_minute_list)
        self.acoustic_date_widget.setLayout(v_acoustic_date)
        self.acoustic_date_widget.setMaximumWidth(175)
        self.acoustic_date_widget.setEnabled(False)

        # Widget for dates of parameters
        self.parameter_date_widget = QWidget(self)
        # - Layout
        v_parameter_date = QVBoxLayout()
        v_parameter_date.addWidget(start_date_label)
        v_parameter_date.addWidget(self.start_date_edit)
        v_parameter_date.addWidget(end_date_label)
        v_parameter_date.addWidget(self.end_date_edit)
        v_parameter_date.addWidget(limit_label)
        v_parameter_date.addWidget(self.limit_spin_box)
        v_parameter_date.addStretch()
        self.parameter_date_widget.setLayout(v_parameter_date)
        self.parameter_date_widget.setEnabled(False)

        # Layout
        # - Vertical layout for EGIM --
        v_egim = QVBoxLayout()
        v_egim.addWidget(egim_label)
        v_egim.addWidget(self.egim_list)
        # -- Vertical layout for instruments -
        v_instrument = QVBoxLayout()
        v_instrument.addWidget(instrument_label)
        v_instrument.addWidget(self.instrument_list)
        # - Vertical layout for parameters -
        v_parameter = QVBoxLayout()
        v_parameter.addWidget(metadata_label)
        v_parameter.addWidget(self.metadata_list)
        v_parameter.addWidget(parameter_label)
        v_parameter.addWidget(self.parameter_list)
        # - Vertical layout for dates and buttons
        v_button = QVBoxLayout()
        v_button.addWidget(download_button)
        v_button.addWidget(close_button)
        v_button.addStretch()
        # - Layout of the frame -
        h_frame = QHBoxLayout()
        h_frame.addLayout(v_egim)
        h_frame.addLayout(v_instrument)
        h_frame.addLayout(v_parameter)
        h_frame.addWidget(self.parameter_date_widget)
        h_frame.addWidget(self.acoustic_date_widget)
        h_frame.addLayout(v_button)

        self.setLayout(h_frame)

    def load_observatories(self):
        """
        It asks for the available EGIM observatories and write its names into
        self.egim_list
        """

        # Send a message for the statusbar
        self.msg2Statusbar.emit("Loading observatories")
        # Clear self.egim_list
        self.egim_list.clear()
        # Ask for the observatories
        code, observatory_list = self.downloader.observatories()
        if code:
            if code == 200:
                # It means that you are going good
                self.egim_list.addItems(observatory_list)
                # Send a message for the statusbar
                self.msg2Statusbar.emit("Ready")
            elif code == 401:
                self.msg2Statusbar.emit(
                    "Unauthorized to use the EMSODEV DMP API")
                self.downloader.password = None
                self.reload()
            elif code == 404:
                self.msg2Statusbar.emit("Not Found")
            elif code == 403:
                self.msg2Statusbar.emit("Forbidden")
            elif code == 500:
                self.msg2Statusbar.emit("EMSODEV API internal error")
            else:
                self.msg2Statusbar.emit("Unknown EMSODEV DMP API error")
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")

    def load_instruments(self, observatory):
        """
        It asks for the available instruments and write its names into
        self.instrument_list

        Parameters
        ----------
            observatory: item
                item from self.observatory_list
        """
        # Send a message for the statusbar
        self.msg2Statusbar.emit("Loading instruments")
        # Clear self.instrument_list
        self.instrument_list.clear()
        # Ask for instruments
        code, instrument_list_ = self.downloader.instruments(observatory.text())
        if code:
            if code == 200:
                # It means that you are going good
                # Obtain all sensor names of instrument_list_
                sensor_type = [instrument['name'] for instrument in instrument_list_]
                self.instrument_list.addItems(sensor_type)
                # Add tooltip
                for i in range(self.instrument_list.count()):
                    self.instrument_list.item(i).setToolTip(
                        '<p><b>Sensor Type</b><br>' +
                        '{}</p><p>'.format(instrument_list_[i]['sensorType']) +
                        '<b>Long Name</b><br>' +
                        '{}</p>'.format(instrument_list_[i]['sensorLongName']) +
                        '<p></p><p><b>S/N</b><br>' +
                        '{}</p>'.format(instrument_list_[i]['sn']))
                # Send a message for the statusbar
                self.msg2Statusbar.emit("Ready")
            elif code == 401:
                self.msg2Statusbar.emit(
                    "Unauthorized to use the EMSODEV DMP API")
                self.downloader.password = None
                self.reload()
            elif code == 404:
                self.msg2Statusbar.emit("Not Found")
            elif code == 403:
                self.msg2Statusbar.emit("Forbidden")
            elif code == 500:
                self.msg2Statusbar.emit("EMSODEV API internal error")
            else:
                self.msg2Statusbar.emit("Unknown EMSODEV DMP API error")
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")

    def load_parameters(self, instrument):
        """
        It asks for the available parameters and metadata and write them into
        self.parameter_list and self.metadata_list
        """
        # Send a message for the statusbar
        self.msg2Statusbar.emit("Loading parameters")
        # Clear self.parameter_list and self.metadata_list
        self.parameter_list.clear()
        self.metadata_list.clear()
        self.parameter_date_widget.setEnabled(False)
        self.acoustic_date_widget.setEnabled(False)

        # If instrument is an icListener, check times
        if instrument.text() == "icListen-1636":
            self.acoustic_date_widget.setEnabled(True)
            # Ask for dates
            code, self.dates = self.downloader.acoustic_date(
                self.egim_list.currentItem().text(), instrument.text())
            if code == 200:
                date_list = [date['acousticObservationDate'] for date in self.dates]
                self.date_list.addItems(date_list)

            else:
                self.msg2Statusbar.emit(
                    "Impossible to connect to the EMSODEV DMP API")
                return
            return

        self.parameter_date_widget.setEnabled(True)

        # Ask for metadata
        code, self.metadata = self.downloader.metadata(
            self.egim_list.currentItem().text(), instrument.text())
        if code == 200:
            items = []
            for key, value in self.metadata.items():
                items.append("{}: {}".format(key, value))
            self.metadata_list.addItems(items)
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")
            return

        # Ask for parameters
        code, parameter_list_ = self.downloader.parameters(
            self.egim_list.currentItem().text(), instrument.text())
        if code:
            if code == 200:
                # It means that you are going good
                # Obtain all parameter names of parameter_list_
                names = [parameter['name'] for parameter in parameter_list_]
                self.parameter_list.addItems(names)
                self.parameter_list.sortItems()
                # Add tooltip
                for i in range(self.parameter_list.count()):
                    self.parameter_list.item(i).setToolTip(
                        '<b>Units:</b> {}'.format(parameter_list_[i]['uom']))
                # Send a message for the statusbar
                self.msg2Statusbar.emit("Ready")
            elif code == 401:
                self.msg2Statusbar.emit(
                    "Unauthorized to use the EMSODEV DMP API")
                self.downloader.password = None
                self.reload()
            elif code == 404:
                self.msg2Statusbar.emit("Not Found")
            elif code == 403:
                self.msg2Statusbar.emit("Forbidden")
            elif code == 500:
                self.msg2Statusbar.emit("EMSODEV API internal error")
            else:
                self.msg2Statusbar.emit("Unknown EMSODEV DMP API error")
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")

    def load_times(self, date_item):
        """
        Write items into self.hour_minute_list QListWidget
        """
        for date in self.dates:
            if date['acousticObservationDate'] == date_item.text():
                time_list = []
                for time in date['observationsHourMinuteList']:
                    time_list.append(time['acousticObservationHourMinute'])
                self.hour_minute_list.addItems(time_list)

    def reload(self):
        """It clear all lists and load again the observatories."""
        # Check the password of the API
        if self.downloader.password is None:
            self.msg2Statusbar.emit("Password is required to download data from EMSODEV")
            # pylint: disable=C0103
            text, ok = QInputDialog.getText(self, "Attention", "Password", QLineEdit.Password)
            if ok:
                self.downloader.password = text
            else:
                return
        self.load_observatories()

    def download_click(self):
        """Function when user click download"""

        self.my_thread = self.DownloadParameterThread(self)
        self.my_thread.start()

    def download_parameter(self, parameter):
        """It download data with the observation function of EGIM"""

        # Send a message for the statusbar
        self.msg2Statusbar.emit("Downloading {}".format(parameter))

        code, df = self.downloader.observation(  # pylint: disable=C0103
            observatory=self.egim_list.currentItem().text(),
            instrument=self.instrument_list.currentItem().text(),
            parameter=parameter,
            startDate=self.start_date_edit.text(),
            endDate=self.end_date_edit.text(),
            limit=self.limit_spin_box.text())
        if code:
            if code == 200:
                self.msg2Statusbar.emit("Waterframe creation")
                # It means that you are going good
                # pylint: disable=C0103
                wf = self.downloader.to_waterframe(data=df, metadata=self.metadata)
                # print(wf.data.head())
                # Send a signal with the new WaterFrame
                self.wf2plotSplitter.emit(wf)
                self.msg2Statusbar.emit("Ready")
            elif code == 401:
                self.msg2Statusbar.emit(
                    "Unauthorized to use the EMSODEV DMP API")
                self.downloader.password = None
                self.reload()
            elif code == 404:
                self.msg2Statusbar.emit("Not Found")
            elif code == 403:
                self.msg2Statusbar.emit("Forbidden")
            elif code == 500:
                self.msg2Statusbar.emit("EMSODEV API internal error")
            else:
                self.msg2Statusbar.emit("Unknown EMSODEV DMP API error")
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")

    def download_acoustic(self, date, time):
        """Download acoustic data from EMSO"""
        # Send a message for the statusbar
        self.msg2Statusbar.emit(
            "Downloading acoustic file from {}, {}".format(date, time))

        code, df, metadata = self.downloader.acoustic_observation(  # pylint: disable=C0103
            observatory=self.egim_list.currentItem().text(),
            instrument=self.instrument_list.currentItem().text(),
            date=date,
            hour_minute=time)
        if code:
            if code == 200:
                self.msg2Statusbar.emit("Waterframe creation")
                # It means that you are going good
                # pylint: disable=C0103
                wf = self.downloader.to_waterframe(data=df, metadata=metadata)
                # Send a signal with the new WaterFrame
                self.wf2plotSplitter.emit(wf)
                self.msg2Statusbar.emit("Ready")
            elif code == 401:
                self.msg2Statusbar.emit(
                    "Unauthorized to use the EMSODEV DMP API")
                self.downloader.password = None
                self.reload()
            elif code == 404:
                self.msg2Statusbar.emit("Not Found")
            elif code == 403:
                self.msg2Statusbar.emit("Forbidden")
            elif code == 500:
                self.msg2Statusbar.emit("EMSODEV API internal error")
            else:
                self.msg2Statusbar.emit("Unknown EMSODEV DMP API error")
        else:
            self.msg2Statusbar.emit(
                "Impossible to connect to the EMSODEV DMP API")

    def enable_date(self):
        """Enable or disable date elements"""
        if int(self.limit_spin_box.text()) > 0:
            self.start_date_edit.setEnabled(False)
            self.end_date_edit.setEnabled(False)
        else:
            self.start_date_edit.setEnabled(True)
            self.end_date_edit.setEnabled(True)
