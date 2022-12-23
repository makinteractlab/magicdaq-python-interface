from magicdaq.api_class import MagicDAQDevice
import time
import csv

# Create daq_one object
daq_one = MagicDAQDevice()

# Connect to the MagicDAQ
daq_one.open_daq_device()

start = time.time()

csv_log_file = open('analog_input_data.csv', 'w+', newline="")
csv_writer = csv.writer(csv_log_file)
log_file_header = ['Time (Sec)', 'Analog Input 0', 'Analog Input 1', 'Analog Input 4']
csv_writer.writerow(log_file_header)

#define frequency by users
streaming_frequency = int(input("define frequency (Hz): "))
duration = int(input("define duration (Sec): "))

#being able to input by multiple pin
#available pin: 0, 1, 4
daq_one.configure_analog_input_stream([0, 1, 4],streaming_frequency)

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