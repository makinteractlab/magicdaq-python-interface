import os
import csv
import sys
import numpy as np
import time, datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def judgeNumber(num):
    for i in range(8):
        if num == str(i):
            return True
    return False

sys_len = len(sys.argv)

# if input is only "python command.py", you can use interaction system in command.
if sys_len == 1:
    method = input("Measure or Display?(answer m/d): ")

    if method == "M" or method == "m":
        print("------  MEASURE  ------")
        pin = list(map(int, input("Enter measured analog pin index(0-7): ").split()))
        pin = list(set(pin))
        if max(pin)> 7 or min(pin)<0:
            print("ERROR! You must enter the appropriate values.")
            sys.exit()
        else:
            frequency, duration = map(int, input("Frequency(Hz, 1-5000) and time duration(s, 1-10): ").split())
            folder_path = input("Enter saved directory name (access a directory at a lower level or create a new directory): ")
            if os.path.exists(folder_path):
                print("Succeeded in access directory.")
            else:
                os.mkdir(folder_path)
                if os.path.exists(folder_path):
                    print("Made new directory.")
                else:
                    print("ERROR! You must enter the appropriate values.")
                    sys.exit()
            file_name = input("Enter file name: ")

            Pins = ["0"] * 8
            for i in range(8):
                if i in pin:
                    Pins[i] = "True"
                else :
                    Pins[i] = "False"

            now = datetime.datetime.fromtimestamp(time.time())
            date = now.strftime("-%Y-%m-%d-%H-%M-%S")
            os.system('python write.py '
                    + Pins[0]+' '+Pins[1]+' '+Pins[2]+' '+Pins[3]+' '+Pins[4]+' '+Pins[5]+' '+Pins[6]+' '+Pins[7]+' '
                    + ' '
                    + str(frequency)
                    + ' '
                    + str(duration)
                    + ' '
                    + file_name
                    + ' '
                    + folder_path
                    + ' '
                    + date
                    )
            
            view = input("Do you want to check graph? (y/n): ")
            if view == "Y" or view == "y":
                with open(folder_path+'/' + file_name + date + '.csv') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    arr = [row for row in reader]
                data = np.array(np.array(arr)[1:, :]).T
                '''data: [[time0, time1, ...], [data0_0, data0_1, ...], ...]'''

                col = ["black", "blue", "red", "green", "purple", "yellow", "brown", "pink"]
                time = data[0].astype(np.float32)
                fig, ax = plt.subplots()
                ax.set_xlabel("Time [s]")
                ax.set_ylabel("Voltage[V]")
                ax.set_title('Measured Voltage Data')
                ax.set_xlim([0, float(data[0][-1])])
                ax.set_ylim([0, 5])
                ax.grid()
                for i in range(1,len(data)):
                    ax.plot(time, data[i].astype(np.float32), color=col[i-1], label=header[i])
                ax.legend(loc=0)
                fig.tight_layout()
                plt.show()
            elif view != "n" and view != "N":
                print("Graph was not displayed because your input was inappropriate.")
            
            save = input("Save data or Dismiss data? (s/d): ")
            if save == "s" or save == "S":
                print("Data was properly saved.")
            else:
                os.remove(folder_path+'/' + file_name + date + '.csv')
                if save == "d" or save == "D":
                    print("Data was deleted.")
                else :
                    print("Data was deleted because your input was inappropriate.")

    elif method == "D" or method == "d":
        print("------  DISPLAY  ------")
        file_path = input("Enter load file path: ")
        if os.path.exists(file_path):
            with open(file_path) as f:
                    reader = csv.reader(f)
                    header = reader.__next__()
            header_text = "0:(" + header[1] + ")"
            for i in range(2, len(header)):
                header_text = header_text + ", " + str(i-1) + ":("+ header[i] + ")"
            ao0 = input("Is the AO0 pin used for displaying? (y/n): ")
            ao1 = input("Is the AO1 pin used for displaying? (y/n): ")
            if not (ao0 == "y" or ao0 == "Y") and not (ao1 == "y" or ao1 == "Y"):
                print("ERROR! you must choose AO0 or AO1 pins at least one.")
                sys.exit()

            a,b,c,d,filter0,filter1,option0,option1 = 0,0,0,0,0,0,'0','0'
            if ao0 == "y" or ao0 == "Y":
                ao0 = "True"
                print("(AO0) The output of a pin can be a single voltage data or the result of two voltage calculations (single, addition, subtraction, multiplication).")
                option0 = input("(AO0) What about the pins to output? (s:single, p:addition, m:subtraction, t:multiplication): ")
                if option0 == "s" or option0 == "S":
                    option0 = '0'
                    print('Selectable voltage data: ' + header_text)
                    a = int(input('(AO0) Specify the input data to be output. The only input value is the numerical value of each index. : '))
                    if not(a >=0 and a<len(header)):
                        print("ERROR! You must enter the appropriate values.")
                        sys.exit()
                elif option0 == "a" or option0 == "A" or option0 == "m" or option0 == "M" or option0 == "t" or option0 == "T":
                    print('Selectable voltage data: ' + header_text)
                    print("The only input value is the numerical value of each index.")
                    print("The inputs are as follows,")
                    if option0 == "a" or option0 == "A":
                        option0 = '1'
                        print("ex) if you want to try '3 + 4', your input is '3 4'")
                    elif option0 == "m" or option0 == "M":
                        option0 = '2'
                        print("ex) if you want to try '3 - 4', your input is '3 4'")
                    elif option0 == "t" or option0 == "T":
                        option0 = '3'
                        print("ex) if you want to try '3 * 4', your input is '3 4'")
                    a, b = map(int, input("(AO0) Specify the two input data to be output: ").split())
                else:
                    print("ERROR! You must enter the appropriate values.")
                    sys.exit()
                filter0 = int(input("(AO0) Which filter do you choose? (None:0, LowPassFilter:1, HighPassFilter:2): "))
            else :
                ao0 = "False"

            if ao1 == "y" or ao1 == "Y":
                ao1 = "True"
                print("(AO1) The output of a pin can be a single voltage data or the result of two voltage calculations (single, addition, subtraction, multiplication).")
                option1 = input("(AO1) What about the pins to output? (s:single, p:addition, m:subtraction, t:multiplication): ")
                if option1 == "s" or option1 == "S":
                    option1 = '0'
                    print('Selectable voltage data: ' + header_text)
                    c = int(input('(AO1) Specify the input data to be output. The only input value is the numerical value of each index. : '))
                    if not(c >=0 and c<len(header)):
                        print("ERROR! You must enter the appropriate values.")
                        sys.exit()
                elif option1 == "a" or option1 == "A" or option1 == "m" or option1 == "M" or option1 == "t" or option1 == "T":
                    print('Selectable voltage data: ' + header_text)
                    print("The only input value is the numerical value of each index.")
                    print("The inputs are as follows,")
                    if option1 == "a" or option1 == "A":
                        option1 = '1'
                        print("ex) if you want to try '3 + 4', your input is '3 4'")
                    elif option1 == "m" or option1 == "M":
                        option1 = '2'
                        print("ex) if you want to try '3 - 4', your input is '3 4'")
                    elif option1 == "t" or option1 == "T":
                        option1 = '3'
                        print("ex) if you want to try '3 * 4', your input is '3 4'")
                    c,d = map(int, input("(AO1) Specify the two input data to be output: ").split())
                    if not(c >=0 and c<len(header) and d >= 0 and d<len(header)):
                        print("ERROR! You must enter the appropriate values.")
                        sys.exit()
                else:
                    print("ERROR!")
                    sys.exit()
                filter1 = int(input("(AO1) Which filter do you choose? (None:0, LowPassFilter:1, HighPassFilter:2): "))
            else:
                ao1 = "False"

            ''' python[] display.py[0] 'path'[1] 
                pin0(T/F)[2] pin0Aindex[3] pin0symbolIndex[4] pin0Bindex[5] pin0filterIndex[6]
                pin1(T/F)[7] pin1Aindex[8] pin1symbolIndex[9] pin1Bindex[10] pin1filterIndex[11]'''
            os.system("python display.py "+file_path + ' '
                    + ao0 + ' ' + str(a) + ' ' + option0 + ' ' + str(b) + ' ' + str(filter0) + ' '
                    + ao1 + ' ' + str(c) + ' ' + option1 + ' ' + str(d) + ' ' + str(filter1)
            )

        else:
            print("There is no such a file in your computer!")
            sys.exit()

    else:
        print("ERROR! you must choose m or d.")
        sys.exit()

