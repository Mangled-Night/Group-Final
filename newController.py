# newController.py
from model import Model

class AudioController:
    def __init__(self):
        self._model = Model()


    def load_file(self, u_file):
        self._model.LoadFile(u_file)


    def show_wav(self,start, end):
        self._model.ShowWav(start,end)
        return self._model.ShowWav()

    def frequency(self,s_freqs=None):
        self._model.Frequency(s_freqs)
        return self._model.Frequency(s_freqs)
    def returnStats(self):
        self.returnStats()
        return self.returnStats()



def main():
    audio_controller = AudioController()
    audio_controller.load_file("PolyHallClap_10mM.WAV")

    if __name__ == "__main__":
        main()

main()







