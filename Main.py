#!/usr/bin/python3
from MainWindow import MainWindow
from PyQt5.QtCore import QDate

class Main():
    def __init__(self):
        program = MainWindow()
    def startProgram(self):
        now = QDate.currentDate()


if __name__ == '__main__':
    main = Main()
    main.startProgram()