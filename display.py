# in this file, we can display the wave from the data created in write.py
from magicdaq.api_class import MagicDAQDevice
import time
import csv
import numpy as np
import pandas as pd

#import csv data
with open('./analog_input_data.csv') as f:
    reader = csv.reader(f)
    arr = [row for row in reader]

# Create daq_one object
daq_one = MagicDAQDevice()

# Connect to the MagicDAQ
daq_one.open_daq_device()

# set index number of data that output from AO0 and AO1 (being able to choose 2 data at most)
pin0, pin1 = map(int, input('set index data that output pin0 and pin1: ').split())
while not(pin0 > 0 and pin0 < len(arr[1]) and pin1 > 0 and pin1 < len(arr[1])):
    print('missed input')
    pin0, pin1 = map(int, input('set index data that output pin0 and pin1: ').split())

print('Config data ....')
print('')

# --------------configure data -----------------------
arrT = np.array(arr).T #[[time, time, ... ], [data1_0, data1_1, ...], [data2_0, data2_1, ...], ...]
threshold_time = 0.1 #(sec) time duration
threshold_voltage = 0.3 #(V)

t = np.array(arr)[:, 0:1]
ch1 = np.array(arr)[:, pin0:pin0+1]
ch1 = np.hstack([t, ch1])[1:, :].astype(np.float32)
ch2 = np.array(arr)[:, pin1:pin1+1]
ch2 = np.hstack([t, ch2])[1:, :].astype(np.float32)

for i in range(len(arr)-1):
    for j in range(i+1, len(arr)-1):
        if ch1[j][0] - ch1[i][0] < threshold_time:
            if abs(ch1[i][1] - ch1[j][1] < threshold_voltage):
                ch1[j] = ch1[i]
ch1 = np.unique(ch1, axis=0)

for i in range(len(arr)-1):
    for j in range(i+1, len(arr)-1):
        if ch2[j][0] - ch2[i][0] < threshold_time:
            if abs(ch2[i][1] - ch2[j][1] < threshold_voltage):
                ch2[j] = ch2[i]
ch2 = np.unique(ch1, axis=0)
ch1 = ch1.tolist()
ch2 = ch2.tolist()

#Calculate duration
end_time = float(np.array(arr)[-1, 0:1])
print(end_time)

index_1 = 0
index_2 = 0

print('Doing demo!!')
start = time.time()
while (duration := time.time() - start) < end_time:
    if(duration > ch1[index_1][0]):
        daq_one.set_analog_output(0, ch1[index_1][1])
        index_1 = min(index_1+1, len(ch1) - 1)
    if(duration > ch2[index_2][0]):
        daq_one.set_analog_output(0, ch2[index_2][1])
        index_2 = min(index_2+1, len(ch2) - 1)
print('done!')
if(index_1 < len(ch1)-1 and index_2 < len(ch2)-1):print('ERROR!! could not demo in same time')
    

# Now stopping the output waves
daq_one.stop_analog_output_wave(0)
daq_one.stop_analog_output_wave(1)

# We are done using the MagicDAQ, so close it
daq_one.close_daq_device()