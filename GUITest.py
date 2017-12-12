from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QWidget, QApplication

class MyWindow(QMainWindow):

    front_wid = None

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        # MAIN WINDOW size
        self.setFixedSize(200,200)

        # CENTRAL WIDGET
        self.central_wid = QWidget()
        self.layout_for_wids = QStackedLayout()

        # BUTTON TO SWITCH BETWEEN WIDGETS
        self.btn_switch = QPushButton("Switch")
        self.btn_switch.clicked.connect(self.switch_wids)
        self.btn_switch.setFixedSize(50,50)
        self.btn_switch

        # 2 WIDGETS
        self.wid1 = QWidget()
        self.wid1.setStyleSheet("""background: blue;""")
        self.wid1.setFixedSize(200,200)
        self.wid1.move(100, 100)
        self.wid2 = QWidget()
        self.wid2.setStyleSheet("""background: green;""")
        self.wid2.setFixedSize(200, 200)
        self.wid2.move(100, 100)

        # LAYOUT CONTAINER FOR WIDGETS AND BUTTON
        self.layout_for_wids.addWidget(self.btn_switch)
        self.layout_for_wids.addWidget(self.wid1)
        self.layout_for_wids.addWidget(self.wid2)

        # ENTERING LAYOUT
        self.central_wid.setLayout(self.layout_for_wids)

        # CHOOSE YOUR CENTRAL WIDGET
        self.setCentralWidget(self.central_wid)

        # WHICH WIDGET IS ON THE FRONT
        self.front_wid = 1

    def switch_wids(self):

        # LOGIC TO SWITCH
        if self.front_wid == 1:
            self.wid1.hide()
            self.wid2.show()
            self.front_wid = 2
        else:
            self.wid1.show()
            self.wid2.hide()
            self.front_wid = 1



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.resize(222, 222)
    main.show()

    sys.exit(app.exec_())