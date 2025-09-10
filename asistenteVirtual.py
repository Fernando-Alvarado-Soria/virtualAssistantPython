import speech_recognition as sr
import keyboard
import time
import pygame
import sounddevice as sd
import soundfile as sf
import tempfile

# Inicializar pygame mixer una sola vez 
#Esto es un comentario
pygame.mixer.init()

# Mapeo de comandos de voz a atajos de teclado
comandos = {
    'copiar': 'ctrl+c',
    'pegar': 'ctrl+v',
    'cortar': 'ctrl+x',
    'guardar': 'ctrl+s',
    'deshacer': 'ctrl+z',
    'regresar': 'ctrl+y',
    'selecionar todo': 'ctrl+a',
    'captura de pantalla': 'shift+windows+s',
    'imprimir': 'ctrl+p',
    'negrita': 'ctrl+b',
    'cursiva': 'ctrl+i',
    'subrayar': 'ctrl+u',
    'centrar texto': 'ctrl+e',
    'alinear a la izquierda': 'ctrl+l',
    'alinear a la derecha': 'ctrl+r',    
    '': '',
}

# Ruta de sonidos
sonido_ok = 'sonido/correct.mp3'
sonido_error = 'sonido/error.mp3'

def reproducir_sonido(ruta):
    try:
        sonido = pygame.mixer.Sound(ruta)
        sonido.play()
    except Exception as e:
        print(f"Error al reproducir sonido: {e}")

def grabar_audio_durante(segundos=4):
    print("🎙️ Grabando...")
    fs = 44100  # frecuencia de muestreo
    audio = sd.rec(int(segundos * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    
    archivo_temporal = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(archivo_temporal.name, audio, fs)
    return archivo_temporal.name

def escuchar_comando():
    recognizer = sr.Recognizer()
    archivo_audio = grabar_audio_durante(4)
    try:
        with sr.AudioFile(archivo_audio) as source:
            audio = recognizer.record(source)
        texto = recognizer.recognize_google(audio, language='es-ES').lower()
        print("Has dicho:", texto)
        return texto
    except sr.UnknownValueError:
        print("No se entendió el comando")
        reproducir_sonido(sonido_error)
    except sr.RequestError:
        print("Error de conexión con el servicio de reconocimiento")
        reproducir_sonido(sonido_error)
    return None

def ejecutar_comando(texto):
    if texto in comandos:
        keyboard.press_and_release(comandos[texto])
        reproducir_sonido(sonido_ok)
    else:
        print("Comando no reconocido")
        reproducir_sonido(sonido_error)

print("Asistente iniciado. Pulsa Ctrl+Shift para activar.")

while True:
    if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
        print("Activado")
        time.sleep(0.5)  # Evita múltiples activaciones
        comando = escuchar_comando()
        if comando:
            ejecutar_comando(comando)
