import pyaudio
import numpy
import math
from scipy.signal import lfilter
import spl_lib as spl

#Each chuck of array recorded
CHUNK = 9600
FORMAT = pyaudio.paInt16
#mono
CHANNELS = 1
#fs must be 44100 because of mic
RATE = 44100
#A-weighting
NUMERATOR, DENOMINATOR = spl.A_weighting(RATE)


class Recorder(object):

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream1 = self.open_pyaudio_stream(2)
        self.stream2 = self.open_pyaudio_stream(3)

    def open_pyaudio_stream(self,index):
        steam = self.p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input_device_index=index,
                            input=True,
                            frames_per_buffer=CHUNK)

        return steam

    def list_all_device(self):
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            print((i, dev['name'], dev['maxInputChannels']))

    def record(self,record_seconds):
        # RATE => frame per second
        # CHUNK => frame per buffer
        # RATE /CHUNK => buffer per second
        # RATE / CHUNK * SECOND => buffer

        for i in range(0, int(RATE / CHUNK * record_seconds)):
            data1 = self.stream1.read(CHUNK, exception_on_overflow=False)
            data2 = self.stream2.read(CHUNK, exception_on_overflow=False)
            decibel1 = self.to_decibel(data1)
            decibel2 = self.to_decibel(data2)
        return decibel1,decibel2

    def terminate(self):
        self.stream1.stop_stream()
        self.stream1.close()
        self.stream2.stop_stream()
        self.stream2.close()
        self.p.terminate()

    def to_decibel(self,data_chunk):

        # Int16 is a numpy data type which is Integer (-32768 to 32767)
        # If you put Int8 or Int32, the result numbers will be ridiculous
        decoded_block = numpy.fromstring(data_chunk, 'Int16')

        # This is where you apply A-weighted filter
        y = lfilter(NUMERATOR, DENOMINATOR, decoded_block)
        new_decibel = 20 * numpy.log10(spl.rms_flat(y))
        return new_decibel

    def sum_decibel(self,d1,d2):
        #sum of decibel cannot just sum
        return 10 * math.log10(10 ** (d1 / 10) + 10 ** (d2 / 10))

    def avg_decibel(self,d1,d2):
        #decibel division cannot just divide
        return self.sum_decibel(d1,d2) - (10 * math.log10(2))