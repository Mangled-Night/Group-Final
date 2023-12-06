# newController.py
import pandas as pd
from scipy.io import wavfile
from pydub import AudioSegment

class AudioController:
    def __init__(self,model,view):
        self.model = model
        self.view = view

    def load_file(self, file_path):
        self.model.load_file(file_path)






