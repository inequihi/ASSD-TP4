from mido import MidiFile
from NoteClass import Note
from TrackClass import Track

########################################################################################################################
# ESTRUCTURA DE UN ARCHIVO MIDI
# - type (int):
#   - 0 Single Track: Tiene 1 sólo track
#   - 1 Synchronous: Todos los tracks empiezan al mismo tiempo
#   - 2 Asynchronous: Cada track es independiente
# - length (float): Tiempo en segundos que dura la canción contenida en el archivo (Sólo para tipos 0 y 1)
# - ticks_per_beat (int): Un beat representa la duración de 1/4 de redonda (1 negra), los beats se dividen en ticks (la
#                         mínima unidad de tiempo en los MIDI). Entonces todas las duraciones de las notas estarán
#                         expresadas en ticks.
#                         Esta variable indica la duración de 1 tick, según cuántos ticks hay en 1 beat
# - tracks (list): Lista de los tracks en formato MidiTrack
#   - MidiTrack (list) : Clase hija de List que contiene los Message
#       - name (string): Nombre del Track
#       - MetaMessage (MetaMessage): Mensaje informativo que representa un evento y que el sintetizador no lee
#           - type (string): Indica el tipo de mensaje ('set_tempo', 'time_signature', 'end_of_track')
#           - Los demás atributos dependerán del tipo de mensaje (https://mido.readthedocs.io/en/latest/meta_message_types.html)
#       - Message (Message): Son las "instrucciones" de la canción. Los atributos dependerán del tipo
#           - type (string): Tipo de instrucción
#               - Note Off (Note, Number,Velocity)
#               - Note On (Note, Number, Velocity)
#               - Polyphonic Aftertouch (Note, Number, Pressure)
#               - Control Change (Controller, Number, Data)
#               - Program Change (Program, Number)
#               - Channel Aftertouch (Pressure)
#               - Pitch Wheel
########################################################################################################################

def get_time(dic):
    return dic['time']

def get_start_time(note):
    return note.start_time

########################################################################################################################
# Recibe un archivo MIDI y lo parsea para extraer los datos de cada track y convertirlos a sus objetos de Python
# ----------------------------------------------------------------------------------------------------------------------
class MIDIHandler:
    def __init__(self, midi):
        self.midi = midi
        self.duration = self.midi.length
        self.ticks_per_beat = midi.ticks_per_beat
        self.tracks = []
        self.tempo = []
        self.time = 0

        self.notes = []
        self.aux_notes = []

        for idt, track in enumerate(midi.tracks):
            print('Track:', idt)
            self.notes = []
            self.aux_notes = []
            self.time = 0
            self.meta_time = 0
            self.tempo.append({'tempo': 0, 'time': self.duration * 1E6})
            if self.tempo:
                self.tempo_idx = 0
            for idm, message in enumerate(track):
                if idm == 2158:
                    print('acá')
                self.midi_message_switch.get(message.type, self.other)(self, message)
                if not message.is_meta:
                    print(idm)
                    self.time = self.time + message.time
                else:
                    self.meta_time = self.meta_time + message.time
            if self.notes: self.tracks.append(Track(self.notes))
            self.tempo.remove({'tempo': 0, 'time': self.duration * 1E6})

        return

    def find_note(self, note):
        r = None
        for idn, n in enumerate(self.aux_notes):
            if n.note != note.note:
                pass
            else:
                r = idn
                break
        return r

    # note_off(channel, note, velocity)
    def note_off(self, msg):
        # print("Note OFF")
        r = True
        idn = self.find_note(msg)
        if idn == 2162:
            print('aqui')
        if idn is not None:
            while self.notes[idn].end_time == 0:
                if self.notes[idn].start_time > self.duration * 1E6:
                    self.notes[idn].start_time = self.duration * 1E6 - 1
                    self.notes[idn].end_time = self.duration * 1E6
                elif self.tempo[self.tempo_idx]['time'] <= self.notes[idn].start_time < self.tempo[self.tempo_idx + 1]['time']:
                    self.notes[idn].start_time = self.notes[idn].start_time * self.tempo[self.tempo_idx]['tempo'] / self.ticks_per_beat
                    self.notes[idn].end_time = (self.time + msg.time) * self.tempo[self.tempo_idx]['tempo'] / self.ticks_per_beat
                elif self.tempo[self.tempo_idx + 1]['time'] <= self.notes[idn].start_time:
                    self.tempo_idx = self.tempo_idx + 1
                else:
                    self.tempo_idx = self.tempo_idx - 1
                if self.notes[idn].end_time >= self.duration * 1E6:
                    self.notes[idn].end_time = self.duration * 1E6
                    if self.notes[idn].start_time >= self.duration * 1E6:
                        self.notes[idn].start_time = self.duration * 1E6 - 1
            self.notes[idn].duration = self.notes[idn].end_time - self.notes[idn].start_time
            self.aux_notes[idn].note = -1
        else:
            r = False

        return r

    # note_on(channel, note, velocity)
    def note_on(self, msg):
        # print("Note ON")
        self.notes.append(Note(msg.note, self.time + msg.time, 0, 0, msg.velocity))
        self.aux_notes.append(Note(msg.note, self.time + msg.time, 0, 0, msg.velocity))
        return True

    def set_tempo(self, msg):
        # print("Set Tempo")
        self.tempo.remove({'tempo': 0, 'time': self.duration * 1E6})
        self.tempo.append({'tempo': msg.tempo, 'time': self.meta_time + msg.time})
        self.tempo.append({'tempo': 0, 'time': self.duration * 1E6})
        return

    def time_signature(self, msg):
        # print("Time Signature")
        return

    def end_of_track(self, msg):
        # print("End of track")
        return

    def other(self, msg, msg2):
        return

    midi_message_switch = {
        'note_off': note_off,
        'note_on': note_on,
        'set_tempo': set_tempo,
        'time_signature': time_signature,
        'end_of_track': end_of_track,
    }
########################################################################################################################

'''
print_midi: Función para ver el formato de un MIDI
'''
def print_midi(path):
    midi_types = ["Single Track", "Synchronous", "Asynchronous"]
    mid = MidiFile(path, clip=True)
    print("Archivo:", path.split('\\')[-1])
    print("Tipo:", midi_types[mid.type])
    if mid.type != 2:
        print("Duración:", mid.length / 60, "minutos")
    print("Hay", len(mid.tracks), "tracks")
    for i in range(len(mid.tracks)):
        print("Track", i, ":", len(mid.tracks[i]), "Messages")
    return mid
