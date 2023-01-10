import os
import sys
import csv
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random


class WriteGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        '''
        self.resize(width, height)
        self.move(300, 150)
        self.setWindowTitle('Measure Voltage Data')
        '''
        self.width = 600
        self.height = 750
        width = self.width
        height = self.height

        #config title
        self.title = QLabel('Measure Voltage Data', self)
        self.title.setFont(QFont('Arial', 26))
        self.title.move(int(width*4/20), int(height*1/20))

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
        self.cb_pin0.move(int(width*3/20),int(height*7/40))
        self.cb_pin1.move(int(width*7/20),int(height*7/40))
        self.cb_pin2.move(int(width*11/20),int(height*7/40))
        self.cb_pin3.move(int(width*15/20),int(height*7/40))
        self.cb_pin4.move(int(width*3/20),int(height*9/40))
        self.cb_pin5.move(int(width*7/20),int(height*9/40))
        self.cb_pin6.move(int(width*11/20),int(height*9/40))
        self.cb_pin7.move(int(width*15/20),int(height*9/40))

        # frequency 
        self.freq_text = QLabel('Frequency(Hz):', self)
        self.freq_text.setFont(QFont('Arial', 15))
        self.freq_text.move(int(width*3/20), int(height*6/20))
        self.freq = QComboBox(self)
        self.freq.setGeometry(int(width*9/20), int(height*6/20), 100, 30)
        self.freq_data = [10,100,200,500,1000,2000,3000]
        for i in range(len(self.freq_data)):
            self.freq.addItem(str(self.freq_data[i]))

        # Time Duration
        self.time_text = QLabel('Time Duration(Sec):', self)
        self.time_text.setFont(QFont('Arial', 15))
        self.time_text.move(int(width*3/20), int(height*7/20))
        self.time = QComboBox(self)
        self.time.setGeometry(int(width*9/20), int(height*7/20), 100, 30)
        self.duration_list = [1,2,3,4,5,10]
        for i in range(len(self.duration_list)):
            self.time.addItem(str(self.duration_list[i]))

        # choose file location button
        self.load_btn = QPushButton('Choose File Location (Select Folder)', self)
        self.load_btn.setFont(QFont('Times', 15))
        self.load_btn.setGeometry(int(width*3/20), int(height*17/40),400, 40)
        self.path_text = QLabel('Folder Path is not defined.', self)
        self.path_text.setFont(QFont('Times', 8))
        self.path_text.setGeometry(int(width*3/20), int(height*19/40),400,20)

        # save file name
        self.file_name_text = QLabel('File Name (.csv):', self)
        self.file_name_text.setFont(QFont('Arial', 15))
        self.file_name_text.move(int(width*3/20), int(height*21/40))
        self.file_name = QLineEdit(self)
        self.file_name.setGeometry(int(width*9/20), int(height*21/40), 220, 30)
        
        # measure button
        self.measure_btn = QPushButton('MEASURE', self)
        self.measure_btn.setFont(QFont('Times', 27))
        self.measure_btn.setGeometry(int(width*5/20), int(height*12/20), 280, 70)

        # display measured data and save or not
        self.graph_measured_data = PlotCanvas(self, width = 5, height = 4)
        self.graph_measured_data.setGeometry(int(self.width*0/20), int(self.height*29/40), int(self.width*20/20), int(self.height*5/20))
        self.save_btn = QPushButton('Save', self)
        self.save_btn.setFont(QFont('Times', 20))
        self.save_btn.setGeometry(int(width*3/20), int(height*20/20), 150, 55)

        self.dismiss_btn = QPushButton('Dismiss', self)
        self.dismiss_btn.setFont(QFont('Times', 20))
        self.dismiss_btn.setGeometry(int(width*11/20), int(height*20/20), 150, 55)


        # Configure Connection
        self.cb_pin0.stateChanged.connect(self.ensureMeasure) 
        self.cb_pin1.stateChanged.connect(self.ensureMeasure)
        self.cb_pin2.stateChanged.connect(self.ensureMeasure) 
        self.cb_pin3.stateChanged.connect(self.ensureMeasure)
        self.cb_pin4.stateChanged.connect(self.ensureMeasure) 
        self.cb_pin5.stateChanged.connect(self.ensureMeasure)
        self.cb_pin6.stateChanged.connect(self.ensureMeasure) 
        self.cb_pin7.stateChanged.connect(self.ensureMeasure)


        self.freq.currentIndexChanged.connect(self.ensureMeasure)
        self.time.currentIndexChanged.connect(self.ensureMeasure)
        self.file_name.textChanged.connect(self.ensureMeasure)
        self.load_btn.clicked.connect(self.fetchFolder)
        self.measure_btn.clicked.connect(self.runMeasure)

        self.file_name.setEnabled(False)
        self.measure_btn.setEnabled(False)
        self.path = None
        

    def fetchFolder(self):
        self.path = QFileDialog.getExistingDirectory(self)
        if self.path:
            self.path_text.setText('Path: ' + str(self.path))
            self.file_name.setEnabled(True)
            self.file_name.setText('sample')
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
        
        frequency = self.freq_data[self.freq.currentIndex()]
        duration = self.duration_list[self.time.currentIndex()]

        self.measure_btn.setEnabled(False)
        # python[] write.py[0] Pins(array)[1-8] Frequency[9] duration[10] filename[11] folder path[12]
        os.system('python write.py '
                + Pins[0]+' '+Pins[1]+' '+Pins[2]+' '+Pins[3]+' '+Pins[4]+' '+Pins[5]+' '+Pins[6]+' '+Pins[7]+' '
                + ' '
                + str(frequency)
                + ' '
                + str(duration)
                + ' '
                + self.file_name.text()
                + ' '
                + self.path
                )
        # self.measure_btn.setEnabled(True)
        PlotCanvas.changeData()



