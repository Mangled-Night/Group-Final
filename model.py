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
        self._channels = len(self._data.shape)
        self._length = self._data.shape[0] / self._samplerate

    def ClearMeta(self, file):
        with taglib.File(file, save_on_exit=True) as audio:
            audio.tags.clear()  #Removes Metadata

    def ShowWav(self, start=0, end=0):
        if(end == 0 or end >= self._length):
            end = self._length
            #If user entered nothing or entered a value too great

        #Sets the bounds
        d_start = math.ceil(self._samplerate * start)
        d_end = math.ceil(self._samplerate * end)

        if(self._channels == 1):
            # Displays the Data
            time = np.linspace(start, end, (d_end - d_start))
            plt.plot(time, self._data[d_start:d_end], label="Single channel")
            plt.legend()
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")
            plt.show()

        else:
            #Displays the Data
            time = np.linspace(start, end , (d_end - d_start))
            plt.plot(time, self._data[d_start:d_end][:, 0], label="Left channel")
            plt.plot(time, self._data[d_start:d_end][:, 1], label="Right channel")
            plt.legend()
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")
            plt.show()

    def Frequency(self):
        if(self._channels == 1):
            spectrum1, freqs1, t1, im1 = plt.specgram(self._data, Fs=self._samplerate, NFFT=1024, cmap=plt.get_cmap('autumn'))
            cbar1 = plt.colorbar(im1)
            plt.ylabel('Frequency (Hz)')
            cbar1.set_label('Intensity (dB)')
            plt.title("Single Channel")
            plt.show()

        else:
            a1 = plt.subplot(211)
            a1.set_title("Left Channel")
            spectrum1, freqs1, t1, im1 = plt.specgram(self._data[:, 0], Fs= self._samplerate, NFFT=1024, cmap=plt.get_cmap('autumn'))
            cbar1 = plt.colorbar(im1)
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

        self.RT60(freqs1, spectrum1, t1, 1000)
        self.RT60(freqs1, spectrum1, t1, 2000)
        self.RT60(freqs1, spectrum1, t1, 11218)



    def RT60(self, freqs, spectrum, t, target_frequency):
        def frequency_check(target_frequency):
            ratio = spectrum.shape[0]/freqs.max()
            data_for_frequency = spectrum[math.ceil(ratio * target_frequency)]

            data_in_db_fun = 10 * np.log10(data_for_frequency)

            idx_last_pos = 0
            for x in range(len(data_in_db_fun)):
                if(data_in_db_fun[x] > 0):
                    idx_last_pos = x
            pos_data_in_db = data_in_db_fun[:idx_last_pos+1]
            return pos_data_in_db, idx_last_pos

        def HeighestFrequency():
            _max = len(freqs)
            ratio = spectrum.shape[0]/freqs.max()
            heighest_freq = None
            heighest_plottable_freq = None
            for x in range(1, _max):
                _data = 10 * np.log10(spectrum[_max - x])
                idx_last_pos = 0
                for y in range(len(_data)):
                    if (_data[y] > 0):
                        idx_last_pos = y

                if (len(_data[:idx_last_pos + 1]) > 1 and heighest_freq == None):
                    heighest_freq = (_max - x) / ratio

                if(len(_data[:idx_last_pos + 1]) >= 11):
                    heighest_plottable_freq = (_max - x) / ratio
                    break

            return heighest_freq, heighest_plottable_freq



        data_in_db,last_pos = frequency_check(target_frequency)


        plt.figure(2)

        plt.plot(t[:last_pos+1], data_in_db, linewidth=1, alpha=.7, color='#004bc6')

        plt.xlabel('Time (s)')

        plt.ylabel('Power (db)')

        plt.title(f'{target_frequency}Hz')

        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        plt.plot(t[index_of_max], data_in_db[index_of_max], 'go', label="Max")

        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5

        def find_nearest_value(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()

            return array[idx]

        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro', label='Max-25DB')

        sliced_array = data_in_db[index_of_max : index_of_max_less_25[0][0]]
        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo', label='Max-5DB')



        rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])

        rt60 = 3 * rt20

        plt.grid()
        plt.legend()
        plt.show()

        print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {np.round(abs(rt60), 2)[0]} seconds')
        print(f'Amount of audiable sound in this frequency is about {np.round(t[last_pos] - t[0], 2)}s')
        print(f'Heighest audiable frequency is {math.floor(HeighestFrequency()[0])}Hz')
        print(f'Heighest Plottable frequency is {math.floor(HeighestFrequency()[1])}')

def main():
    C = Controller()
    C.LoadFile("Sample5.wav")
    C.ShowWav(0)
    C.Frequency()


main()
