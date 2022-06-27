from mido import MidiFile
import numpy as np
from midi_handler import MIDIHandler
#from TrackClass import Track

class Song:
    def __init__(self, fs=float(44.1E3)):
        self.midi = None
        self.tracks = []
        self.fs = fs
        self.duration = 0.0                 # Duración de la canción en segundos
        self.time_base = 0.0
        self.output_signal = None

    def set_output_signal(self, output_signal):
        self.output_signal = output_signal

    def set_midi(self, path):
        self.midi = MidiFile(path, clip=True)
        self.duration = self.midi.length
        self.time_base = np.linspace(0, self.duration*10**-6, int(self.fs * self.duration))
        self.tracks = MIDIHandler(self.midi).tracks
        return

    def set_base_tiempo(self):
        self.time_base = np.linspace(0, self.duration*10**-6, int(self.fs*self.duration))