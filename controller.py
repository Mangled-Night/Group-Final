import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as sio
from pydub import AudioSegment
import taglib
import math

class Controller:
    _file = None

    def LoadFile(self, uFile):
        print(uFile)
        parsed_file = uFile.split(".")
        if(parsed_file[-1] == "wav"):       #Checks if the file inputted is a wave
            self.ClearMeta(uFile)
            self._file = uFile
        else:                               #Cleans then Converts to Wav if it is not a Wav
            try:
                self.ClearMeta(uFile)
                audio = AudioSegment.from_file(uFile)
                name = uFile.split(".")[0] + ".wav"
                self._file = audio.export(format="wav")
            except Exception as err:
                print(f'An error occured "{err}"')

    def ClearMeta(self, file):
        with taglib.File(file, save_on_exit=True) as audio:
            audio.tags.clear()  #Removes Metadata

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

        n = 10      #Number of chunks to break the waveform into
        for x in range(0, n):
            #Helps Break the waveform data into chuncks
            start = math.ceil(data.shape[0] * x/n)
            end = math.ceil(data.shape[0] * (x+1)/n)
            l_start = length * x/n
            l_end = length * (x+1)/n

            #Displays the Data
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