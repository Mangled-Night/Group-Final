# newController.py
from model import Model

class AudioController:
    def __init__(self):
        self._model = Model()

    def load_file(self, u_file):
        self._model.LoadFile(u_file)

    def show_wav(self):
        self._model.ShowWav()

    def frequency(self):
        self._model.Frequency()

    def rt60(self, freqs, spectrum, t, user_frequencies):
        self._model.rt60(freqs, spectrum, t, user_frequencies)

def main():
    audio_controller = AudioController()
    audio_controller.load_file("PolyHallClap_10mM.WAV")

    if __name__ == "__main__":
        main()

main()







