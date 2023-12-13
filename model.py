import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as sio
from pydub import AudioSegment
import taglib

class Model:
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

    def ReturnStats(self):
        if(self._channels == 1):
            return self._length, self._samplerate, np.max(self._data)
        else:
            return self._length, self._samplerate, np.max(self._data[:,0]) , np.max(self._data[:,1])

    def ClearMeta(self, file):
        with taglib.File(file, save_on_exit=True) as audio:
            audio.tags.clear()  #Removes Metadata

    def ShowWav(self, start=0, end=0):
        if(end == 0 or end >= self._length):
            end = self._length
            #If user entered nothing or entered a value too great

        #Sets the bounds
        d_start = int(self._samplerate * start)
        d_end = int(self._samplerate * end)

        if(self._channels == 1):
            #Makes the plot and returns it
            fig = plt.figure(1)
            time = np.linspace(start, end, (d_end - d_start))
            plt.plot(time, self._data[d_start:d_end], label="Single channel")
            plt.legend()
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")
            return fig

        else:
            #Makes the plot and returns it
            fig = plt.figure(1)
            time = np.linspace(start, end , (d_end - d_start))
            plt.subplot(211)
            plt.plot(time, self._data[d_start:d_end][:, 0], label="Left channel", color='Red')
            plt.ylabel("Amplitude")
            plt.legend()
            plt.subplot(212)
            plt.ylabel("Amplitude")
            plt.plot(time, self._data[d_start:d_end][:, 1], label="Right channel", color='Black')
            plt.xlabel('Time [s]')
            plt.legend()
            return fig

    def Frequency(self, s_freqs):
        if(self._channels == 1):             #Makes the plot and returns it
            s1 = plt.figure(2)
            spectrum1, freqs1, t1, im1 = plt.specgram(self._data, Fs=self._samplerate, NFFT=1024, cmap=plt.get_cmap('autumn'))
            cbar1 = plt.colorbar(im1)
            plt.ylabel('Frequency (Hz)')
            cbar1.set_label('Intensity (dB)')
            plt.title("Single Channel")
            f1 = self.RT60(freqs1, spectrum1, t1, 3, s_freqs, 1)
            return [s1, f1]

        else:             #Makes the plot and returns it
            s1 = plt.figure(2)
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

            f1 = self.RT60(freqs1, spectrum1, t1, 3, s_freqs, 1)
            f2 = self.RT60(freqs2, spectrum2, t2, 4, s_freqs, 2)
            return [s1, f1, f2]



    def RT60(self, freqs, spectrum, t, fig, s_freq, chan):
        ratio = spectrum.shape[0] / freqs.max()     #Ratio to convert between desired frequency and index for frequency
        def HeighestFrequency():
            _max = len(freqs)
            heighest_freq = None
            heighest_plottable_freq = None
            for x in range(1, _max):
                _data = 10 * np.log10(spectrum[_max - x])
                idx_last_pos = 0                    #Starts at the heighest frequency and converts it into DB
                idx_first_abv_5 = None
                Found = False
                for y in range(len(_data)):
                    if (_data[y] > 0):              #Checks if any of the coverted DB is positive, if so finds find the last positive index
                        idx_last_pos = y
                    if (_data[y] > 5 and (not (Found))):
                        idx_first_abv_5 = y                 #Checks for the first value above 5 DB to clear out unwanted data
                        Found = True

                if(idx_first_abv_5 == None):
                    continue

                if (len(_data[idx_first_abv_5 : idx_last_pos + 1]) > 1 and heighest_freq == None):
                    heighest_freq = (_max - x) / ratio                              #Heighest Frequency has at least one positive data point

                if (len(_data[idx_first_abv_5 : idx_last_pos + 1]) >= 11):
                    heighest_plottable_freq = (_max - x) / ratio                    #Heightest plottable has at least 10 data points
                    break

            return heighest_freq, heighest_plottable_freq

        heightest_frequency , heighest_plottable = HeighestFrequency()

        def plot_frequencies(target_frequency, can_label, _color):
            def frequency_check(target_frequency):
                if(target_frequency > freqs[len(freqs) - 1]):
                    target_frequency = freqs[len(freqs) - 1]
                elif(target_frequency < 0):
                    target_frequency = 0

                data_for_frequency = spectrum[int(ratio * target_frequency)]
                data_in_db_fun = 10 * np.log10(data_for_frequency)      #Converts the data into DB
                idx_last_pos = 0
                idx_first_abv_5 = None
                Found = False

                for x in range(len(data_in_db_fun)):
                    if(data_in_db_fun[x] > 0):              #Finds the indedx of the last positive data point
                        idx_last_pos = x
                    if(data_in_db_fun[x] > 5 and not(Found)):
                        idx_first_abv_5 = x
                        Found = True


                pos_data_in_db = data_in_db_fun[idx_first_abv_5 : idx_last_pos+1]        #returns data from the start to the last positive data point

                return pos_data_in_db, idx_last_pos, idx_first_abv_5

            data_in_db = 0
            last_pos = 0
            first_abv_5 = 0

            t_data_in_db, t_last_pos, t_first_abv_5 = frequency_check(target_frequency)
            if (len(t_data_in_db) < 10):
                upper = target_frequency+3000
                lower = target_frequency-3000
                for x in range(lower, upper):       #Checks 5000Hz above and below in case default frequenct isn't plottable
                    t_data_in_db, t_last_pos, t_first_abv_5 = frequency_check(x)
                    if (t_first_abv_5 == None):
                        continue
                    if (len(t_data_in_db) >= 11):      #Once found, set new values accordingly
                        data_in_db = t_data_in_db
                        last_pos = t_last_pos
                        first_abv_5 = t_first_abv_5
                        target_frequency = x
                        break
            else:
                data_in_db = t_data_in_db
                last_pos = t_last_pos
                first_abv_5 = t_first_abv_5


        #Plotting Data
            plt.figure(fig)
            t_arry = t[first_abv_5: last_pos + 1]
            plt.plot(t_arry, data_in_db, linewidth=1, alpha=.7, color=_color, label=f'{target_frequency}Hz')
            plt.xlabel('Time (s)')
            plt.ylabel('Power (db)')

            index_of_max = np.argmax(data_in_db)
            value_of_max = data_in_db[index_of_max]


            sliced_array = data_in_db[index_of_max:]
            value_of_max_less_5 = value_of_max - 5


            def find_nearest_value(array, value):
                array = np.asarray(array)
                idx = (np.abs(array - value)).argmin()


                return array[idx]


            value_of_max_less_25 = value_of_max - 25
            value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
            index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)


            sliced_array = data_in_db[index_of_max : index_of_max_less_25[0][0]]
            value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
            index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

            if(can_label):
                plt.plot(t_arry[index_of_max], data_in_db[index_of_max], 'go', label="Max")
                plt.plot(t_arry[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro', label='Max-25DB')
                plt.plot(t_arry[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo', label='Max-5DB')
            else:
                plt.plot(t_arry[index_of_max], data_in_db[index_of_max], 'go')
                plt.plot(t_arry[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')
                plt.plot(t_arry[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')


            rt20 = np.abs( (t_arry[index_of_max_less_25] - t_arry[index_of_max_less_5]) )

            rt60 = np.round(3 * rt20, 2)

            delata_t = np.round(t[last_pos] - t[first_abv_5], 2)

            plots_data.append( (rt60[0], delata_t) )
            if(s_freq == None):
                plt.title(f'Decible Vs Time of default frequencies to last audiable second'
                          f' of channel {chan}')
            else:
                plt.title(f'Decible Vs Time of {target_frequency}Hz to last audiable second'
                      f' of channel {chan}')


        default_frequencies = [0, int(heighest_plottable/2), int(heighest_plottable)]
            #Low Mid and High Frequencies

        colors = ["Red", "Blue", "Black"]
        plots_data = []

        if(s_freq == None):
            #If no spesific frequency, merge all 3
            for x in range(len(default_frequencies)):
                if (x == len(default_frequencies) - 1):
                    plot_frequencies(default_frequencies[x], True, colors[x])
                else:       #To provent muntiple lables/legends, only adds a lable on the last iteration
                    plot_frequencies(default_frequencies[x], False, colors[x])

        else:
            # Plots a low, mid, or high frequency
            plot_frequencies(default_frequencies[s_freq], True, colors[0])

        plt.grid()
        plt.legend()

        return (plt.figure(fig) , plots_data, int(heightest_frequency))

