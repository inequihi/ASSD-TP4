import numpy as np
import math as math

def eco_simple(song, ganancia, retraso): # ganancia en porcentaje, y retraso en ms

    corrimiento= int(song.fs*retraso*10**-3)      ## retraso en ms
    señal_eco= (ganancia/100)*np.concatenate(np.zeros(corrimiento), song.output_signal)
    song.output_signal = señal_eco + np.concatenate(song.output_signal, np.zeros(corrimiento))

class effect:
    def __init__(self):
        self.g = 0.5
        self.delay = 1 # en ms
        self.signal_in = []
        self.signal_out = []
        self.fs = 1*1E3
        self.fd = 1
    def comb(self, xin, yinold):
        out = xin + self.g*yinold
        return out
    def filter_comb(self):
        self.signal_out = np.zeros(len(self.signal_in))
        delay_paso= int( self.delay*1E-3 * self.fs)

        for i, out in enumerate(self.signal_out):
            if (i- delay_paso) >= 0:
                self.signal_out[i] = self.comb(self.signal_in[i], self.signal_out[i- delay_paso])
            else:
                self.signal_out[i] = self.signal_in[i]
        #print(self.signal_out)
    def all_pass(self, xin, xinold, yiold):
        out = (-self.g*xin)+xinold+(self.g*yiold)
        return out

    def all_pass_filter(self):
        self.signal_out  = np.zeros(len(self.signal_in))
        delay_paso = int(self.delay * 1E-3 * self.fs)
        for i, out in enumerate(self.signal_out):
            if (i - delay_paso) >= 0:
                self.signal_out[i] = self.all_pass(self.signal_in[i], self.signal_in[i- delay_paso],self.signal_out[i- delay_paso])
            else:
                self.signal_out[i] = self.signal_in[i]

    def flanger(self):
        self.signal_out = np.zeros(len(self.signal_in))
        for i, out in enumerate(self.signal_out):
            print(self.fd/self.fs)
            print("coseno",math.cos(2*np.pi*i*self.fd/self.fs))
            delay_paso = int((self.delay * 1E-3 * self.fs)*(1+(np.sin(2*np.pi*i*(self.fd/self.fs)))))
            print("delay de paso", delay_paso)
            print("indice", i, "\n")
            if (i - delay_paso) >= 0:
                self.signal_out[i] = self.signal_in[i] + self.g*self.signal_in[i- delay_paso]
            else:
                self.signal_out[i] = self.signal_in[i]


    def update_params(self, g, delay, signal_in, fs, fd=1):
        self.g = g
        self.delay = delay
        self.signal_in = signal_in
        self.fs = fs
        self.fd = fd

    def get_output_signal(self):
        out = self.signal_out
        return out

prueba = np.array([1, 2, 3, 4, 3, 2, 1, 0, 5])
#prueba = np.zeros(4)
obj = effect()
obj.update_params(0.5, 5, prueba, 1*1E3, 400)
obj.filter_comb()
print(obj.signal_in)
print(obj.get_output_signal())


