import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as sio
from pydub import AudioSegment
import taglib
import math

class Controller:
    _file = None
    _channels = None
    _samplerate = None
    _data = None
    _length = None

    def LoadFile(self, uFile):
        print(uFile)
        parsed_file = uFile.split(".")
        if(parsed_file[-1] == "wav"):       #Checks if the file inputted is a wave
            self.ClearMeta(uFile)
            self._file = uFile
        else:                               #Cleans then Converts to Wav if it is not a Wav
            self.ClearMeta(uFile)
            audio = AudioSegment.from_file(uFile)
            name = uFile.split(".")[0] + ".wav"
            self._file = audio.export(format="wav")

        self.GetAudioStats()

    def GetAudioStats(self):
        self._samplerate, self._data = sio.read(self._file)
        self._channels = self._data.shape[len(self._data.shape) - 1]
        self._length = self._data.shape[0] / self._samplerate

    def ClearMeta(self, file):
        with taglib.File(file, save_on_exit=True) as audio:
            audio.tags.clear()  #Removes Metadata

    def ShowWav(self, start=0, end=0):
        if(end == 0 or end >= self._length):
            end = self._length
            #If user entered nothing or entered a value too great

        #Sets the bounds
        d_start = self._samplerate * start
        d_end = math.ceil(self._samplerate * end)

        #Displays the Data
        time = np.linspace(start, end , (d_end - d_start))
        plt.plot(time, self._data[d_start:d_end][:, 0], label="Left channel")
        plt.plot(time, self._data[d_start:d_end][:, 1], label="Right channel")
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()

    def ShowFrequency(self):
        a1 = plt.subplot(211)
        a1.set_title("Left Channel")
        spectrum1, freqs1, t1, im1 = plt.specgram(self._data[:, 0], Fs= self._samplerate, NFFT=1024, cmap=plt.get_cmap('autumn'))
        cbar1 = plt.colorbar(im1)
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        cbar1.set_label('Intensity (dB)')

        a2 = plt.subplot(212)
        a2.set_title("Right Channel")
        spectrum2, freqs2, t2, im2 = plt.specgram(self._data[:, 1], Fs= self._samplerate, NFFT=1024, cmap=plt.get_cmap('viridis'))
        cbar2 = plt.colorbar(im2)
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        cbar2.set_label('Intensity (dB)')

        plt.show()


def main():
    C = Controller()
    C.LoadFile("Sample2.wav")
    C.ShowWav(5, 10)
    C.ShowFrequency()



main()
