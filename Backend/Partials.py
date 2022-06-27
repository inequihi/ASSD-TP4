import numpy as np
import time

################################################    PARTIAL NOTE    ################################################

# La clase partial note se va a encargar de procesar cada uno de los
# parciales de cada nota

####################################################################################################################


class PartialNote:


    ########################    INIT    ########################
    def __init__(self, amplitud, freq, phase, start_time, D_time, D_amp, S_time, S_amp, R_time, R_amp, off_time):

        # A la funcion __init__ se la para configurar cada uno de los parciales correspondientes a la nota

        # Dicha clase utilizara las siguientes variables

        #   freq: Frecuencia del parcial.
        #   phase: Fase del sample a la frecuencia del parcial.

        #   start_time: Tiempo en el cual comienza la nota.

        #   D_time: Tiempo en el que termina el attack y comienza el decay
        #   D_amp: Amplitud alcanzada en el punto entre las etapas de attack y decay.

        #   S_time: Tiempo en el que termina el decay y comienza el sustain
        #   S_amp: Amplitud alcanzada en el punto entre las etapas de decay y sustain.

        #   R_time: Tiempo en el que termina el sustain y comienza el release
        #   R_amp: Amplitud alcanzada en el punto entre las etapas de sustain y release.

        #   off_time: Tiempo en el que se observa que la señal se anula. Fin de la etapa de release


        #       /\
        #      /  \                             0: start_time
        #     /    \_________                   1: D_time
        #    /               \                  2: S_time
        #   /                 \                 3: R_time
        #  /----+--+-------+---\---> t          4: off_time
        #  0    1  2       3   4
        #     A   D    S      R

