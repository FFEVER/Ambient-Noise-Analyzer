import sys
from builtins import super

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pickle

#User lib
from Recorder import Recorder
from HistoryItem import HistoryItem


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Ambient Noise Analyzer'
        self.setWindowTitle(self.title)
        self.setFixedSize(480,300)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()
        sys.exit(app.exec_())


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Main")
        self.tabs.addTab(self.tab2, "History")
        self.tabs.addTab(self.tab3, "Info")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)

        self.label = QLabel('', self)
        self.label.setPixmap(QPixmap("logo2.png"))
        self.label.setAlignment(Qt.AlignCenter)

        self.pushButton1 = QPushButton('', self)
        self.pushButton1.clicked.connect(self.OtherWindow)
        self.pushButton1.setIcon(QIcon('enter.png'))

        self.pushButton1.setIconSize(QSize(200, 100))
        self.pushButton1.setStyleSheet("border:0px")

        self.tab1.layout.addWidget(self.label)
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

        # Create third tab

        self.tab3.layout = QVBoxLayout(self)
        self.label2 = QLabel('* dBA -> A-weighted sound levels', self)

        self.table = QTableWidget(self)
        self.table.setRowCount(15)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Level    ", "    Noise Level(dBA)    ", "Maximum Exposure Time per 24 hours"])
        self.table.verticalHeader().setVisible(False)

        self.table.setItem(0, 0, QTableWidgetItem("1"))
        self.table.setItem(0, 1, QTableWidgetItem("85"))
        self.table.setItem(0, 2, QTableWidgetItem("8 hours"))
        self.table.setItem(1, 1, QTableWidgetItem("88"))
        self.table.setItem(1, 2, QTableWidgetItem("4 hours"))
        self.table.setItem(2, 1, QTableWidgetItem("91"))
        self.table.setItem(2, 2, QTableWidgetItem("2 hours"))
        self.table.setItem(3, 1, QTableWidgetItem("94"))
        self.table.setItem(3, 2, QTableWidgetItem("1 hour"))

        self.table.setItem(4, 0, QTableWidgetItem("2"))
        self.table.setItem(4, 1, QTableWidgetItem("97"))
        self.table.setItem(4, 2, QTableWidgetItem("30 minutes"))
        self.table.setItem(5, 1, QTableWidgetItem("100"))
        self.table.setItem(5, 2, QTableWidgetItem("15 minutes"))
        self.table.setItem(6, 1, QTableWidgetItem("103"))
        self.table.setItem(6, 2, QTableWidgetItem("7.5 minutes"))

        self.table.setItem(7, 0, QTableWidgetItem("3"))
        self.table.setItem(7, 1, QTableWidgetItem("109"))
        self.table.setItem(7, 2, QTableWidgetItem("112 seconds"))
        self.table.setItem(8, 1, QTableWidgetItem("112"))
        self.table.setItem(8, 2, QTableWidgetItem("56 seconds"))
        self.table.setItem(9, 1, QTableWidgetItem("115"))
        self.table.setItem(9, 2, QTableWidgetItem("28 seconds"))

        self.table.setItem(10, 0, QTableWidgetItem("4"))
        self.table.setItem(10, 1, QTableWidgetItem("121"))
        self.table.setItem(10, 2, QTableWidgetItem("7 seconds"))
        self.table.setItem(11, 1, QTableWidgetItem("124"))
        self.table.setItem(11, 2, QTableWidgetItem("3 seconds"))
        self.table.setItem(12, 1, QTableWidgetItem("127"))
        self.table.setItem(12, 2, QTableWidgetItem("1 seconds"))

        self.table.setItem(13, 0, QTableWidgetItem("5"))
        self.table.setItem(13, 1, QTableWidgetItem("130"))
        self.table.setItem(13, 2, QTableWidgetItem("< 1 seconds"))
        self.table.setItem(14, 1, QTableWidgetItem("140"))
        self.table.setItem(14, 2, QTableWidgetItem("NO Exposure"))

        self.table.resizeColumnsToContents()
        self.tab3.layout.addWidget(self.label2)
        self.tab3.layout.addWidget(self.table)
        self.tab3.setLayout(self.tab3.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.recorder = None
        # For checking is recording
        self.isRecording = False

        # Read History File and update table
        self.initializeHistoryTable()


    @pyqtSlot()
    def on_click(self):
        self.writeToHistoryFile(HistoryItem("1/1/2017","77.1","22.0"))
        self.updateHistoryTable()

        # # Initialize Recorder
        # self.recorder = Recorder()
        # print("*Recording*")
        # # Set state to recording
        # self.isRecording = True
        # # Record until stop button pressed
        # self.record()

        self.recorder = None
    def record(self):
        if self.recorder is None:
            return

        while(self.isRecording):
            dB1,dB2 = self.recorder.record(1)
            print(dB1,dB2,self.recorder.avg_decibel(dB1,dB2))

    def writeToHistoryFile(self, historyItem):
        outfile = open("history.pkl", "ab")
        pickle.dump(historyItem, outfile)
        outfile.close()
        del historyItem
    def readFromHistoryFile(self):
        objects = []
        with (open("history.pkl", "rb")) as openfile:
            while True:
                try:
                    objects.append(pickle.load(openfile))
                except EOFError:
                    break
        return objects

    def initializeHistoryTable(self):
        objects = self.readFromHistoryFile()

        self.tab2.layout = QVBoxLayout(self)


        # create Table
        self.historyTable = QTableWidget(self)
        self.historyTable.setRowCount(len(objects))
        self.historyTable.setColumnCount(3)
        self.historyTable.setHorizontalHeaderLabels(
            ["Time             ", "                    Noise Level(dBA)                   ", "Durations                  "])
        self.historyTable.resize(500, 500)
        self.historyTable.verticalHeader().setVisible(False)

        for i in range(0,len(objects)):
            objects[i].getTime()
            self.historyTable.setItem(i, 0, QTableWidgetItem(objects[i].getTime()))
            self.historyTable.setItem(i, 1, QTableWidgetItem(objects[i].getdba()))
            self.historyTable.setItem(i, 2, QTableWidgetItem(objects[i].getDuration()))

        self.historyTable.resizeColumnsToContents()
        self.tab2.layout.addWidget(self.historyTable)
        self.tab2.setLayout(self.tab2.layout)

    def updateHistoryTable(self):
        self.historyTable.clearContents()

        objects = self.readFromHistoryFile()
        # create Table
        self.historyTable.setRowCount(len(objects))
        self.historyTable.setColumnCount(3)
        self.historyTable.setHorizontalHeaderLabels(
            ["Time             ", "                    Noise Level(dBA)                   ",
             "Durations                  "])
        self.historyTable.resize(500, 500)
        self.historyTable.verticalHeader().setVisible(False)

        for i in range(0, len(objects)):
            objects[i].getTime()
            self.historyTable.setItem(i, 0, QTableWidgetItem(objects[i].getTime()))
            self.historyTable.setItem(i, 1, QTableWidgetItem(objects[i].getdba()))
            self.historyTable.setItem(i, 2, QTableWidgetItem(objects[i].getDuration()))

        self.historyTable.resizeColumnsToContents()
        self.tab2.layout.addWidget(self.historyTable)
    @pyqtSlot()
    def on_click(self):
        self.showdb.hide()
        self.tab1.show()

    def OtherWindow(self):
        self.tab1.hide()
        self.db = "80"
        self.level = "1"
        self.startLayout = QGridLayout(self)
        self.showdb = QWidget()
        self.showdb.setFixedSize(480, 300)

        self.dbLabel = QLabel('hi', self)
        self.dbLabel.setText(self.db+' db(A)'+ '\nLevel ' + self.level)
        self.dbLabel.setAlignment(Qt.AlignCenter)
        self.dbLabel.setFont(QFont("Arail",24,QFont.Bold))
        #self.dbLabel.setFixedSize(450,100)

        self.stopButton = QPushButton('STOP',self)
        self.stopButton.clicked.connect(self.on_click)
        self.stopButton.setFixedSize(300,50)

        self.Barrow1 = QPushButton('',self)
        self.Barrow1.setFixedSize(50, 50)

        self.Barrow2 = QPushButton('',self)
        self.Barrow2.setFixedSize(50, 50)

        self.startLayout.addWidget(self.dbLabel, 0, 1)
        self.startLayout.addWidget(self.stopButton, 1, 1)
        self.startLayout.addWidget(self.Barrow1, 0, 0)
        self.startLayout.addWidget(self.Barrow2, 0, 2)

        self.showdb.setLayout(self.startLayout)

        self.showdb.show()
        #self.arrow1.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())