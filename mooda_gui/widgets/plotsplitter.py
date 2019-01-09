"""Module to create a Widget"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

from PyQt5.QtWidgets import (QWidget, QLabel, QListWidget, QPushButton,
                             QVBoxLayout, QSplitter, QGroupBox, QRadioButton,
                             QAbstractItemView, QPlainTextEdit)
from PyQt5.QtCore import pyqtSignal, Qt
from mooda import WaterFrame
from mooda_gui.widgets import (DropWidget, QCWidget, RenameWidget, ResampleWidget, SliceWidget,
                               ScatterMatrixPlotWidget, QCPlotWidget, TSPlotWidget, QCBarPlotWidget,
                               SpectrogramPlotWidget)
from mooda_gui.widgets.histoplotwidget import HistoPlotWidget


class PlotSplitter(QSplitter):
    """Pyqt5 widget to show data in plots and lists."""

    # Signals
    msg2statusbar = pyqtSignal(str)
    msg2TextArea = pyqtSignal(str)

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

        # Instance variables
        self.wf = WaterFrame()  # pylint: disable=C0103
        # List of PlotWidget, to control them in any case
        self.plot_widget_list = []

        self.init_ui()

    def init_ui(self):
        """UI creator"""

        # Lists
        self.data_list = QListWidget(self)
        self.data_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.data_list.itemClicked.connect(self.data_list_click)
        self.graph_list = QListWidget(self)
        self.graph_list.itemClicked.connect(self.graph_click)

        # PlainTextEdit
        self.other_info_plain_text = QPlainTextEdit(self)
        self.metadata_plain_text = QPlainTextEdit(self)

        # Labels
        metadata_label = QLabel("Metadata")
        data_label = QLabel("Data")
        graph_label = QLabel("Graph")
        info_label = QLabel("Other information")

        # DropWidget
        self.drop_widget = DropWidget()
        self.drop_widget.list2drop[list, list, bool].connect(self.drop_data)
        self.drop_widget.hide()

        # Group Box
        plot_group_box = QGroupBox("Plot properties", self)
        v_plot_group_box = QVBoxLayout()
        # - RadioButton
        self.auto_plot_radio_button = QRadioButton("Time series plot", self)
        self.auto_plot_radio_button.setChecked(True)
        self.multiple_parameter_radio_button = QRadioButton("Multiparameter", self)
        self.correlation_radio_button = QRadioButton("Correlation", self)
        self.histogram_radio_button = QRadioButton("Histogram", self)
        self.parameter_qc_radio_button = QRadioButton("QC of the parameter", self)
        v_plot_group_box.addWidget(self.auto_plot_radio_button)
        v_plot_group_box.addWidget(self.histogram_radio_button)
        v_plot_group_box.addWidget(self.multiple_parameter_radio_button)
        v_plot_group_box.addWidget(self.correlation_radio_button)
        v_plot_group_box.addWidget(self.parameter_qc_radio_button)
        plot_group_box.setLayout(v_plot_group_box)

        # QCWidget
        self.qc_widget = QCWidget()
        self.qc_widget.list2qc[list].connect(self.apply_qc)
        self.qc_widget.hide()

        # RenameWidget
        self.rename_widget = RenameWidget()
        self.rename_widget.key2change[str, str].connect(self.apply_rename)
        self.rename_widget.hide()

        # ResampleWidget
        self.resample_widget = ResampleWidget()
        self.resample_widget.resampleRule[str].connect(self.apply_resample)
        self.resample_widget.hide()

        # SliceWidget
        self.slice_widget = SliceWidget()
        self.slice_widget.sliceTimes[str, str].connect(self.apply_slice)
        self.slice_widget.hide()

        # Splitters
        self.v_data_splitter = QSplitter(Qt.Vertical)
        # Custom Widget Metadata
        self.v_metadata_widget = QWidget()

        # Buttons
        # - For metadata area
        hide_metadata_button = QPushButton("Hide")
        hide_metadata_button.clicked.connect(self.v_metadata_widget.hide)
        # - For data Area
        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.add_plot)
        hide_data_button = QPushButton("Hide")
        hide_data_button.clicked.connect(self.v_data_splitter.hide)

        # Custom Widget Data
        # - Data Widget
        parameter_widget = QWidget()
        # -- Layout
        v_data = QVBoxLayout()
        v_data.addWidget(data_label)
        v_data.addWidget(self.data_list)
        v_data.addWidget(plot_group_box)
        v_data.addWidget(plot_button)
        parameter_widget.setLayout(v_data)
        # - Graph Widget
        graph_widget = QWidget()
        # -- Layout
        v_graph = QVBoxLayout()
        v_graph.addWidget(graph_label)
        v_graph.addWidget(self.graph_list)
        v_graph.addWidget(hide_data_button)
        graph_widget.setLayout(v_graph)
        # - Data splitter
        self.v_data_splitter.addWidget(parameter_widget)
        self.v_data_splitter.addWidget(graph_widget)

        # Layouts
        # - Metadata -
        v_metadata = QVBoxLayout()
        v_metadata.addWidget(metadata_label)
        v_metadata.addWidget(self.metadata_plain_text)
        v_metadata.addWidget(info_label)
        v_metadata.addWidget(self.other_info_plain_text)
        v_metadata.addWidget(hide_metadata_button)
        self.v_metadata_widget.setLayout(v_metadata)

        # Splitter (self)
        # - Layout for actions
        v_actions_widget = QWidget()
        v_actions = QVBoxLayout()
        v_actions.addWidget(self.rename_widget)
        v_actions.addWidget(self.resample_widget)
        v_actions.addWidget(self.drop_widget)
        v_actions.addWidget(self.slice_widget)
        v_actions.addStretch()
        v_actions_widget.setLayout(v_actions)
        # - Add to self (splitter)
        self.addWidget(self.qc_widget)
        self.addWidget(v_actions_widget)
        self.addWidget(self.v_metadata_widget)
        self.addWidget(self.v_data_splitter)

    def data_list_click(self):
        """Action on lick item of data_list"""
        if (self.auto_plot_radio_button.isChecked() or self.histogram_radio_button.isChecked()):
            self.add_plot()

    def add_plot(self):
        """It creates a FigureCanvas with the input figure"""

        self.msg2statusbar.emit("Making the figure")

        # Create key list
        keys = [item.text() for item in self.data_list.selectedItems()]

        # If nothing is selected, go out
        if not keys:
            self.msg2statusbar.emit("Ready")
            return

        # Check if it is a QC plot
        if self.parameter_qc_radio_button.isChecked():
            keys = [keys[0] + "_QC"]

        # Check if it is a correlation
        if self.correlation_radio_button.isChecked():
            plot_widget = ScatterMatrixPlotWidget(wf=self.wf, keys=keys)
            self.addWidget(plot_widget)
            self.msg2statusbar.emit("Ready")
            return

        # Create name of the plot
        name = '_'.join(keys)

        if self.histogram_radio_button.isChecked():
            name = "hist_" + name

        # Check if plot is done
        new = True
        for plot_widget in self.plot_widget_list:
            if plot_widget.name == name:
                if ~plot_widget.isVisible():
                    plot_widget.refresh_plot()
                    plot_widget.show()
                new = False
                break

        # Create the plot if is new
        if new:
            if len(keys) == 1 and "_QC" in keys[0]:
                plot_widget = QCPlotWidget(wf=self.wf, key=keys[0])
            else:
                if self.histogram_radio_button.isChecked():
                    plot_widget = HistoPlotWidget(wf=self.wf, keys=keys)
                else:
                    plot_widget = TSPlotWidget(wf=self.wf, keys=keys)
                plot_widget.msg2statusbar[str].connect(self.msg2statusbar.emit)
            self.addWidget(plot_widget)
            # Add the widget to the list
            self.plot_widget_list.append(plot_widget)

        self.msg2statusbar.emit("Ready")

    def add_qc_bar_plot(self):
        """
        It creates a FigureCanvas with the input figure (QC)
        """
        self.msg2statusbar.emit("Making the figure")
        # Check if the plot exists
        plot_widget = None
        for plot_widget_ in self.plot_widget_list:
            if plot_widget_.name == "QC":
                plot_widget = plot_widget_
                plot_widget.wf = self.wf
                plot_widget.refresh_plot()
                plot_widget.show()
                break
        if plot_widget is None:

            plot_widget = QCBarPlotWidget(wf=self.wf)
            self.addWidget(plot_widget)
            # Add the widget to the list
            self.plot_widget_list.append(plot_widget)
        self.msg2statusbar.emit("Ready")

    def add_spectro_plot(self):
        """It ads the SpectroplotWidget to the screen"""

        self.msg2statusbar.emit("Making the figure")
        # Check if the plot exists
        plot_widget = None
        for plot_widget_ in self.plot_widget_list:
            if plot_widget_.name == "Spectrogram":
                plot_widget = plot_widget_
                plot_widget.wf = self.wf
                plot_widget.refresh_plot()
                plot_widget.show()
                break
        if plot_widget is None:
            plot_widget = SpectrogramPlotWidget(wf=self.wf)
            self.addWidget(plot_widget)
            # Add the widget to the list
            self.plot_widget_list.append(plot_widget)
        self.msg2statusbar.emit("Ready")

    def open_data(self, path, concat=False):
        """
        It opens the netcdf of the path.

        Parameters
        ----------
            path: str or WaterFrame
                Path where the file is or WaterFrame object.
            concat: bool, optional (concat = False)
                It adds the new dataframe to the current dataframe.

        Returns
        -------
            True/False: bool
                It indicates if the operation is ok.
        """
        debug = True  # Variable for debug reasons

        if debug:
            print("In PlotSplitter.open_data():")
            print("  - Emit msg2statusbar: Opening data")

        self.msg2statusbar.emit("Opening data")
        if isinstance(path, str):
            if debug:
                print("  - path is a string:", path)
            # Obtain type of file
            extension = path.split(".")[-1]
            # Init ok
            ok = False  # pylint: disable=C0103
            wf_new = WaterFrame()
            if extension == "nc":
                ok = wf_new.from_netcdf(path)  # pylint: disable=C0103
            elif extension == "pkl":
                ok = wf_new.from_pickle(path)  # pylint: disable=C0103
            if ok:
                # Check if we want actual data
                if not concat:
                    self.new_waterframe()
                self.wf.concat(wf_new)

                self.msg2TextArea.emit("Working with file {}".format(path))
                # Add metadata information into metadataList
                self.add_metadata(self.wf.metadata)
                # Add other information
                self.other_info_plain_text.setPlainText(repr(self.wf))
                # Add data information into data_list
                self.add_data(self.wf.data)
                # Plot QC
                self.add_qc_bar_plot()
                self.msg2statusbar.emit("Ready")
                if debug:
                    print("  - Emit msg2statusbar: Ready")
                    print("  - Exit from PlotSplitter.open_data()")
                return True
            else:
                self.msg2statusbar.emit("Error opening data")
                if debug:
                    print("  - Emit msg2statusbar: Error opening data")
                    print("  - Exit from PlotSplitter.open_data()")
                return False
        else:
            # Path is a WaterFrame
            if debug:
                print("  - path is a WaterFrame")
                print(path)
            # Check if there is no data in the waterframe
            if path.data.empty:
                return False

            # Check if it is a dataframe of an acoustic data.
            # In this case, we are going to delete the previous dataframe.
            if "Sequence" in self.wf.data.keys():
                self.wf.clear()
            self.wf.concat(path)

            # Add data information into data_list
            self.add_data(self.wf.data)
            self.add_metadata(self.wf.metadata)
            # Add other information
            self.other_info_plain_text.setPlainText(repr(self.wf))
            # Plot QC
            self.add_qc_bar_plot()
            return True

    def add_metadata(self, metadata_dict):
        """
        Add Metadata information into self.metadata_plain_text
        :param metadata_dict: WaterFrame Metadata Dictionary
        """
        # Clear the list
        self.metadata_plain_text.clear()

        items = []
        msg = "\nMetadata:"
        for key, value in metadata_dict.items():
            items.append("{}: {}".format(key, value))
            msg += "\n- {}: {}".format(key, value)
        self.metadata_plain_text.setPlainText(msg[11:])
        # Send a message to the text area
        self.msg2TextArea.emit(msg)

    def add_data(self, data):
        """
        Add data names into self.data_list
        :param data: WaterFrame data variable
        """

        def is_acoustic_data(a):  # pylint: disable=C0103
            # will be True also for 'NaN'
            if a == "Sequence":
                return True
            elif a == "Data Points":
                return True
            try:
                float(a)
                return True
            except ValueError:
                return False

        # Clear the list
        self.data_list.clear()
        # Parameter keys (without QC)
        # NO DEPTH in nc files, NO TIME
        keys_to_work = [key for key in data.keys() if 'TIME' not in key
                        if not is_acoustic_data(key)
                        if key + "_QC" in data.keys()]
        self.data_list.addItems(keys_to_work)
        # Add graphs
        self.graph_list.clear()
        self.graph_list.addItem("QC")
        # Check if we have acoustic data
        for key in data.keys():
            if is_acoustic_data(key):
                self.graph_list.addItem("Spectrogram")
                break

        # Add tooltip
        msg = "\nData:"
        for i in range(self.data_list.count()):
            if "_QC" in self.data_list.item(i).text():
                self.data_list.item(i).setToolTip(
                    'QC flags of {}'.format(self.data_list.item(i).text()[:-3]))
            else:
                try:
                    self.data_list.item(i).setToolTip('{} ({})'.format(
                        self.wf.meaning[
                            self.data_list.item(i).text()]['long_name'],
                        self.wf.meaning[
                            self.data_list.item(i).text()]['units']))
                    msg += "\n- {}: {} ({})".format(
                        self.data_list.item(i).text(),
                        self.wf.meaning[
                            self.data_list.item(i).text()]['long_name'],
                        self.wf.meaning[
                            self.data_list.item(i).text()]['units'])
                except KeyError:
                    pass
        # Send a message to the text area
        self.msg2TextArea.emit(msg)
        # Send the labels to the drop_widget
        self.drop_widget.add_labels(keys_to_work)
        self.qc_widget.add_labels(keys_to_work)
        self.rename_widget.add_labels(keys_to_work)
        self.slice_widget.refresh(self.wf.data.index[0], self.wf.data.index[-1])

    def save_data(self, path):
        """
        Save current data into a pickle file
        :param path: File path
        :return: Bool
        """
        self.msg2statusbar.emit("Saving data")
        extension = path.split(".")[-1]
        # Init ok
        ok = False  # pylint: disable=C0103
        if extension == "nc":
            pass
        elif extension == "pkl":
            ok = self.wf.to_pickle(path)  # pylint: disable=C0103
        elif extension == "csv":
            ok = self.wf.to_csv(path)  # pylint: disable=C0103

        if ok:
            self.msg2TextArea.emit("Data saved on file {}".format(path))
            self.msg2statusbar.emit("Ready")
        return ok

    def drop_data(self, labels, flag_list, drop_nan):
        """
        Delete some parameters from self.wf and refresh the lists
        :param labels: list of labels to drop
        :param flag_list: list of flags to drop
        :return:
        """
        self.msg2TextArea.emit("Deleting data")

        # This is a trick, delete the list if is a list of None
        if flag_list[0] is None:
            flag_list = None

        if flag_list:
            self.wf.use_only(parameters=labels, flags=[0, 1], dropnan=drop_nan)
        else:
            # Delete the parameters
            self.wf.drop(keys=labels, flags=flag_list)
        # Refresh the lists
        self.add_data(self.wf.data)

        # Delete plots with the key
        for label in labels:
            for plot_widget in self.plot_widget_list:
                if plot_widget.name == "QC":
                    plot_widget.refresh_plot()
                if label == plot_widget.name or label+"_" in \
                   plot_widget.name or "_"+label in plot_widget.name:
                    plot_widget.deleteLater()
                    self.plot_widget_list.remove(plot_widget)

        # Send message
        msg = ""
        if flag_list is None:
            for label in labels:
                if '_QC' in label:
                    continue
                msg += "{} ".format(label)
            msg += "deleted"
        else:
            msg += "Data with QC Flags "
            for flag in flag_list:
                msg += "{}, ".format(flag)
            msg += "from "
            for label in labels:
                if '_QC' in label:
                    continue
                msg += "{}, ".format(label)
            msg += "deleted"
        self.msg2TextArea.emit("\n{}".format(msg))
        self.msg2statusbar.emit(msg)

    def apply_qc(self, list_qc):
        """
        Apply the QC procedures
        :param list_qc:
        :return:
        """

        def do_it(key_in):
            """
            Common part, to not repeat code
            :param key_in: key to apply QC tests
            """
            if '_QC' in key_in:
                return
            if list_qc[0]:
                #  Reset flags
                self.msg2statusbar.emit(
                    "Setting flags from {} to {}".format(key_in, list_qc[0]))
                self.wf.reset_flag(parameters=key_in, flag=int(list_qc[0]))
                self.msg2statusbar.emit("Ready")
            if list_qc[3]:
                # Spike test
                threshold = float(list_qc[4].replace(',', '.'))
                self.msg2statusbar.emit(
                    "Applying spike test to "
                    "{}, with rolling window {} and threshold {}".format(
                        key_in, list_qc[5], threshold))
                self.wf.spike_test(parameters=key_in, window=int(list_qc[5]),
                                   threshold=threshold, flag=int(list_qc[3]))
                self.msg2statusbar.emit("Ready")
            if list_qc[1]:
                # Range test
                self.msg2statusbar.emit(
                    "Applying range test to {}".format(key_in))
                self.wf.range_test(parameters=key_in, flag=int(list_qc[1]))
                self.msg2statusbar.emit("Ready")
            if list_qc[2]:
                # Flat test
                self.msg2statusbar.emit(
                    "Applying flat test to"
                    " {}, with rolling window {}".format(key_in, list_qc[5]))
                self.wf.flat_test(parameters=key_in, window=int(list_qc[5]),
                                  flag=int(list_qc[2]))
                self.msg2statusbar.emit("Ready")
            if list_qc[6]:
                # Flag to flag
                self.msg2statusbar.emit(
                    "Changing flags of "
                    "{} from {} to {}".format(key_in, list_qc[6], list_qc[7]))
                self.wf.flag2flag(parameters=key_in, original_flag=int(list_qc[6]),
                                  translated_flag=int(list_qc[7]))
                self.msg2statusbar.emit("Ready")

        self.msg2statusbar.emit("Creating QC flags")

        if list_qc[8] == 'all':
            for key in self.wf.parameters():
                do_it(key_in=key)
        else:
            for i in range(8, len(list_qc)):
                key = list_qc[i]
                do_it(key_in=key)

        self.msg2statusbar.emit("Updating graphs")
        # Refresh the QC graph
        for plot_widget in self.plot_widget_list:
            if "QC" in plot_widget.name:

                if plot_widget.isVisible():
                    plot_widget.refresh_plot()
                # Show the QCBarPlot
                elif plot_widget.name == "QC":
                    plot_widget.refresh_plot()
                    plot_widget.show()
        self.msg2statusbar.emit("Ready")

    def apply_rename(self, original_key, new_key):
        """It renames keys from a WaterFrame"""
        # Rename key from the Waterframe
        self.msg2statusbar.emit(
            "Changing name {} to {}".format(original_key, new_key))
        self.wf.rename(original_key, new_key)
        # Rename the key of the plotWidgets if it process
        for plot_widget in self.plot_widget_list:
            if isinstance(plot_widget.key, list):
                for i, key in enumerate(plot_widget.key):
                    if key == original_key:
                        plot_widget.key[i] = new_key
                        plot_widget.name = plot_widget.name.replace(original_key, new_key)
                        plot_widget.refresh_plot()
            else:
                if plot_widget.name == "QC":
                    plot_widget.refresh_plot()
                elif plot_widget.key == original_key:
                    plot_widget.key = new_key
                    plot_widget.name = new_key
                    plot_widget.refresh_plot()
        # Add data information into data_list
        self.add_data(self.wf.data)
        self.msg2statusbar.emit("Ready")
        self.msg2TextArea.emit("Key name {} changed to {}.".format(original_key, new_key))

    def apply_resample(self, rule):
        """
        It applies the resample function to  self.waterframe
        :param rule: Rule to resample.
        """
        self.msg2statusbar.emit("Resampling data")
        self.wf.resample(rule)
        self.msg2statusbar.emit("Ready")

        self.msg2statusbar.emit("Updating graphs")
        # Refresh the QC graph
        for plot_widget in self.plot_widget_list:
            if "QC" in plot_widget.name:

                if plot_widget.isVisible():
                    plot_widget.refresh_plot()
                # Show the QCBarPlot
                elif plot_widget.name == "QC":
                    plot_widget.refresh_plot()
                    plot_widget.show()
        self.msg2statusbar.emit("Ready")

    def apply_slice(self, start, stop):
        """
        It applies the resample function to  self.waterframe
        :param start: Start time.
        :param stop: Stop time
        """
        self.msg2statusbar.emit("Slicing data")

        self.wf.slice_time(start, stop)

        self.add_data(self.wf.data)
        self.refresh_plots()

        self.msg2statusbar.emit("Ready")
        self.msg2TextArea.emit(
            "Dataframe sliced from {} to {}.".format(start, stop))

    def graph_click(self, item):
        """Function on click the plot button"""
        if item.text() == "QC":
            self.add_qc_bar_plot()
        elif item.text() == "Spectrogram":
            self.add_spectro_plot()

    def new_waterframe(self):
        """Create a new WaterFrame object and clean all screens."""
        self.wf = WaterFrame()
        # Delete all plots
        for plot_widget in self.plot_widget_list:
            plot_widget.deleteLater()
        self.plot_widget_list.clear()
        # Hide the widget
        self.hide()

    def refresh_plots(self):
        """It refresh all plots"""
        self.msg2statusbar.emit("Refreshing plots")

        for plot_widget in self.plot_widget_list:
            try:
                plot_widget.refresh_plot()
            except KeyError:
                self.plot_widget_list.remove(plot_widget)
                plot_widget.hide()
                plot_widget.deleteLater()

        self.msg2statusbar.emit("Ready")