else:
    measure = '-m' in sys.argv
    display = '-d' in sys.argv
    if not ((measure and not display) or (not measure and display)):
        print("ERROR! you must enter only one of '-m' or '-d'")
        sys.exit()
    
    if measure:
        #default settings
        frequency = 250
        duration = 3
        folder_path = 'data'
        file_name = 'sample'
        pin = [0,1,2,3]
        view_on = False

        if '-f' in sys.argv:
            index = sys.argv.index('-f')
            if index+1 < len(sys.argv) and sys.argv[index+1].isdecimal():
                frequency = sys.argv[index+1]
        if '-t' in sys.argv:
            index = sys.argv.index('-t')
            if index+1 < len(sys.argv) and sys.argv[index+1].isdecimal():
                duration = sys.argv[index+1]
        if '-i' in sys.argv:
            index = sys.argv.index('-i')
            pin = []
            while index+1 < len(sys.argv) and judgeNumber(sys.argv[index+1]):
                pin.append(int(sys.argv[index+1]))
                index += 1
            if len(pin) == 0:
                pin = [0,1,2,3]
        if '-folder' in sys.argv:
            index = sys.argv.index('-folder')
            if index+1 < len(sys.argv) and os.path.exists(sys.argv[index+1]):
                folder_path = sys.argv[index+1]
        if '-file' in sys.argv:
            index = sys.argv.index('-file')
            if index+1 < len(sys.argv):
                file_name = sys.argv[index+1]
        if '-v' in sys.argv:
            view_on = True

        Pins = ["0"] * 8
        for i in range(8):
            if i in pin:
                Pins[i] = "True"
            else :
                Pins[i] = "False"
        now = datetime.datetime.fromtimestamp(time.time())
        date = now.strftime("-%Y-%m-%d-%H-%M-%S")
        os.system('python write.py '
                + Pins[0]+' '+Pins[1]+' '+Pins[2]+' '+Pins[3]+' '+Pins[4]+' '+Pins[5]+' '+Pins[6]+' '+Pins[7]+' '
                + ' '
                + str(frequency)
                + ' '
                + str(duration)
                + ' '
                + file_name
                + ' '
                + folder_path
                + ' '
                + date
                )
        
        if view_on:
            with open(folder_path+'/' + file_name + date + '.csv') as f:
                reader = csv.reader(f)
                header = next(reader)
                arr = [row for row in reader]
            data = np.array(np.array(arr)[1:, :]).T
            '''data: [[time0, time1, ...], [data0_0, data0_1, ...], ...]'''

            col = ["black", "blue", "red", "green", "purple", "yellow", "brown", "pink"]
            time = data[0].astype(np.float32)
            fig, ax = plt.subplots()
            ax.set_xlabel("Time [s]")
            ax.set_ylabel("Voltage[V]")
            ax.set_title('Measured Voltage Data')
            ax.set_xlim([0, float(data[0][-1])])
            ax.set_ylim([0, 5])
            ax.grid()
            for i in range(1,len(data)):
                ax.plot(time, data[i].astype(np.float32), color=col[i-1], label=header[i])
            ax.legend(loc=0)
            fig.tight_layout()
            plt.show()

    elif display:
        file_name = ""
        filter_list = ['none', 'low', 'high']
        option_list = ['+', '-', '*']
        a,b,c,d,filter0,filter1,option0,option1,ao0,ao1 = 0,0,0,0,0,0,'0','0','False','False'
        if '-file' in sys.argv:
            index = sys.argv.index('-file')
            if index+1 < len(sys.argv) and os.path.isfile(sys.argv[index+1]):
                file_name = sys.argv[index+1]
                with open(file_name) as f:
                    reader = csv.reader(f)
                    header = reader.__next__()
                pin_list = [header[i][-1] for i in range(1, len(header))]
            else:
                print("ERROR! You must choose a file.")
                sys.exit()
        else :
            print("ERROR! You must choose a file.")
            sys.exit()

        if '-0' in sys.argv:
            ao0 = 'True'
            index = sys.argv.index('-0')
            if index+2 < len(sys.argv) and sys.argv[index+2] in filter_list:
                formula = sys.argv[index+1]
                if len(formula) == 1 and judgeNumber(formula):
                    a = pin_list.index(sys.argv[index+1])
                elif len(formula) == 3 and judgeNumber(formula[0]) and judgeNumber(formula[2]) and formula[1] in option_list:
                    a = pin_list.index(formula[0])
                    b = pin_list.index(formula[2])
                    option0 = option_list.index(formula[1])
                filter0 = filter_list.index(sys.argv[index+2])
            elif index+1 < len(sys.argv):
                formula = sys.argv[index+1]
                if len(formula) == 1 and judgeNumber(formula):
                    a = pin_list.index(sys.argv[index+1])
                elif len(formula) == 3 and judgeNumber(formula[0]) and judgeNumber(formula[2]) and formula[1] in option_list:
                    a = pin_list.index(formula[0])
                    b = pin_list.index(formula[2])
                    option0 = option_list.index(formula[1])

        if '-1' in sys.argv:
            ao1 = 'True'
            index = sys.argv.index('-1')
            if index+2 < len(sys.argv) and sys.argv[index+2] in filter_list:
                formula = sys.argv[index+1]
                if len(formula) == 1 and judgeNumber(formula):
                    c = pin_list.index(sys.argv[index+1])
                elif len(formula) == 3 and judgeNumber(formula[0]) and judgeNumber(formula[2]) and formula[1] in option_list:
                    c = pin_list.index(formula[0])
                    d = pin_list.index(formula[2])
                    option1 = option_list.index(formula[1])
                filter1 = filter_list.index(sys.argv[index+2])
            elif index+1 < len(sys.argv):
                formula = sys.argv[index+1]
                if len(formula) == 1 and judgeNumber(formula):
                    c = pin_list.index(sys.argv[index+1])
                elif len(formula) == 3 and judgeNumber(formula[0]) and judgeNumber(formula[2]) and formula[1] in option_list:
                    c = pin_list.index(formula[0])
                    d = pin_list.index(formula[2])
                    option1 = option_list.index(formula[1])

        os.system("python display.py "+file_name + ' '
            + ao0 + ' ' + str(a) + ' ' + str(option0)+ ' ' + str(b) + ' ' + str(filter0) + ' '
            + ao1 + ' ' + str(c) + ' ' + str(option1) + ' ' + str(d) + ' ' + str(filter1)
            )