#        Start_time	D_time	  D_amp	    S_time	  S_amp	   R_time	 R_amp	     Off_time
#        0	         0.2  	1.106516	 0.31	0.980918	0.97	0.980918	  1.11767


        self.freq = freq
        self.phase = phase
        self.ampli = amplitud

        #Todos los tiempos son medidos desde el inicio (el inicio del ADSR estandar que es cero)
        # Tiempo de inicio
        self.start_time = start_time

        # Tiempo de inicio hasta Tiempo de D
        self.D_time = D_time - start_time
        self.D_amp = D_amp

        # Tiempo de inicio hasta tiempo de S
        self.S_time = S_time - start_time
        self.S_amp = S_amp

        # Tiempo de  inicio hasta tiempo de R
        self.R_time = R_time - start_time
        self.R_amp = R_amp

        # Tiempo desde el inicio hasta el fin de la etapa de release.
        self.off_time = off_time - start_time


       # Preparo las pendientes
        self.release_time = self.R_time      # QUE ES ESTO??

        self.A_pendiente = self.D_amp / self.D_time                # Pendiente de la etapa de attack.
        self.D_pendiente = (self.S_amp - self.D_amp) / (self.S_time - self.D_time)  # Pendiente de la etapa de decay.
        self.S_pendiente = (self.R_amp - self.S_amp) / (self.R_time - self.S_time)  # Pendiente de la etapa de sustain. --> VA A SER CERO!!!!! en nuestro ADSR trucho xd
        self.R_pendiente = (- self.R_amp) / (self.off_time - self.R_time)           # Pendiente de la etapa de release.

        self.output_signal = np.array([])  # ADSR del parcial pedido

        self.final_ASDR_time = -1  # Tiempo en el cual la ADSR del parcial se hará 0.

    ########################    GETTERS     ########################
    def get_phase(self):
        return self.phase

    def get_freq(self):
        return self.freq

    def get_ampli(self):
        return self.ampli

    def get_amplitude_array(self, note):
        # Se obtiene la ADSR del parcial y lo guarda en self.output_signal
        if(note.duration == 0):

            print("error la duración es cero")

        data = self.get_adsr(note)

        self.output_signal = data

    def get_adsr(self, note):

        ###################################################################
        # QUE ES UN ADSR? (Envolvente: Variación de la intensidad sonora)

        #  Un sonido que se reproduce está condicionado a sufrir alteraciones durante su evolución
        #  temporal a través del tiempo. La envolvente lo que hace es segmentar e intervenir en cada
        #  una de las partes durante la evolución temporal del sonido, desde su inicio hasta su final.
        # Paso la duracion de la nota que venia del objeto nota en microsegundos a segundos
        note_dur_seg = note.duration * 1E-6
        #Se divide el arreglo en las etapas
        #  stageA, stageD, stageS, stageR = np.split(note_out, [D_time_index, S_time_index, R_time_index])
        #Spliteamos el tiempo de duracion de la nota entre las 4 etapas.
        # #TIMPO TOTAL DE ADSR BASE HARDCODEADO DE LA FLAUTA
        t_tot_ADSRn = self.off_time  # Offtime tiene el tiempo donde finaliza

        #TIEMPO DE CADA ETAPA float
        # Agarro la cantidad de elementos que tiene el time base de la nota y con la ADSR estandar y el porcentaje que
        # correponde a cada etapa saco cuantos elementos tiene el time base de cada tapa. Es decir como se repaerte el time base
        # en las diferentes
        note.create_time_base()


        stageA_elements = int((self.D_time / t_tot_ADSRn)                 * np.size(note.time_base))  # stageA% * time_base
        stageD_elements = int(((self.S_time - self.D_time) / t_tot_ADSRn) * np.size(note.time_base))  # same
        stageS_elements = int((self.R_time - self.S_time) / t_tot_ADSRn   * np.size(note.time_base))  # same
        stageR_elements = int((t_tot_ADSRn - self.R_time) / t_tot_ADSRn   * np.size(note.time_base))  # same

        #LINSPACE DE CADA ETAPA
        stageA_x = np.linspace(0 , self.D_time, stageA_elements)
        stageD_x = np.linspace(self.D_time, self.S_time, stageD_elements)
        stageS_x = np.linspace(self.S_time, self.R_time, stageS_elements)
        stageR_x = np.linspace(self.R_time, self.off_time , stageR_elements)

        # Se calculan las etapas de la ADSR --> Son las rectas que hacen al envelope
        stageA = stageA_x * self.A_pendiente
        stageD = (stageD_x - self.D_time)  * self.D_pendiente + self.D_amp
        stageS = (stageS_x - self.S_time)* self.S_pendiente + self.S_amp
        stageR = (stageR_x - self.R_time) * self.R_pendiente + self.R_amp

        ADSR_data = np.concatenate([stageA, stageD, stageS, stageR])  # Se concatenan las etapas

        # IMPORTANTE ! ! !
        # CHECK SIZE LINSPACE DE ADSR MATCHING EL LINSPACE DE NOTA note.timebase
        difference = np.size(note.time_base) - np.size(ADSR_data)  # Chequea diferencias de longitudes para poder sumar
        zeros = np.zeros(abs(difference))  # Crea un arreglo de ceros que permita igualar las longitudes
 #       print("\n.................... CHECKING SIZE I...........................")
  #      print("\nTIME BASE SIZE = " , np.size(note.time_base) )
   #     print("\nADSR SIZE = " , np.size(ADSR_data))
    #    print("\n diferencia = " , difference)

        if (difference > 0):  # Si el timebase es mas grande que el ADSR envelope le agrego ceros :D
            ADSR_data = np.concatenate([ADSR_data, zeros])  # Se concatena y se suma

        elif (difference < 0):  # Si el ADSR envelope es mas grande que el timebase [D:] le sacamos a la etapa de sustain la diferencia
            ADSR_data = ADSR_data[:difference]


        difference = np.size(note.time_base) - np.size(ADSR_data)

 #       print("\n..................... CHECKING SIZE II ...........................")
  #      print("\nTIME BASE SIZE = " , np.size(note.time_base) )
   #     print("\nADSR SIZE = " , np.size(ADSR_data))
    #    print("\n diferencia = " , difference)

        return ADSR_data


    def get_final_ASDR_time(self, note):

        # Si se completan las etapas de attack y decay
        if (note.duration >= self.S_time ):

            # Si la pendiente de sustain es positiva o la duracion es menor que el tiempo en que la etapa S se haria 0.
            # ==> El tiempo maximo es cuando la etapa R se hace 0.
            if ((self.S_pendiente >= 0) or note.duration <= self.S_time - self.S_amp / self.S_pendiente):
                return note.duration - ((note.duration - self.S_time) * self.S_pendiente + self.S_amp) / self.R_pendiente

            # Si no se llega a la etapa R antes de que se anule S
            # ==> El timepo maximo es cuando se anula S
            else:
                return self.S_time - self.S_amp / self.S_pendiente

        # Si no se completan todas las etapas
        else:

            # Si no se completan todas las etapas y no hay etapa D
            if note.duration <= self.D_time:
                return note.duration - ((note.duration) * self.A_pendiente) / self.R_pendiente

            # Si no se completan todas las etapas y no hay etapa S
            elif note.duration <= self.S_time:
                return note.duration - ((note.duration - self.D_time) * self.D_pendiente + self.D_amp) / self.R_pendiente




'''
        # Si no se completan todas las etapas...
        else:
            # Etapas AR
            if note_dur_seg <= self.D_time:
                stageA, stageR = np.split(note_out, [R_time_index])
                stageA = (stageA) * self.A_pendiente
                stageR = (stageR - note_dur_seg) * self.R_pendiente + note_dur_seg * self.A_pendiente
                data = np.concatenate([stageA, stageR])

            # Etapas A D y R
            elif note.duration <= self.S_time:
                D_time_index = int(round((self.D_time) * note.fs))
                stageA, stageD, stageR = np.split(note_out, [D_time_index, R_time_index])
                stageA = (stageA) * self.A_pendiente
                stageD = self.D_amp + self.D_pendiente * (stageD - self.D_time)
                stageR = (stageR - note_dur_seg) * self.R_pendiente + self.D_amp + ( note_dur_seg - self.D_time) * self.D_pendiente
                data = np.concatenate([stageA, stageD, stageR])  # Se concatenan las etapas
'''
