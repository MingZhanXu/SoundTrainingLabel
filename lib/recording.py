import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write
import msvcrt
class Recorder():
    def __init__(self, samplerate=22050, duration=1):
        self.samplerate = samplerate
        self.duration = duration
    def record(self):
        audio_data = sd.rec(int(self.samplerate * self.duration), samplerate=self.samplerate, channels=1, dtype=np.int16)
        sd.wait()
        return audio_data
    def recorder_to_file(self, audio_data, save_path, file_name):
        file_path = os.path.join(save_path, f"{file_name}.wav")
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        write(file_path, self.samplerate, audio_data)
        return file_path
    def record_audio(self, save_path, file_name):
        audio_data = self.record()
        file_path = self.recorder_to_file(audio_data, save_path, file_name)
        return file_path
        