class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(True)

    def plot(self, check):
        if(check):
            time_data = [1,2,3]
            voltage_data =  [2,3,4]
            self.ax = self.figure.add_subplot(111)
            self.ax.plot(time_data, voltage_data)
            self.ax.set_title('PyQt Matplotlib Example')
            self.draw()
        else:
            time_data = [3,4,5]
            voltage_data = [1,4,2]
            self.ax.clear()
            self.ax.plot(time_data, voltage_data)

    def changeData(self):
        self.plot(False)####################


class DisplayGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
        self.resize(width, height)
        self.move(1000, 200)
        self.setWindowTitle('Display Voltage Data')
        '''
        self.width = 600
        self.height = 750
        width = self.width
        height = self.height

        # define elements
        self.text1 = QLabel('Display Voltage Data', self)
        self.text1.setFont(QFont('Arial', 26))
        self.text1.move(int(width*4/20), int(height*1/20))

        # Load voltage data
        self.loadbtn = QPushButton('Choose a Load File', self)
        self.loadbtn.setFont(QFont('Times', 15))
        self.loadbtn.setGeometry(int(width*3/20), int(height*2/10),400, 40)
        self.path_text = QLabel('Load file is not defined.', self)
        self.path_text.setFont(QFont('Times', 8))
        self.path_text.setGeometry(int(width*3/20), int(height*10/40),400,20)

        # Configure output
        diff = int(height*9/40)
        self.cb_pin0 = QCheckBox('pin0', self)
        self.cb_pin1 = QCheckBox('pin1', self)
        self.cb_pin0.setGeometry(int(width*1/10),int(height*7/20),100,30)
        self.cb_pin1.setGeometry(int(width*1/10),int(height*7/20)+diff,100,30)
        self.setStyleSheet("""
            QCheckBox{
                font-family: 'Arial';
                font-size: 30px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        self.cb_pin0.toggle() # default setting


        self.pin0_listA = QComboBox(self)
        self.pin0_listB = QComboBox(self)
        self.pin0_symbol = QComboBox(self)
        self.pin0_filter = QComboBox(self)
        self.pin0_symbol_text = QLabel('Option', self)
        self.pin0_filter_text = QLabel('Filter:',self)
        self.pin1_listA = QComboBox(self)
        self.pin1_listB = QComboBox(self)
        self.pin1_symbol = QComboBox(self)
        self.pin1_filter = QComboBox(self)
        self.pin1_symbol_text = QLabel('Option', self)
        self.pin1_filter_text = QLabel('Filter:',self)

        self.pin0_listA.setFont(QFont('Arial', 12))
        self.pin0_listB.setFont(QFont('Arial', 12))
        self.pin0_symbol.setFont(QFont('Arial', 15))
        self.pin0_filter.setFont(QFont('Arial', 12))
        self.pin0_symbol_text.setFont(QFont('Arial', 15))
        self.pin0_filter_text.setFont(QFont('Arial', 18))
        self.pin1_listA.setFont(QFont('Arial', 12))
        self.pin1_listB.setFont(QFont('Arial', 12))
        self.pin1_symbol.setFont(QFont('Arial', 15))
        self.pin1_filter.setFont(QFont('Arial', 12))
        self.pin1_symbol_text.setFont(QFont('Arial', 15))
        self.pin1_filter_text.setFont(QFont('Arial', 18))
        
        self.pin0_listA.setGeometry(int(width*11/40), int(height*7/20), 130, 40)
        self.pin0_listB.setGeometry(int(width*51/80), int(height*7/20), 130, 40)
        self.pin0_symbol.setGeometry(int(width*21/40), int(height*7/20), 50, 40)
        self.pin0_filter.setGeometry(int(width*11/40), int(height*35/80), 180, 40)
        self.pin0_symbol_text.move(int(width*83/160), int(height*25/80))
        self.pin0_filter_text.move(int(width*3/20), int(height*9/20))

        self.pin1_listA.setGeometry(int(width*11/40), int(height*7/20)+diff, 130, 40)
        self.pin1_listB.setGeometry(int(width*51/80), int(height*7/20)+diff, 130, 40)
        self.pin1_symbol.setGeometry(int(width*21/40), int(height*7/20)+diff, 50, 40)
        self.pin1_filter.setGeometry(int(width*11/40), int(height*35/80)+diff, 180, 40)
        self.pin1_symbol_text.move(int(width*83/160), int(height*25/80)+diff)
        self.pin1_filter_text.move(int(width*3/20), int(height*9/20)+diff)

        self.pin0_symbol.addItem('N')
        self.pin0_symbol.addItem('+')
        self.pin0_symbol.addItem('-')
        self.pin0_symbol.addItem('x')
        self.pin1_symbol.addItem('N')
        self.pin1_symbol.addItem('+')
        self.pin1_symbol.addItem('-')
        self.pin1_symbol.addItem('x')
        self.pin0_filter.addItem('None')
        self.pin0_filter.addItem('Low Pass Filter')
        self.pin0_filter.addItem('High Pass Filter')
        self.pin1_filter.addItem('None')
        self.pin1_filter.addItem('Low Pass Filter')
        self.pin1_filter.addItem('High Pass Filter')

        self.pin0_listA.setEnabled(False)
        self.pin0_listB.setEnabled(False)
        self.pin0_filter.setEnabled(False)
        self.pin0_symbol.setEnabled(False)
        self.pin1_listA.setEnabled(False)
        self.pin1_listB.setEnabled(False)
        self.pin1_filter.setEnabled(False)
        self.pin1_symbol.setEnabled(False)

        

        # run button
        self.display_btn = QPushButton('DISPLAY', self)
        self.display_btn.setFont(QFont('Times', 27))
        self.display_btn.setGeometry(int(width*5/20), int(height*16/20), 280, 70)


        # cover text(running)
        '''
        self.label_demo = QLabel('  ', self)
        self.label_demo.setGeometry(int(width*3/10),int(height*7/10), 200 , 50)
        self.label_demo.setFont(QFont('Arial', 30))
        '''

        # Configure Connection
        self.loadbtn.clicked.connect(self.fetchFile)
        self.cb_pin0.stateChanged.connect(self.ensureList0) # change statement
        self.cb_pin1.stateChanged.connect(self.ensureList1) # change statement
        self.pin0_symbol.currentIndexChanged.connect(self.ensureSymbol0)
        self.pin1_symbol.currentIndexChanged.connect(self.ensureSymbol1)


        self.display_btn.clicked.connect(self.runDisplay)
        
        self.check=False
        self.display_btn.setEnabled(False)
    
    def openCheckBox(self):
        self.pin0_listA.setEnabled(True)
        self.pin0_filter.setEnabled(True)
        self.pin0_symbol.setEnabled(True)
        self.pin1_listA.setEnabled(True)
        self.pin1_filter.setEnabled(True)
        self.pin1_symbol.setEnabled(True)


    def ensureRun(self):
        if (self.cb_pin0.isChecked() == True or self.cb_pin1.isChecked() == True) and self.check:
            self.display_btn.setEnabled(True)
        else :
            self.display_btn.setEnabled(False)
    
    def addElement(self, header):
        for i in range(1, len(header)):
            self.pin0_listA.addItem(header[i]) 
            self.pin0_listB.addItem(header[i])
            self.pin1_listA.addItem(header[i])
            self.pin1_listB.addItem(header[i])

    def clearElement(self):
        self.pin0_listA.clear()
        self.pin1_listA.clear()
    
    def fetchFile(self):
        self.path, self.check = QFileDialog.getOpenFileName(None,"Choose a load file","","CSV Files (*.csv);;Text Files (*.txt)")
        if self.check:
            self.path_text.setText('Path: '+str(self.path))
            self.clearElement()
            with open(self.path) as f:
                reader = csv.reader(f)
                header = reader.__next__()
                self.addElement(header)
        self.openCheckBox()
        self.ensureRun()
    
    def ensureList0(self, state):
        if state == Qt.Checked:
            self.pin0_listA.setEnabled(True)
            self.pin0_listB.setEnabled(True)
            self.pin0_filter.setEnabled(True)
            self.pin0_symbol.setEnabled(True)
        else:
            self.pin0_listA.setEnabled(False)
            self.pin0_listB.setEnabled(False)
            self.pin0_filter.setEnabled(False)
            self.pin0_symbol.setEnabled(False)
        self.ensureRun()

    def ensureList1(self, state):
        if state == Qt.Checked:
            self.pin1_listA.setEnabled(True)
            self.pin1_listB.setEnabled(True)
            self.pin1_filter.setEnabled(True)
            self.pin1_symbol.setEnabled(True)
        else:
            self.pin1_listA.setEnabled(False)
            self.pin1_listB.setEnabled(False)
            self.pin1_filter.setEnabled(False)
            self.pin1_symbol.setEnabled(False)
        self.ensureRun()

    def ensureSymbol0(self, state):
        if state != 0:
            self.pin0_listB.setEnabled(True)
        else :
            self.pin0_listB.setEnabled(False)
        
    def ensureSymbol1(self, state):
        if state != 0:
            self.pin1_listB.setEnabled(True)
        else :
            self.pin1_listB.setEnabled(False)

    def runDisplay(self):
        self.display_btn.setEnabled(False)

        # python[] display.py[0] 'path'[1] pin0(T/F)[2] pin0index[3] pin1(T/F)[4] pin1index[5]
        if self.check:
            os.system('python display.py '
                    + self.path
                    + ' '
                    + str(self.cb_pin0.isChecked())
                    + ' '
                    + str(self.pin0_listA.currentIndex())
                    + ' '
                    + str(self.cb_pin1.isChecked())
                    + ' '
                    + str(self.pin1_listA.currentIndex())
                    )
        self.display_btn.setEnabled(True)

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # define tabs widgets
        self.tabs = QTabWidget()
        write_tab = WriteGUI()
        display_tab = DisplayGUI()

        # add tabs
        self.tabs.addTab(write_tab,"Measure")
        self.tabs.addTab(display_tab,"Display")

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)

        self.setLayout(vbox)
    
        self.setWindowTitle("Easy M&D")
        self.setGeometry(100,100,600,900)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainGUI()
    sys.exit(app.exec_())