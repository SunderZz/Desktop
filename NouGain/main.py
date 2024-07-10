import sys
from PyQt5.QtWidgets import QApplication
from controller.main_controller import MainController
from PyQt5 import QtGui
def main():
    app = QApplication(sys.argv)
    controller = MainController()
    font = QtGui.QFont("Montserrat", 10)
    app.setFont(font)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
