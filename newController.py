# newController.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as sio
from scipy.io import wavfile
from pydub import AudioSegment
from model import Model

class AudioController:
    def __init__(self, model):
        self._model = model()

    def load_file(self, u_file):
        self._model.load_file(u_file)

    def show_wav(self, start=0, end=0):
        self._model.show_wav(start, end)

    def frequency(self, u_frequencies):
        self._model.frequency(u_frequencies)

    def rt60(self, freqs, spectrum, t, user_frequencies):
        self._model.rt60(freqs, spectrum, t, user_frequencies)

def main():
    audio_controller = AudioController()
    audio_controller.load_file("PolyHallClap_10mM.WAV")

    if __name__ == "__main__":
        main()

main()







