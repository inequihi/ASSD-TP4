##########################################
#          ENCRYPTION PROCESS            #
##########################################

# 1. Leer archivo de audio original (read_wav)
# 2. Aplicar transformacion FFT (FFT)
# 3. Aplicar funcion 6 (FreqDomain) (Este no traduce ascii)
# 4. Aplicar algoritmo de encripcion
# 5. Aplicar Funcion 3 (FreqDomain) (Este traduce ascii)
# 6. Aplicar transformacion inversa IFFT
# 7. Guardar archivo de audio encriptado .wav

###########################################
#           DECRYPTION PROCESS            #
###########################################

# 1. Leer archivo de audio encriptado (read_wav)
# 2. Aplicar transformacion FFT (FFT)
# 4. Aplicar Funcion 4 (FreqDomain)
# 5. Aplicar algoritmo de desencriptacion
# 6. Aplicar Funcion 7 (FreqDomain)
# 6. Aplicar transformacion inversa IFFT
# 7. Guardar archivo de audio desencriptado .wav






# 4+88+5+
#
# b'L//J34'
#
# [[ASCII(L)][ASCII(/)] , [ASCII(/)][ASCII(J)]] (Transformo -> F-1[ [[ASCII(L)][ASCII(/)] , [ASCII(/)][ASCII(J)]] ]
#
#
#
# .WAV
#
#
#
# F[ F-1[ [[ASCII(L)][ASCII(/)] , [ASCII(/)][ASCII(J)]] ] ] -> [[ASCII(L)][ASCII(/)] , [ASCII(/)][ASCII(J)]]
#
# -> b'L//J34'



