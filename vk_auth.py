# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from main_window import MainWindow
from model import Model

def main():
    app = QApplication([])

    model = Model()
    main = MainWindow(model)
    main.show()

    app.exec_()


if __name__ == "__main__":
    main()
