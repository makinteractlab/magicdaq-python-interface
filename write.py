from magicdaq.api_class import MagicDAQDevice
import time
import csv
import sys

Pins = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]]
streaming_frequency = int(sys.argv[9])
duration = int(sys.argv[10])
filename = sys.argv[11]
folderPath = sys.argv[12]

# Pin configure
selected_pin = [i for i in range(0,len(Pins)) if Pins[i] == 'True']

# Create daq_one object
daq_one = MagicDAQDevice()

# Connect to the MagicDAQ
daq_one.open_daq_device()

start = time.time()

csv_log_file = open(folderPath+'/'+filename+'.csv', 'w+', newline="")
csv_writer = csv.writer(csv_log_file)
#log_file_header = ['Time (Sec)', 'Analog Input 0', 'Analog Input 1', 'Analog Input 4']
log_file_header = ['Time (Sec)']
for l in selected_pin:
    log_file_header.append('Analog Input '+str(l))
csv_writer.writerow(log_file_header)

#being able to input by multiple pin
daq_one.configure_analog_input_stream(selected_pin,streaming_frequency)

print('--- Starting Test (Fast Data Acquisition) ---')
print('Streaming Frequency (Hz): ', streaming_frequency)
print('Measuring Duration (Sec): ', duration)
print('')

total_test_time_sec = 1
test_start_time = time.time()
daq_one.start_analog_input_stream()

while (time.time() < (test_start_time + (total_test_time_sec * duration)) ):
    latest_samples = daq_one.get_last_n_streaming_data_samples(1)
    if len(latest_samples[0])>=1 and len(latest_samples[1])>=1:
        print('Analog Input 0: ',latest_samples[0][0], ' Analog Input 1: ',latest_samples[1][0], ' Analog Input 4: ',latest_samples[2][0])
    print('Will print latest sample in 1 sec.')
    print('')
    time.sleep(1)

daq_one.stop_analog_input_stream()

# Total length of test
print('Total Test Time (sec): ', round((time.time() - test_start_time),3) )

all_streaming_data = daq_one.get_full_streaming_data_buffer()
print('Number of data points gathered for each analog input: ', len(all_streaming_data[0]))

data_index = 0
while data_index < len(all_streaming_data[0]):
    # Calculate time at this data point (sec)
    time_at_data_point = round((data_index *(1/streaming_frequency)),3)

    # save data to CSV
    csv_writer.writerow([time_at_data_point, all_streaming_data[0][data_index], all_streaming_data[1][data_index], all_streaming_data[2][data_index]])
    data_index += 1

daq_one.close_daq_device()
print('')
print ('--- Test Complete ---')
csv_log_file.close()