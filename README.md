# ASSD - TP4

## Clone and Install
1. Clonar repositorio de https://github.com/inequihi/ASSD-TP4.git

2. Crear y activar el virtual environment. 

    Si utiliza PyCharm ir a 'Add Interpreter' y seleccionar 'New Environment'. 
    Si utiliza VSCode, abrir una Terminal y ejecutar:

          ```
          py -3 -m venv venv
          venv\Scripts\activate
          ```

    Si tira 'No se puede cargar el archivo Activate.ps1 porque la ejecución de scripts está deshabilitada en este sistema', abrir un Powershell como administrador y ejecutar:

          ```
          Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
          ```
 
    Ahora debería funcionar el comando de activación.
    Si se está utilizando VSCode o PyCharm se activará automaticamente cada vez que se abra una terminal, así se trabaja siempre desde el venv.
    Si utiliza otra IDE, chequear si es necesario activar el venv cada vez que se abre el proyecto.

    Si por alguna razón resulta necesario salir del venv, ejecutar:

          ```
          deactivate
          ```

3. Ya en el venv, ejecutar:

    ```
    pip install -r requirements.txt
    ```

4. A laburar

## Encryption Process
 1. Leer archivo de audio original (read_wav)

 2. Aplicar transformacion FFT (FFT)

 ###3. Aplicar funcion FFT-to-byte
       La funcion se encarga de convertir una matriz de valores de fourier a un
       string compuesto por dichos valores, separados por su signo
       Ejemplo:
           Entrada = [[1][2], [3][-4], [5][6]]
           Salida  = "+1+2+3-4+5+6"

 4. Aplicar algoritmo de encripcion

 5. Aplicar funcion encript-to-FFT_ascii
       La funcion se encarfga de convertir un string, el cual es la respuesta de
       la encriptacion, a un arreglo apto para aplicar transformada de fourier con valores ASCII
       Ejemplo:
           Entrada = b'Lx^#5'
           Salida  = [[ASCII(L)][ASCII(x)], [ASCII(^)][ASCII(#)]], donde el ASCII(...) = numero

 6. Aplicar transformacion inversa IFFT

 7. Guardar archivo de audio encriptado .wav

## Decryption Process
 1. Leer archivo de audio encriptado (read_wav)

 2. Aplicar transformacion FFT (FFT)

 4. Aplicar la funcion FFT_ascii-to-encript
       La funcion en cuestion sirve para hacer la accion contraria a la funcion FFT-to-byte. Con
       el fin de devolver un string capaz de ser interpretado por la funcion de desencriptacion
       Ejemplo:
           Salida = b'Lx^#5'
           Entrada = [[ASCII(L)][ASCII(x)], [ASCII(^)][ASCII(#)]], donde el ASCII(...) = numero

 5. Aplicar algoritmo de desencriptacion

 6. Aplicar la funcion byte-to-FFT
       La funcion en cuestion sirve para hacer la accion contraria a la funcion encript-to-FFT_ascii. Con
       el fin de devolver un arreglo apto para aplicar transformada de fourier
       Ejemplo:
           Entrada = "+1+2+3-4+5+6"
           Salida = [[1][2], [3][-4], [5][6]]

 6. Aplicar transformacion inversa IFFT

 7. Guardar archivo de audio desencriptado .wav


