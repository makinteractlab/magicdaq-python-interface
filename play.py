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
        width = 600
        height = 750

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
        self.freq = QComboBox(self)
        self.freq.setGeometry(int(width*9/20), int(height*7/20), 100, 30)
        self.freq_data = [10,100,200,500,1000,2000,3000]
        for i in range(len(self.freq_data)):
            self.freq.addItem(str(self.freq_data[i]))

        # Time Duration
        self.time_text = QLabel('Time Duration(Sec):', self)
        self.time_text.setFont(QFont('Arial', 15))
        self.time_text.move(int(width*3/20), int(height*8/20))
        self.time = QComboBox(self)
        self.time.setGeometry(int(width*9/20), int(height*8/20), 100, 30)
        self.duration_list = [1,2,3,4,5,10]
        for i in range(len(self.duration_list)):
            self.time.addItem(str(self.duration_list[i]))

        # choose file location button
        self.save_btn = QPushButton('Choose File Location (Select Folder)', self)
        self.save_btn.setFont(QFont('Times', 15))
        self.save_btn.setGeometry(int(width*3/20), int(height*10/20),400, 40)
        self.path_text = QLabel('Folder Path is not defined.', self)
        self.path_text.setFont(QFont('Times', 8))
        self.path_text.setGeometry(int(width*3/20), int(height*11/20),400,20)

        # save file name
        self.file_name_text = QLabel('File Name (.csv):', self)
        self.file_name_text.setFont(QFont('Arial', 15))
        self.file_name_text.move(int(width*3/20), int(height*12/20))
        self.file_name = QLineEdit(self)
        self.file_name.setGeometry(int(width*9/20), int(height*12/20), 220, 30)
        
        # measure button
        self.measure_btn = QPushButton('MEASURE', self)
        self.measure_btn.setFont(QFont('Times', 27))
        self.measure_btn.setGeometry(int(width*5/20), int(height*14/20), 280, 80)

        # display measured data and save or not
        '''
        fig = Figure(figsize=(400, 200), dpi = 100)
        self.axes = fig.add_subplot(111)
        self.axes.plot([2,3,4],[3,6,21])
        FigureCanvas.__init__(self, fig)
        self.setParent(None)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
        '''

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
        self.save_btn.clicked.connect(self.fetchFolder)
        self.measure_btn.clicked.connect(self.runMeasure)

        self.file_name.setEnabled(False)
        self.measure_btn.setEnabled(False)
        self.path = None

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()


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
        self.measure_btn.setEnabled(True)


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
        width= 600
        height= 750

        # define elements
        self.text1 = QLabel('Display Voltage Data', self)
        self.text1.setFont(QFont('Arial', 24))
        self.text1.move(int(width*5/20), int(height*1/20))

        # Load voltage data
        self.loadbtn = QPushButton('Choose a Load File', self)
        self.loadbtn.setFont(QFont('Times', 15))
        self.loadbtn.setGeometry(int(width*3/20), int(height*2/10),400, 40)
        self.path_text = QLabel('Load file is not defined.', self)
        self.path_text.setFont(QFont('Times', 8))
        self.path_text.setGeometry(int(width*3/20), int(height*12/40),400,20)

        # Configure output
        self.cb_pin0 = QCheckBox('pin0', self)
        self.cb_pin1 = QCheckBox('pin1', self)
        self.dropdownlist0 = QComboBox(self)
        self.dropdownlist1 = QComboBox(self)
        
        self.cb_pin0.setFont(QFont('Arial', 20))
        self.cb_pin1.setFont(QFont('Arial', 20))
        self.dropdownlist0.setFont(QFont('Times', 12))
        self.dropdownlist1.setFont(QFont('Times', 12))
        self.cb_pin0.setGeometry(int(width*2/10),int(height*8/20),100,30)
        self.cb_pin1.setGeometry(int(width*2/10),int(height*10/20),100,30)
        self.dropdownlist0.setGeometry(int(width*4/10), int(height*8/20), 130, 30)
        self.dropdownlist1.setGeometry(int(width*4/10), int(height*10/20), 130, 30)
        self.cb_pin0.toggle() # default setting
        self.dropdownlist1.setEnabled(False)

        # run button
        self.runbtn = QPushButton('RUN!', self)
        self.runbtn.setFont(QFont('Times', 15))
        self.runbtn.setGeometry(int(width*4/10), int(height*13/20), 100, 40)

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
        self.runbtn.clicked.connect(self.runDisplay)
        
        self.check=False
        self.runbtn.setEnabled(False)
    
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
        self.path, self.check = QFileDialog.getOpenFileName(None,"Choose a load file","","CSV Files (*.csv);;Text Files (*.txt)")
        if self.check:
            self.path_text.setText('Path: '+str(self.path))
            self.clearElement()
            with open(self.path) as f:
                reader = csv.reader(f)
                header = reader.__next__()
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

        # python[] display.py[0] 'path'[1] pin0(T/F)[2] pin0index[3] pin1(T/F)[4] pin1index[5]
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
        self.runbtn.setEnabled(True)

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
        self.setGeometry(200,100,600,900)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainGUI()
    sys.exit(app.exec_())