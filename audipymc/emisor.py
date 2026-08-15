import socket

import pyaudio



# Misma configuración para que coincidan las ondas

CHUNK = 1024

FORMAT = pyaudio.paInt16

CHANNELS = 1

RATE = 44100



def emisor_audio():

    p = pyaudio.PyAudio()

    # Abrimos el stream como entrada (micrófono)

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    

    # IMPORTANTE: Aquí usas la IP y el puerto PÚBLICO que te dio Playit

    # Basado en tu mensaje: '147.185.221.30' y el puerto 49962

    direccion_publica = '147.185.221.30' 

    puerto_publico = 49962

    

    print(f"Conectando a {direccion_publica}:{puerto_publico}...")

    sock.connect((direccion_publica, puerto_publico))

    

    print("¡Conectado! Habla ahora...")

    

    try:

        while True:

            data = stream.read(CHUNK)

            sock.sendall(data)

    except KeyboardInterrupt:

        pass

    finally:

        stream.stop_stream()

        stream.close()

        p.terminate()

        sock.close()



emisor_audio()
