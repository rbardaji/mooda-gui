"""This is the main module of of the mooda_gui. Here you have the code to load the GUI"""
# pylint: disable=no-name-in-module
# pylint: disable=import-error

import sys
from PyQt5.QtWidgets import QApplication
from mooda_gui.widgets import MOODA


def main():
    """Main function to load the GUI"""

    app = QApplication(sys.argv)
    mooda_app = MOODA()
    mooda_app.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
