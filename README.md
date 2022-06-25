# ASSD - TP4

## Encryption Process
 ### 1. Leer archivo de audio original (read_wav)

 ### 2. Aplicar transformacion FFT (FFT)

 ### 3. Aplicar funcion FFT-to-byte
       La funcion se encarga de convertir una matriz de valores de fourier a un
       string compuesto por dichos valores, separados por su signo
       Ejemplo:
           Entrada = [[1][2], [3][-4], [5][6]]
           Salida  = "+1+2+3-4+5+6"

 ### 4. Aplicar algoritmo de encripcion

 ### 5. Aplicar funcion encript-to-FFT_ascii
       La funcion se encarfga de convertir un string, el cual es la respuesta de
       la encriptacion, a un arreglo apto para aplicar transformada de fourier con valores ASCII
       Ejemplo:
           Entrada = b'Lx^#5'
           Salida  = [[ASCII(L)][ASCII(x)], [ASCII(^)][ASCII(#)]], donde el ASCII(...) = numero

 ### 6. Aplicar transformacion inversa IFFT

 ### 7. Guardar archivo de audio encriptado .wav


## Decryption Process
 ### 1. Leer archivo de audio encriptado (read_wav)

 ### 2. Aplicar transformacion FFT (FFT)

 ### 3. Aplicar la funcion FFT_ascii-to-encript
       La funcion en cuestion sirve para hacer la accion contraria a la funcion FFT-to-byte. Con
       el fin de devolver un string capaz de ser interpretado por la funcion de desencriptacion
       Ejemplo:
           Salida = b'Lx^#5'
           Entrada = [[ASCII(L)][ASCII(x)], [ASCII(^)][ASCII(#)]], donde el ASCII(...) = numero

 ### 4. Aplicar algoritmo de desencriptacion

 ### 5. Aplicar la funcion byte-to-FFT
       La funcion en cuestion sirve para hacer la accion contraria a la funcion encript-to-FFT_ascii. Con
       el fin de devolver un arreglo apto para aplicar transformada de fourier
       Ejemplo:
           Entrada = "+1+2+3-4+5+6"
           Salida = [[1][2], [3][-4], [5][6]]

 ### 6. Aplicar transformacion inversa IFFT

 ### 7. Guardar archivo de audio desencriptado .wav


