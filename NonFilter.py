#!/usr/bin/env python
# encoding: utf-8

import matplotlib.pyplot as plt

## Module infomation ###
# Python (3.4.4)
# numpy (1.10.2)
# PyAudio (0.2.9)
# matplotlib (1.5.1)
# All 32bit edition
########################
import numpy as np
import pyaudio


class SpectrumAnalyzer:
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 16000
    CHUNK = 2048
    START = 0
    N = 2048

    wave_x = 0
    wave_y = 0
    spec_x = 0
    spec_y = 0

    data = []

    def __init__(self):
        self.pa = pyaudio.PyAudio()

    def start(self):
        self.stream = self.pa.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=False,
            frames_per_buffer=self.CHUNK,
        )
        self.is_running = True
        # Main loop
        self.loop()

    def stop(self):
        self.is_running = False
        self.stream.close()
        self.pa.close(stream=self.stream)

    def loop(self):
        try:
            while self.is_running:
                self.data = self.audioinput()
                self.fft()
                self.graphplot()

        except KeyboardInterrupt:
            self.pa.close(stream=self.stream)

        print("End...")

    def audioinput(self):
        ret = self.stream.read(self.CHUNK)
        ret = np.frombuffer(ret, np.float32)
        return ret

    def fft(self):
        self.wave_x = range(self.START, self.START + self.N)
        self.wave_y = self.data[self.START : self.START + self.N]
        self.spec_x = np.fft.fftfreq(self.N, d=1.0 / self.RATE)
        y = np.fft.fft(self.data[self.START : self.START + self.N])
        self.spec_y = [np.sqrt(c.real**2 + c.imag**2) for c in y]

    def graphplot(self):
        plt.clf()
        # wave
        plt.subplot(311)
        plt.plot(self.wave_x, self.wave_y)
        plt.axis([self.START, self.START + self.N, -1, 1])
        plt.xlabel("time [sample]")
        plt.ylabel("amplitude")
        # Spectrum
        plt.subplot(312)
        plt.plot(self.spec_x, self.spec_y, marker="", linestyle="-")
        plt.axis([0, self.RATE / 2, 0, 50])
        plt.xlabel("frequency [Hz]")
        plt.ylabel("amplitude spectrum")
        # Pause
        plt.pause(0.01)
