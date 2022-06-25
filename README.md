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
1. Leer archivo de audio original
2. Aplicar transformacion FFT
3. Aplicar algoritmo de encripcion
4. Aplicar transformacion inversa IFFT
5. Guardar archivo de audio encriptado .wav

## Decryption Process
1. Leer archivo de audio encriptado
2. Aplicar transformacion FFT
3. Aplicar algoritmo de desencriptacion
4. Aplicar transformacion inversa IFFT
5. Guardar archivo de audio desencriptado .wav

