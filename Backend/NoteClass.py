import numpy as np

class Note:
    def __init__(self, note, start_time, duration, end_time, velocity, fs=44.1E3):
        self.note = note
        self.freq = self.note2freq(note)
        self.start_time = start_time            # Tiempo en microsegundos
        self.duration = duration                # Tiempo de microsegundos
        self.end_time = end_time                # Tiempo de microsegundos
        self.velocity = velocity
        self.note_signal = None
        self.fs = fs
        self.time_base = np.linspace(self.start_time * 1E-6, self.end_time * 1E-6, int(self.fs * self.duration*1E-6))

    def set_note_signal(self, note_signal):
        self.note_signal = note_signal

    def update_fs(self, fs):
        self.fs = fs
        self.time_base = np.linspace(self.start_time *1E-6, self.end_time *1E-6, int(self.fs * self.duration* 1E-6))

    def create_time_base(self):
        self.time_base = np.linspace(self.start_time * 1E-6, self.end_time * 1E-6, int(self.fs * self.duration* 1E-6))

    def note2freq(self, note):
        #freq = 8.1757989156 * (2 ** (note / 12))
        if note > 83:
            note_aux = note % 12 + 72
            freq = 8.1757989156 * (2 ** (note_aux / 12))

        elif note < 36:
            note_aux = note % 12 + 36
            freq = 8.1757989156 * (2 ** (note_aux / 12))
        else:
            freq = 8.1757989156 * (2 ** (note / 12))

        return freq
