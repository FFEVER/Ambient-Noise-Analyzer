import sys
from builtins import super

import _thread

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# For history record
import pickle
from datetime import datetime

import time

# User libs
from Recorder import Recorder
from HistoryItem import HistoryItem


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Ambient Noise Analyzer'
        self.setWindowTitle(self.title)
        self.setFixedSize(480, 270)
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
        self.pushButton1.clicked.connect(self.on_start)
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
        self.table.setItem(0, 2, QTableWidgetItem("> 8 hours"))
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
        self.table.setItem(12, 2, QTableWidgetItem("1 second"))

        self.table.setItem(13, 0, QTableWidgetItem("5"))
        self.table.setItem(13, 1, QTableWidgetItem("130"))
        self.table.setItem(13, 2, QTableWidgetItem("< 1 second"))
        self.table.setItem(14, 1, QTableWidgetItem("140"))
        self.table.setItem(14, 2, QTableWidgetItem("NO Exposure"))

        self.table.resizeColumnsToContents()
        self.tab3.layout.addWidget(self.label2)
        self.tab3.layout.addWidget(self.table)
        self.tab3.setLayout(self.tab3.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.recorder = Recorder()
        # For checking is recording
        self.isRecording = False
        # Saving the last average decibel
        self.avgDecibel = 0
        # Saving the last time used
        self.recordedTime = 0

        # Read History File and update table
        self.initializeHistoryTable()

        self.empty = QIcon('')


    def record(self):
        self.isRecording = True
        start = time.time()

        print("*Recording*")
        while self.isRecording:
            # record sound from two mic
            dB1, dB2 = self.recorder.record(1)
            # Get average decibel
            self.avgDecibel = self.recorder.avg_decibel(dB1, dB2)
            # Show average decibel, Level and record time in the window
            level = self.classify_level(self.avgDecibel)
            exposure = self.classify_hour(self.avgDecibel)
            self.recordedTime = self.convertTime(start,time.time())
            self.dbLabel.setText("{:.2f}".format(self.avgDecibel) + ' db(A)' +
                                 '\nLevel ' + str(level) + " (" + exposure + ")" +
                                 '\n' + self.recordedTime)
            # Show which way the noise louder
            self.clssify_arrow_direction(dB1,dB2)


        print("*Record done*")

    def clssify_arrow_direction(self,db1,db2):
        if(db1 > db2):
            self.show_right()
        else:
            self.show_left()

    def classify_hour(self,decibel):
        if (decibel < 86):
            return "> 8 hours"
        elif (decibel >= 86 and decibel < 88):
            return "4 hours"
        elif (decibel >= 88 and decibel < 91):
            return "2 hours"
        elif (decibel >= 91 and decibel < 94):
            return "1 hour"
        elif (decibel >= 94 and decibel < 97):
            return "30 minutes"
        elif (decibel >= 97 and decibel < 100):
            return "15 minutes"
        elif (decibel >= 100 and decibel < 103):
            return "7.5 minutes"
        elif (decibel >= 103 and decibel < 109):
            return "112 seconds"
        elif (decibel >= 109 and decibel < 112):
            return "56 seconds"
        elif (decibel >= 112 and decibel < 121):
            return "28 seconds"
        elif (decibel >= 121 and decibel < 124):
            return "7 seconds"
        elif (decibel >= 124 and decibel < 127):
            return "3 seconds"
        elif (decibel >= 127 and decibel < 130):
            return "1 second"
        else:
            return "< 1 second"

    def classify_level(self,decibel):
        if(decibel < 97):
            return 1
        elif(decibel >= 97 and decibel <109):
            return 2
        elif (decibel >= 109 and decibel < 121):
            return 3
        elif (decibel >= 121 and decibel < 130):
            return 4
        else:
            return 5

    def convertTime(self,start,stop):
        seconds = int(stop - start)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        output = "%d:%02d:%02d" % (h, m, s)

        return output

    @pyqtSlot()
    def on_stop(self):
        # Close recording window
        self.showdb.close()
        self.tab1.show()

        # Reset isRecording
        self.isRecording = False

        # Add to history
        self.writeToHistoryFile()
        # Update the table
        self.updateHistoryTable()

    def writeToHistoryFile(self):
        if self.avgDecibel <= 0:
            return
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        historyItem = HistoryItem(time," {:.2f} ".format(self.avgDecibel),self.recordedTime)

        try:
            outfile = open("history.pkl", "ab")
        except FileNotFoundError:
            outfile = open("history.pkl", "wb")

        pickle.dump(historyItem, outfile)
        outfile.close()


    def readFromHistoryFile(self):
        objects = []

        # Check file existance first
        try:
            infile = open("history.pkl", "rb")
            infile.close()
        except FileNotFoundError:
            infile = open("history.pkl", "wb")
            infile.close()

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
            ["Time", "    Noise Level(dBA)    ", "Durations    "])
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
            ["Time", "    Noise Level(dBA)    ", "Durations    "])
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
    def on_start(self):
        # Create new window
        self.otherWindow()

        # Start recording
        _thread.start_new_thread(self.record, ())


    def otherWindow(self):
        self.tab1.hide()

        # Create new window
        self.startLayout = QGridLayout(self)
        self.showdb = QWidget()
        self.showdb.setFixedSize(480, 300)

        self.dbLabel = QLabel('', self)
        self.dbLabel.setAlignment(Qt.AlignCenter)
        self.dbLabel.setFont(QFont("Arail",24,QFont.Bold))
        #self.dbLabel.setFixedSize(450,100)

        self.stopButton = QPushButton('STOP',self)
        self.stopButton.clicked.connect(self.on_stop)
        self.stopButton.setFixedSize(300,50)

        self.Barrow1 = QPushButton('', self)
        self.Barrow2 = QPushButton('', self)
        self.Barrow1.setFixedSize(50, 50)
        self.Barrow2.setFixedSize(50, 50)

        self.Barrow1.clicked.connect(self.show_left)
        self.Barrow2.clicked.connect(self.show_right)

        self.Barrow1.setStyleSheet("border:0px")
        self.Barrow2.setStyleSheet("border:0px")

        self.startLayout.addWidget(self.dbLabel, 0, 1)
        self.startLayout.addWidget(self.stopButton, 1, 1)
        self.startLayout.addWidget(self.Barrow1, 0, 0)
        self.startLayout.addWidget(self.Barrow2, 0, 2)

        self.showdb.setLayout(self.startLayout)

        self.showdb.show()

    def show_right(self):
        self.Rightarrow = QIcon('Rightarrow.png')
        self.Barrow1.setIcon(self.empty)
        self.Barrow2.setIcon(self.Rightarrow)
        self.Barrow2.setIconSize(QSize(40, 40))

    def show_left(self):
        self.Leftarrow = QIcon('Leftarrow.png')
        self.Barrow2.setIcon(self.empty)
        self.Barrow1.setIcon(self.Leftarrow)
        self.Barrow1.setIconSize(QSize(40, 40))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())