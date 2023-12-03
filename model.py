# model.py
import pandas as pd
from scipy.io import wavfile
from pydub import AudioSegment

class Model:
    def __init__(self):
        self.audio_data = None
        self.file_info ={}

    def load_audio_file(self, file_path):
        # Checks if the file is of the correct format
        if not file_path.lower().endswith(('.wav', '.mp3', '.aac')):
            raise ValueError("Wrong file format chosen. Please use wav, mp3, or aac.")

        # Convert to wav if not already in wav format
        if not file_path.lower().endswith('.wav'):
            file_path = self.convert_to_wav(file_path)




