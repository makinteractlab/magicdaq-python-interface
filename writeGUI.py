import sys
import os
import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

width = 600
height = 750

class ExampleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.resize(width, height)
        self.move(600, 150)
        self.setWindowTitle('Measure Voltage Data')

        #config title
        self.title = QLabel('Measure Voltage Data', self)
        self.title.setFont(QFont('Arial', 24))
        self.title.move(int(width*5/20), int(height*1/20))

        # check box configure        
        self.exp1 = QLabel('Select measured Analog Pin:', self)
        self.exp1.setFont(QFont('Arial', 13))
        self.exp1.move(int(width*3/20), int(height*3/20))
        
        self.cb_pin0 = QCheckBox('Pin0', self)
        self.cb_pin1 = QCheckBox('Pin1', self)
        self.cb_pin2 = QCheckBox('Pin2', self)
        self.cb_pin3 = QCheckBox('Pin3', self)
        self.cb_pin4 = QCheckBox('Pin4', self)
        self.cb_pin5 = QCheckBox('Pin5', self)
        self.cb_pin6 = QCheckBox('Pin6', self)
        self.cb_pin7 = QCheckBox('Pin7', self)
        cb_font = QFont('Arial', 15)
        self.cb_pin0.setFont(cb_font)
        self.cb_pin1.setFont(cb_font)
        self.cb_pin2.setFont(cb_font)
        self.cb_pin3.setFont(cb_font)
        self.cb_pin4.setFont(cb_font)
        self.cb_pin5.setFont(cb_font)
        self.cb_pin6.setFont(cb_font)
        self.cb_pin7.setFont(cb_font)
        self.cb_pin0.move(int(width*3/20),int(height*4/20))
        self.cb_pin1.move(int(width*7/20),int(height*4/20))
        self.cb_pin2.move(int(width*11/20),int(height*4/20))
        self.cb_pin3.move(int(width*15/20),int(height*4/20))
        self.cb_pin4.move(int(width*3/20),int(height*5/20))
        self.cb_pin5.move(int(width*7/20),int(height*5/20))
        self.cb_pin6.move(int(width*11/20),int(height*5/20))
        self.cb_pin7.move(int(width*15/20),int(height*5/20))

        # frequency 
        self.freq_text = QLabel('Frequency(Hz):', self)
        self.freq_text.setFont(QFont('Arial', 15))
        self.freq_text.move(int(width*3/20), int(height*7/20))
        self.freq = QLineEdit(self)
        self.freq.setGeometry(int(width*9/20), int(height*7/20), 100, 30)

        # Time Duration
        self.time_text = QLabel('Time Duration(Sec):', self)
        self.time_text.setFont(QFont('Arial', 15))
        self.time_text.move(int(width*3/20), int(height*8/20))
        self.time = QLineEdit(self)
        self.time.setGeometry(int(width*9/20), int(height*8/20), 100, 30)

        # save file name
        self.file_name_text = QLabel('File Name (.csv):', self)
        self.file_name_text.setFont(QFont('Arial', 15))
        self.file_name_text.move(int(width*3/20), int(height*10/20))
        self.file_name = QLineEdit(self)
        self.file_name.setGeometry(int(width*9/20), int(height*10/20), 220, 30)
        
        # choose file location button
        self.save_btn = QPushButton('Choose File Location (Select Folder)', self)
        self.save_btn.setFont(QFont('Times', 15))
        self.save_btn.setGeometry(int(width*3/20), int(height*11/20),400, 40)
        self.path_text = QLabel('Folder Path is not defined.', self)
        self.path_text.setFont(QFont('Times', 8))
        self.path_text.setGeometry(int(width*3/20), int(height*12/20),400,20)

        # measure button
        self.measure_btn = QPushButton('MEASURE!', self)
        self.measure_btn.setFont(QFont('Times', 18))
        self.measure_btn.setGeometry(int(width*6/20), int(height*14/20), 200, 60)

        # quit button
        self.quit_btn = QPushButton('QUIT', self)
        self.quit_btn.setFont(QFont('Times', 18))
        self.quit_btn.setGeometry(int(width * 3/10), int(height * 17/20), 200, 60)
        
        # Configure Connection
        self.cb_pin0.stateChanged.connect(self.ensureMeasure) 
        self.cb_pin1.stateChanged.connect(self.ensureMeasure)
        self.cb_pin2.stateChanged.connect(self.ensureMeasure) 
        self.cb_pin3.stateChanged.connect(self.ensureMeasure)
        self.cb_pin4.stateChanged.connect(self.ensureMeasure) 
        self.cb_pin5.stateChanged.connect(self.ensureMeasure)
        self.cb_pin6.stateChanged.connect(self.ensureMeasure) 
        self.cb_pin7.stateChanged.connect(self.ensureMeasure)

        self.freq.textChanged.connect(self.ensureMeasure)
        self.time.textChanged.connect(self.ensureMeasure)
        self.file_name.textChanged.connect(self.ensureMeasure)
        self.save_btn.clicked.connect(self.fetchFolder)
        self.measure_btn.clicked.connect(self.runMeasure)
        self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

        self.measure_btn.setEnabled(False)
        self.path = None

        self.show()

    def fetchFolder(self):
        self.path = QtWidgets.QFileDialog.getExistingDirectory(self)
        if self.path:
            self.path_text.setText('Path: ' + str(self.path))
            self.ensureMeasure()

    def ensureMeasure(self):
        if (self.cb_pin0.isChecked() or 
            self.cb_pin1.isChecked() or
            self.cb_pin2.isChecked() or 
            self.cb_pin3.isChecked() or
            self.cb_pin4.isChecked() or 
            self.cb_pin5.isChecked() or
            self.cb_pin6.isChecked() or 
            self.cb_pin7.isChecked() ) and (
            self.freq.text() != '' and 
            self.time.text() != '' and 
            self.file_name.text() != '' and 
            self.path):
                self.measure_btn.setEnabled(True)
        else :
            self.measure_btn.setEnabled(False)

    def runMeasure(self):
        Pins = [self.cb_pin0.isChecked(),
                self.cb_pin1.isChecked(),
                self.cb_pin2.isChecked(),
                self.cb_pin3.isChecked(),
                self.cb_pin4.isChecked(),
                self.cb_pin5.isChecked(),
                self.cb_pin6.isChecked(),
                self.cb_pin7.isChecked()]
        Pins = [str(x) for x in Pins]
        frequency = self.freq.text()
        duration = self.time.text()

        self.measure_btn.setEnabled(False)
        # python[] write.py[0] Pins(array)[1-8] Frequency[9] duration[10] filename[11] folder path[12]
        os.system('python write.py '
                + Pins[0]+' '+Pins[1]+' '+Pins[2]+' '+Pins[3]+' '+Pins[4]+' '+Pins[5]+' '+Pins[6]+' '+Pins[7]+' '
                + ' '
                + frequency
                + ' '
                + duration
                + ' '
                + self.file_name.text()
                + ' '
                + self.path
                )
        self.measure_btn.setEnabled(True)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ew = ExampleWidget()    
    sys.exit(app.exec_())