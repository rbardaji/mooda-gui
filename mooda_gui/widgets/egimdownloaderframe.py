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
                self.downloader.downloadAcoustic(
                    date, self.downloader.hour_minute_list.currentItem().text())
            else:
                parameters = [item.text() for item in
                              self.downloader.parameter_list.selectedItems()]
                for parameter in parameters:
                    self.downloader.downloadParameter(parameter)

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
        download_button.clicked.connect(self.downloadClick)
        download_button.setEnabled(False)
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.hide)

        # Lists
        self.egim_list = QListWidget(self)
        self.egim_list.itemClicked.connect(self.loadInstruments)
        self.egim_list.setMaximumWidth(200)

        self.instrument_list = QListWidget(self)
        self.instrument_list.itemClicked.connect(self.loadParameters)
        self.instrument_list.setMaximumWidth(290)

        self.metadata_list = QListWidget(self)

        self.parameter_list = QListWidget(self)
        self.parameter_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.parameter_list.itemClicked.connect(lambda: download_button.setEnabled(True))

        self.date_list = QListWidget(self)
        self.date_list.itemClicked.connect(self.loadTimes)
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
        self.limit_spin_box.valueChanged.connect(self.enableDate)

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
        self.parameterDateWidget = QWidget(self)
        # - Layout
        vparameterDate = QVBoxLayout()
        vparameterDate.addWidget(start_date_label)
        vparameterDate.addWidget(self.start_date_edit)
        vparameterDate.addWidget(end_date_label)
        vparameterDate.addWidget(self.end_date_edit)
        vparameterDate.addWidget(limit_label)
        vparameterDate.addWidget(self.limit_spin_box)
        vparameterDate.addStretch()
        self.parameterDateWidget.setLayout(vparameterDate)
        self.parameterDateWidget.setEnabled(False)

        # Layout
        # - Vertical layout for EGIM --
        vEgim = QVBoxLayout()
        vEgim.addWidget(egim_label)
        vEgim.addWidget(self.egim_list)
        # -- Vertical layout for instruments -
        vInstrument = QVBoxLayout()
        vInstrument.addWidget(instrument_label)
        vInstrument.addWidget(self.instrument_list)
        # - Vertical layout for parameters -
        vParameter = QVBoxLayout()
        vParameter.addWidget(metadata_label)
        vParameter.addWidget(self.metadata_list)
        vParameter.addWidget(parameter_label)
        vParameter.addWidget(self.parameter_list)
        # - Vertical layout for dates and buttons
        vButton = QVBoxLayout()
        vButton.addWidget(download_button)
        vButton.addWidget(close_button)
        vButton.addStretch()
        # - Layout of the frame -
        hFrame = QHBoxLayout()
        hFrame.addLayout(vEgim)
        hFrame.addLayout(vInstrument)
        hFrame.addLayout(vParameter)
        hFrame.addWidget(self.parameterDateWidget)
        hFrame.addWidget(self.acoustic_date_widget)
        hFrame.addLayout(vButton)

        self.setLayout(hFrame)

    def loadObservatories(self):
        """
        It asks for the available EGIM observatories and write its names into
        self.egim_list
        """

        # Send a message for the statusbar
        self.msg2Statusbar.emit("Loading observatories")
        # Clear self.egim_list
        self.egim_list.clear()
        # Ask for the observatories
        code, observatoryList = self.downloader.observatories()
        if code:
            if code == 200:
                # It means that you are going good
                self.egim_list.addItems(observatoryList)
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

    def loadInstruments(self, observatory):
        """
        It asks for the available instruments and write its names into
        self.instrument_list

        Parameters
        ----------
            observatory: item
                item from self.observatoryList
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
                sensorType = [
                    instrument['name'] for instrument in instrument_list_]
                self.instrument_list.addItems(sensorType)
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

    def loadParameters(self, instrument):
        """
        It asks for the available parameters and metadata and write them into
        self.parameter_list and self.metadata_list
        """
        # Send a message for the statusbar
        self.msg2Statusbar.emit("Loading parameters")
        # Clear self.parameter_list and self.metadata_list
        self.parameter_list.clear()
        self.metadata_list.clear()
        self.parameterDateWidget.setEnabled(False)
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

        self.parameterDateWidget.setEnabled(True)

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

    def loadTimes(self, date_item):
        """
        Write items into self.hour_minute_list QListWidget
        """
        for date in self.dates:
            if date['acousticObservationDate'] == date_item.text():
                timeList = []
                for time in date['observationsHourMinuteList']:
                    timeList.append(time['acousticObservationHourMinute'])
                self.hour_minute_list.addItems(timeList)

    def reload(self):
        """It clear all lists and load again the observatories."""
        # Check the password of the API
        if self.downloader.password is None:
            self.msg2Statusbar.emit(
                "Password is required to download data from EMSODEV")
            text, ok = QInputDialog.getText(self, "Attention", "Password",
                                            QLineEdit.Password)
            if ok:
                self.downloader.password = text
            else:
                return
        self.loadObservatories()

    def downloadClick(self):
        """Function when user click download"""

        self.my_thread = self.DownloadParameterThread(self)
        self.my_thread.start()

    def downloadParameter(self, parameter):
        """It download data with the observation function of EGIM"""

        # Send a message for the statusbar
        self.msg2Statusbar.emit("Downloading {}".format(parameter))

        code, df = self.downloader.observation(
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
                wf = self.downloader.to_waterframe(data=df,
                                                   metadata=self.metadata)
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

    def downloadAcoustic(self, date, time):
        # Send a message for the statusbar
        self.msg2Statusbar.emit(
            "Downloading acoustic file from {}, {}".format(date, time))

        code, df, metadata = self.downloader.acoustic_observation(
            observatory=self.egim_list.currentItem().text(),
            instrument=self.instrument_list.currentItem().text(),
            date=date,
            hour_minute=time)
        if code:
            if code == 200:
                self.msg2Statusbar.emit("Waterframe creation")
                # It means that you are going good
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

    def enableDate(self):
        """Enable or disable date elements"""
        if int(self.limit_spin_box.text()) > 0:
            self.start_date_edit.setEnabled(False)
            self.end_date_edit.setEnabled(False)
        else:
            self.start_date_edit.setEnabled(True)
            self.end_date_edit.setEnabled(True)
