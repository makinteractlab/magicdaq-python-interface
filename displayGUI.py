import sys
import os
import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

width = 600
height = 600

class ExampleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(width, height)
        self.move(600, 300)
        self.setWindowTitle('Display Voltage Data')


        # define elements
        self.text1 = QLabel('Display Voltage Data', self)
        self.text1.setFont(QFont('Arial', 24))
        self.text1.move(int(width*5/20), int(height*1/10))

        # Load voltage data
        self.loadbtn = QPushButton('Choose a Load File', self)
        self.loadbtn.setFont(QFont('Times', 15))
        self.loadbtn.setGeometry(int(width*3/20), int(height*2/10),400, 40)
        self.path_text = QLabel('Load file is not defined.', self)
        self.path_text.setFont(QFont('Times', 8))
        self.path_text.setGeometry(int(width*3/20), int(height*11/40),400,20)

        # Configure output
        self.cb_pin0 = QCheckBox('pin0', self)
        self.cb_pin1 = QCheckBox('pin1', self)
        self.dropdownlist0 = QtWidgets.QComboBox(self)
        self.dropdownlist1 = QtWidgets.QComboBox(self)
        
        self.cb_pin0.setFont(QFont('Arial', 20))
        self.cb_pin1.setFont(QFont('Arial', 20))
        self.dropdownlist0.setFont(QFont('Times', 12))
        self.dropdownlist1.setFont(QFont('Times', 12))
        self.cb_pin0.setGeometry(int(width*2/10),int(height*7/20),100,30)
        self.cb_pin1.setGeometry(int(width*2/10),int(height*9/20),100,30)
        self.dropdownlist0.setGeometry(int(width*4/10), int(height*7/20), 130, 30)
        self.dropdownlist1.setGeometry(int(width*4/10), int(height*9/20), 130, 30)
        self.cb_pin0.toggle() # default setting
        self.dropdownlist1.setEnabled(False)

        # run button
        self.runbtn = QPushButton('RUN!', self)
        self.runbtn.setFont(QFont('Times', 15))
        self.runbtn.setGeometry(int(width*3/10), int(height*6/10), 200, 40)

        # cover text(running)
        '''
        self.label_demo = QLabel('  ', self)
        self.label_demo.setGeometry(int(width*3/10),int(height*7/10), 200 , 50)
        self.label_demo.setFont(QFont('Arial', 30))
        '''
        
        # quit button
        qbtn = QPushButton('QUIT', self)
        qbtn.setFont(QFont('Times', 15))
        qbtn.setGeometry(int(width * 3/10), int(height * 8/10), 100, 40)


        # Configure Connection
        self.loadbtn.clicked.connect(self.fetchFile)
        self.cb_pin0.stateChanged.connect(self.ensureList0) # change statement
        self.cb_pin1.stateChanged.connect(self.ensureList1) # change statement
        self.runbtn.clicked.connect(self.runDisplay)
        qbtn.clicked.connect(QCoreApplication.instance().quit)

        self.runbtn.setEnabled(False)
        self.show()
    
    def ensureRun(self):
        if (self.cb_pin0.isChecked() == True or self.cb_pin1.isChecked() == True) and self.check:
            self.runbtn.setEnabled(True)
        else :
            self.runbtn.setEnabled(False)
    
    def addElement(self, header):
        for i in range(1, len(header)):
            self.dropdownlist0.addItem(header[i])
            self.dropdownlist1.addItem(header[i])

    def clearElement(self):
        self.dropdownlist0.clear()
        self.dropdownlist1.clear()
    
    def fetchFile(self):
        self.path, self.check = QtWidgets.QFileDialog.getOpenFileName(None,"Choose a load file","","CSV Files (*.csv);;Text Files (*.txt)")
        if self.check:
            self.path_text.setText('Path: '+str(self.path))
            self.clearElement()
            with open(self.path) as f:
                reader = csv.reader(f)
                header = reader.__next__()  # ヘッダーの読み込み
                self.addElement(header)
        self.ensureRun()
    
    def ensureList0(self, state):
        if state == Qt.Checked:
            self.dropdownlist0.setEnabled(True)
        else:
            self.dropdownlist0.setEnabled(False)
        self.ensureRun()

    def ensureList1(self, state):
        if state == Qt.Checked:
            self.dropdownlist1.setEnabled(True)
        else:
            self.dropdownlist1.setEnabled(False)
        self.ensureRun()

    def runDisplay(self):
        self.runbtn.setEnabled(False)

        if self.check:
            os.system('python display.py '
                    + self.path
                    + ' '
                    + str(self.cb_pin0.isChecked())
                    + ' '
                    + str(self.dropdownlist0.currentIndex())
                    + ' '
                    + str(self.cb_pin1.isChecked())
                    + ' '
                    + str(self.dropdownlist1.currentIndex())
                    )
        # python[] display.py[0] 'path'[1] pin0(T/F)[2] pin0index[3] pin1(T/F)[4] pin1index[5]
        self.runbtn.setEnabled(True)
    
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ew = ExampleWidget()    
    sys.exit(app.exec_())
