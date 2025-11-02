import speech_recognition as sr
import pyttsx3

# Inicializamos el motor de voz
voz = pyttsx3.init()

def hablar(texto):
    voz.say(texto)
    voz.runAndWait()

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Te escucho...")
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language="es-ES")
        print("Dijiste:", texto)
        return texto.lower()
    except:
        hablar("No te entendí, repite por favor.")
        return ""

# Ejemplo de interacción
hablar("Hola, soy tu asistente. ¿Qué deseas hacer?")
comando = escuchar()

if "hora" in comando:
    from datetime import datetime
    hora = datetime.now().strftime("%H:%M")
    hablar(f"Son las {hora}")
elif "luces" in comando:
    hablar("Encendiendo las luces.")
else:
    hablar("No tengo una acción para eso todavía.")


