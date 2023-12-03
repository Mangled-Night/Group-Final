import tempfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as sio
from pydub import AudioSegment
import taglib
import math

class Controller:
    _file = None
    _channel = None
    _tags = []

    def LoadFile(self, uFile):
        print(uFile)
        parsed_file = uFile.split(".")
        if(parsed_file[-1] == "wav"):
            self.ClearMeta(uFile)
            self._file = uFile
        else:
            try:
                self.ClearMeta(uFile)
                audio = AudioSegment.from_file(uFile)
                name = uFile.split(".")[0] + ".wav"
                self._file = audio.export(format="wav")
            except Exception as err:
                print(f'An error occured "{err}"')
            else:
                samplerate, data = sio.read(self._file)
                self._channels = data.shape[len(data.shape) - 1]

    def ClearMeta(self, file):
        with taglib.File(file, save_on_exit=True) as audio:
            audio.tags.clear()

    def ShowWav(self):
        samplerate, data = sio.read(self._file)
        print(f"number of channels = {data.shape[len(data.shape) - 1]}")
        print(f"sample rate = {samplerate}Hz")
        length = data.shape[0] / samplerate
        print(f"length = {length}s")
        print(data.shape, data.dtype, samplerate)

        print(data[0:20][:, 0])
        print(data[:, 0])
        print(data[:, 1])

        n = 10
        for x in range(0, n):
            start = math.ceil(data.shape[0] * x/n)
            end = math.ceil(data.shape[0] * (x+1)/n)
            l_start = length * x/n
            l_end = length * (x+1)/n
            time = np.linspace(l_start, l_end , (end-start))
            plt.plot(time, data[start:end][:, 0], label="Left channel")
            plt.plot(time, data[start:end][:, 1], label="Right channel")
            plt.legend()
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")
            plt.show()



def main():
    C = Controller()
    C.LoadFile("Sample2.wav")
    C.ShowWav()



main()