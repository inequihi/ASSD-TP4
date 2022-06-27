import numpy as np

from SongClass import *

#import pyaudio
import simpleaudio as sa

from scipy.io import wavfile

from Eco import effect

from ProcessedNote import ProcessedNote

class backend():

    def __init__(self):
        self.song = Song()
        self.effect = effect()
        self.process_note = ProcessedNote()
        # self.additive = Additive()

    def synthesize_song(self):
        self.song.output_signal = np.zeros(int(self.song.fs*self.song.duration))
        for i in range(len(self.song.tracks)):
            if self.song.tracks[i].activate:
                self.process_note.track_id = i
                self.synthesize_track(self.song.tracks[i])
                # print("track numero", i)
                self.song.output_signal += self.song.tracks[i].velocity * self.song.tracks[i].signal_out / 127

    def synthesize_track(self, track):
        if track.change == 1:
            track.signal_out = np.zeros(int(self.song.fs*self.song.duration))
            # print("sintetiza track")
            # print(self.song.duration)

            for i, note in enumerate(track.notes):
                print("Track:", self.process_note.track_id, "Note:", i, "Instrument:", track.instrument, "\n")
                self.synthesize_note(note, track.instrument)
                z = 0
                # print(int(note.end_time))
                # print(int(note.end_time*1E-6*self.song.fs)-1)
                for y in range(int(note.start_time*1E-6*self.song.fs), int(note.end_time*1E-6*self.song.fs) - 1, 1):
                    track.signal_out[y] = track.signal_out[y] + note.note_signal[z]
                    z = z + 1
                '''    # print("en el for pa ")
                # print(np.abs(track.signal_out))
                if  track.notes[i].start_time != 0:
                    diference = int(track.notes[i].start_time*track.notes[i].fs*1E-6)
                    track.notes[i].note_signal = np.concatenate( (np.zeros(diference), track.notes[i].note_signal) )
                if  track.notes[i].end_time != self.song.duration:
                    #diferencef = int((self.song.duration-track.notes[i].end_time*1E-6)*self.song.fs)
                    diferencef = len(track.signal_out) - len(track.notes[i].note_signal)
                    print(len(np.zeros(diferencef)))
                    #print(len(track.notes[i].note_signal))
                    track.notes[i].note_signal = np.concatenate( (track.notes[i].note_signal, np.zeros(diferencef)) )
                track.signal_out += track.notes[i].note_signal
                '''
    def synthesize_note(self, note, instrument):
        # print("entre a synthesis")
        self.process_note.create_note(note, instrument)
        # print(note.note_signal)

        # llamar a create_note(self, note, instrument)
        # En un futuro no muy lejano create_note recibe un parámetro metodo que diga cual metodo de sintetizar usa


    # Suma las señales de track tomando en cuenta el tiempo que dura cada uno y formando la cancion entera

    def output_signal_song(self):
        print("xddd")

    def play_signal(self, signal):
        signal *= 32767 / np.max(np.abs(signal))
        signal = signal.astype(np.int16)
        self.play = sa.play_buffer(signal, 1, 2, int(self.song.fs))
        # self.play.wait_done()
    # Interfaz con el back

    # una vez que desde el front se modifico la clase Song , llamando a track.update si es el mismo path anterior
    # para sintetizar la cancion

    def quantity_of_tracks(self):
        return len(self.song.tracks)

    def update_path(self, path):
        if self.song.midi != path:
            self.song.set_midi(path)
            print("path updateado")

    def process_song(self):
        if self.song is not None:
            self.synthesize_song()

    def echo_effect(self, g, delay):
        if self.song.output_signal is not None:
            effect.update_params(g, delay, self.song.output_signal, self.song.fs, 500)
            effect.filter_comb()
            self.song.output_signal = effect.get_output_signal()
        else:
            return -1

    def all_pass_effect(self, g, delay):
        if self.song.output_signal is not None:
            effect.update_params(g, delay, self.song.output_signal, self.song.fs)
            effect.all_pass_filter()
            self.song.output_signal = effect.get_output_signal()
        else:
            return -1

    def flanger_effect(self, g, delay, fd):
        if self.song.output_signal is not None:
            effect.update_params(g, delay, self.song.output_signal, self.song.fs, fd)
            effect.flanger()
            self.song.output_signal = effect.get_output_signal()
        else:
            return -1

    def update_track(self, number_track, instrument, activate, velocity):
        if number_track < len(self.song.tracks):
            self.song.tracks[number_track].update(velocity, activate, instrument)
            return True
        else:
            return False

    def play_song(self):
        if self.song.output_signal is not None:
            self.play_signal(self.song.output_signal)

    def play_track(self, n_track):
        if self.song is not None:
            if n_track < len(self.song.tracks):
                self.synthesize_track(self.song.tracks[n_track])
                self.play_signal(self.song.tracks[n_track].signal_out)
            else:
                return -1
        return -1

    def pause_reproduction(self):
        # if self.play.isplaying() and self.play is not None:
        if self.play is not None:
            self.play.stop()
        else:
            return -1

    def resume_song(self, time):
        if self.song.output_signal is not None:
            self.play_signal(self.song.output_signal[int(time*self.song.fs):])


    def save_wav_file(self, filename):
        print(np.max(np.abs(self.song.output_signal)))
        signal = self.song.output_signal * (32767 / np.max(np.abs(self.song.output_signal)))
        signal = signal.astype(np.int16)
        wavfile.write(filename, int(self.song.fs), signal)