import numpy
import matplotlib as Mplt
from scipy.io import wavfile as sio
from pydub import AudioSegment


class Controller:
    _file = None

    def LoadFile(self, uFile):
        parsed_file = uFile.split(".")
        if(parsed_file[-1] == "wav"):
            self._file = uFile
        else:
            try:
                audio = AudioSegment.from_file(uFile)
                self._file = audio.export(format="wav")
            except Exception as err:
                print(f'An error occured "{err}"')

    def ShowWav(self):
        samplerate, data = sio.read(self._file)
        print(f"number of channels = {data.shape[len(data.shape) - 1]}")
        print(f"sample rate = {samplerate}Hz")
        length = data.shape[0] / samplerate
        print(f"length = {length}s")


def main():
    C = Controller()
    C.LoadFile("")



main()