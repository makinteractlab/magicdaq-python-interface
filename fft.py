import time
import csv
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from scipy import signal

def calc_amp(data, fs):
    '''フーリエ変換して振幅スペクトルを計算する関数
    '''
    N = len(data)
    window = signal.hann(N)
    F = np.fft.fft(data * window)
    freq = np.fft.fftfreq(N, d=1/fs) # 周波数スケール
    F = F / (N / 2) # フーリエ変換の結果を正規化
    F = F * (N / sum(window)) # 窓関数による振幅減少を補正する
    Amp = np.abs(F) # 振幅スペクトル
    return Amp, freq

def butter_lowpass(lowcut, fs, order=4):
    
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = signal.butter(order, low, btype='low')
    return b, a


def butter_lowpass_filter(x, lowcut, fs, order=4):
    
    b, a = butter_lowpass(lowcut, fs, order=order)
    y = signal.filtfilt(b, a, x)
    return y
'''
N = 1024            # サンプル数
dt = 0.0005          # サンプリング周期 [s]
fs = 1 / dt         # サンプリング周波数 [Hz]
f1, f2, f3 = 30, 432, 604    # サンプルデータの周波数 [Hz]

t = np.arange(0, N * dt, dt) # 時間 [s]
x = 1.5 * np.sin(2 * np.pi * f1 * t) \
    + 0.5 * np.sin(2 * np.pi * f2 * t) \
    + 0.7 * np.sin(2 * np.pi * f3 * t) # データ
print(x)
'''
with open('./assets/20Hz.csv') as f:
    reader = csv.reader(f)
    arr = [row for row in reader]
ch1 = np.array(arr)[1:, 1:2]
ch1 = np.array([float(ch1[i][0])for i in range(len(ch1))])

N = len(ch1) # the number of data
dt = 0.001 
fs = 1 / dt #frquency
t = np.arange(0, N * dt, dt)
x = ch1
last = float(np.array(arr)[len(arr)-1:len(arr), :1][0][0])

y = butter_lowpass_filter(x, 100, fs, order=4)
print(y)
fig, ax = plt.subplots()
ax.plot(t, x, label='raw data')
ax.plot(t, y, label='filtered')
ax.set_xlabel("Time [s]")
ax.set_ylabel("Signal")
ax.set_xlim([0, 1])
ax.grid()
plt.legend(loc='best')
plt.show()

Amp, freq = calc_amp(x, fs)
fig, ax = plt.subplots(1,2)
ax[0].plot(freq[:N//2], Amp[:N//2])
ax[0].set_xlabel("Frequency [Hz]")
ax[0].set_ylabel("Amplitude")
ax[0].set_title('raw data')
ax[0].grid()
Amp_filt, freq_filt = calc_amp(y, fs)
ax[1].plot(freq_filt[:N//2], Amp_filt[:N//2])
ax[1].set_xlabel("Frequency [Hz]")
ax[1].set_ylabel("Amplitude")
ax[1].set_title('filtered')
ax[1].grid()
plt.tight_layout()
plt.show()