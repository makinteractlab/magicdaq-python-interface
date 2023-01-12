# in this file, we can display the wave from the data created in write.py
from magicdaq.api_class import MagicDAQDevice
import time
import csv
import numpy as np
import pandas as pd
import sys
from distutils.util import strtobool
from scipy import signal

def calc_amp(data, fs):
    # calculate amplitude spectrum after FFT
    
    N = len(data)
    window = signal.hann(N)
    F = np.fft.fft(data * window)
    freq = np.fft.fftfreq(N, d=1/fs) # frequency scale
    F = F / (N / 2) # フーリエ変換の結果を正規化
    F = F * (N / sum(window)) # 窓関数による振幅減少を補正する
    Amp = np.abs(F) # amplitude spectrum
    return Amp, freq

def butterWorthLow(lowcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = signal.butter(order, low, btype='low')
    return b, a
def butterWorthHigh(lowcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = signal.butter(order, low, btype='high')
    return b, a

def butterLowPassFilter(x, lowcut, fs, order=4):
    b, a = butterWorthLow(lowcut, fs, order=order)
    y = signal.filtfilt(b, a, x)
    return y

def butterHighPassFilter(x, lowcut, fs, order=4):
    b, a = butterWorthHigh(lowcut, fs, order=order)
    y = signal.filtfilt(b, a, x)
    return y

print('--- Start -----------------------')
#import csv data
with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    arr = [row for row in reader]

# Create daq_one object
daq_one = MagicDAQDevice()

# Connect to the MagicDAQ
daq_one.open_daq_device()

# set index number of data that output from AO0 and AO1 (being able to choose 2 data at most)
''' 
pin0(T/F)[2] pin0Aindex[3] pin0symbolIndex[4] pin0Bindex[5] pin0filterIndex[6]
pin1(T/F)[7] pin1Aindex[8] pin1symbolIndex[9] pin1Bindex[10] pin1filterIndex[11]'''
pin0_bool = strtobool(sys.argv[2])
pin0_A = int(sys.argv[3]) + 1
pin0_symbol = int(sys.argv[4])
pin0_B = int(sys.argv[5]) + 1
pin0_filter = int(sys.argv[6])

pin1_bool = strtobool(sys.argv[7])
pin1_A = int(sys.argv[8]) + 1
pin1_symbol = int(sys.argv[9])
pin1_B = int(sys.argv[10]) + 1
pin1_filter = int(sys.argv[11])

print('Config data ....')
print('')

# --------------configure data -----------------------
arrT = np.array(arr).T #[[time, time, ... ], [data1_0, data1_1, ...], [data2_0, data2_1, ...], ...]
threshold_time = 0.01 #(sec) time duration
threshold_voltage = 0.3 #(V)

t = np.array(arr)[1:, 0:1]
t = np.array([float(t[i][0]) for i in range(len(t))]).T
dt = float(arrT[0][2]) - float(arrT[0][1])
fs = int(1/dt)

# down scale when max Voltage is more than 5[V] or min Voltage is less than 0[V]
def modifyData(array):
    '''shape: [vol0, vol1, ...]'''

    # if minimum is less than 0[V], adjust the data so that the minimum value of the data is 0[V].
    if (min_value := min(array)) < 0:
        for i in range(len(array)):
            array[i] = round(array[i] + abs(min_value), 3)
    #if maximum of data is more than 5[V], adjust the range of voltages in the data to be 0[V] to 5[V]
    if (max_value := max(array)) > 5:
        for i in range(len(array)):
            array[i] = round(array[i] * 5 / max_value, 3)
    return array


# compile section
if pin0_bool:
    arr_A = np.array(arr)[1:, pin0_A:pin0_A+1]
    arr_A = np.array([float(arr_A[i][0]) for i in range(len(arr_A))]).T
    arr_B = np.array(arr)[1:, pin0_B:pin0_B+1]
    arr_B = np.array([float(arr_B[i][0]) for i in range(len(arr_B))]).T

    # first, it's filtered by filter variable
    if pin0_filter == 1: # Low Pass Filter
        arr_A = butterLowPassFilter(arr_A, 100, fs, order=4)
        arr_B = butterLowPassFilter(arr_B, 100, fs, order=4)
        arr_A = modifyData(arr_A)
        arr_B = modifyData(arr_B)
    if pin0_filter == 2: # High Pass Filter
        arr_A = butterHighPassFilter(arr_A, 100, fs, order=4)
        arr_B = butterHighPassFilter(arr_B, 100, fs, order=4)
        arr_A = modifyData(arr_A)
        arr_B = modifyData(arr_B)

    # symbol check
    if pin0_symbol == 0:
        ch1 = [['0']] * len(arr_A)
        for i in range(0, len(arr_A)):
            ch1[i] = [str(min(5, float(arr_A[i])))]

        ch1 = np.array(np.vstack([np.array([t]), np.array([arr_A])])).T
        for i in range(len(arr)-1):
            if not(i >= len(arr)-2):
                j = i + 1
                while ch1[j][0] - ch1[i][0] < threshold_time:
                    if abs(ch1[i][1] - ch1[j][1] < threshold_voltage):
                        ch1[j] = ch1[i]
                        break
                    j+=1
                    if(j >= len(arr)-1):
                        break
        ch1 = np.unique(ch1, axis=0)
        ch1 = ch1.tolist()
    else: 
        ch1 = [['0']] * len(arr_A)

        if pin0_symbol == 1: #addition (a+b)
            for i in range(0, len(arr_A)):
                ch1[i] = [str(min(5, float(arr_A[i]) + float(arr_B[i])))]
        elif pin0_symbol == 2: # subtraction(a-b)
            for i in range(0, len(arr_A)):
                ch1[i] = [str(max(0, float(arr_A[i]) - float(arr_B[i])))]
        elif pin0_symbol == 3: # multiplication(a*b)
            for i in range(0, len(arr_A)):
                ch1[i] = [str(min(5, float(arr_A[i]) * float(arr_B[i])))]

        ch1 = np.array(np.vstack([np.array([t]), np.array([arr_A])])).T
        for i in range(len(arr)-1):
            if not(i >= len(arr)-2):
                j = i + 1
                while ch1[j][0] - ch1[i][0] < threshold_time:
                    if abs(ch1[i][1] - ch1[j][1] < threshold_voltage):
                        ch1[j] = ch1[i]
                        break
                    j+=1
                    if(j >= len(arr)-1):
                        break
        ch1 = np.unique(ch1, axis=0)
        ch1 = ch1.tolist()

if pin1_bool:
    arr_A = np.array(arr)[1:, pin1_A:pin1_A+1]
    arr_A = np.array([float(arr_A[i][0]) for i in range(len(arr_A))]).T
    arr_B = np.array(arr)[1:, pin1_B:pin1_B+1]
    arr_B = np.array([float(arr_B[i][0]) for i in range(len(arr_B))]).T

    # first, it's filtered by filter variable
    if pin1_filter == 1: # Low Pass Filter
        arr_A = butterLowPassFilter(arr_A, 100, fs, order=4)
        arr_B = butterLowPassFilter(arr_B, 100, fs, order=4)
        arr_A = modifyData(arr_A)
        arr_B = modifyData(arr_B)
    if pin1_filter == 2: # High Pass Filter
        arr_A = butterHighPassFilter(arr_A, 100, fs, order=4)
        arr_B = butterHighPassFilter(arr_B, 100, fs, order=4)
        arr_A = modifyData(arr_A)
        arr_B = modifyData(arr_B)

    if pin1_symbol == 0:
        ch2 = [['0']] * len(arr_A)
        for i in range(0, len(arr_A)):
            ch2[i] = [str(min(5, float(arr_A[i])))]

        ch2 = np.array(np.vstack([np.array([t]), np.array([arr_A])])).T
        for i in range(len(arr)-1):
            if not(i == len(arr)-2):
                j = i + 1
                while ch2[j][0] - ch2[i][0] < threshold_time:
                    if abs(ch2[i][1] - ch2[j][1] < threshold_voltage):
                        ch2[j] = ch2[i]
                        break
                    j+=1
                    if(j >= len(arr)-1):
                        break
        ch2 = np.unique(ch2, axis=0)
        ch2 = ch2.tolist()
    
    else:
        ch2 = [['0']] * len(arr_A)

        if pin1_symbol == 1: #addition (a+b)
            for i in range(0, len(arr_A)):
                ch2[i] = [str(min(5, float(arr_A[i]) + float(arr_B[i])))]
        elif pin1_symbol == 2: # subtraction(a-b)
            for i in range(0, len(arr_A)):
                ch2[i] = [str(max(0, float(arr_A[i]) - float(arr_B[i])))]
        elif pin1_symbol == 3: # multiplication(a*b)
            for i in range(0, len(arr_A)):
                ch2[i] = [str(min(5, float(arr_A[i]) * float(arr_B[i])))]

        ch2 = np.array(np.vstack([np.array([t]), np.array([arr_A])])).T
        for i in range(len(arr)-1):
            if not(i == len(arr)-2):
                j = i + 1
                while ch2[j][0] - ch2[i][0] < threshold_time:
                    if abs(ch2[i][1] - ch2[j][1] < threshold_voltage):
                        ch2[j] = ch2[i]
                        break
                    j+=1
                    if(j >= len(arr)-1):
                        break
        ch2 = np.unique(ch2, axis=0)
        ch2 = ch2.tolist()

print('Compile Done.')

#Calculate duration
end_time = float(np.array(arr)[-1, 0:1])
print('Endtime: ' + str(end_time))

index_1 = 0
index_2 = 0

#last check


#------------- Demo part ----------------------------
print('Doing DEMO!!')
if pin0_bool and not pin1_bool:
    start = time.time()
    while (duration := time.time() - start) < end_time:
        if(duration > ch1[index_1][0]):
            daq_one.set_analog_output(0, ch1[index_1][1])
            index_1 = min(index_1+1, len(ch1) - 1)
    print('--- Display Completed. ---')
    if(index_1 < len(ch1)-1):print('ERROR!! could not demo in same time')    


elif not pin0_bool and pin1_bool:
    start = time.time()
    while (duration := time.time() - start) < end_time:
        if(duration > ch2[index_2][0]):
            daq_one.set_analog_output(1, ch2[index_2][1])
            index_2 = min(index_2+1, len(ch2) - 1)
    print('--- Display Completed. ---')
    if(index_2 < len(ch2)-1):print('ERROR!! could not demo in same time')    


elif pin0_bool and pin1_bool:
    start = time.time()
    while (duration := time.time() - start) < end_time + 0.1:
        if(duration > ch1[index_1][0]):
            daq_one.set_analog_output(0, ch1[index_1][1])
            index_1 = min(index_1+1, len(ch1) - 1)
        if(duration > ch2[index_2][0]):
            daq_one.set_analog_output(1, ch2[index_2][1])
            index_2 = min(index_2+1, len(ch2) - 1)
    print('--- Display Completed. ---')
    if(index_1 < len(ch1)-1 and index_2 < len(ch2)-1):print('ERROR!! could not demo in same time\nindex1: '+str(index_1)+', index2: '+str(index_2)+', total: '+str(len(ch1)))
else :
    print('ERROR! Both pins do not selected')

# Now stopping the output waves
daq_one.stop_analog_output_wave(0)
daq_one.stop_analog_output_wave(1)

# We are done using the MagicDAQ, so close it
daq_one.close_daq_device()