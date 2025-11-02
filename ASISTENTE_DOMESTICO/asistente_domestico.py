import random as rd
import datetime as dt
import time as t
import speech_recognition as sr
import pyttsx3 #libreria que permite darle voz al programa

class ComandoVoz:
    def __init__(self):
        self.r = sr.Recognizer()
        
        micros = sr.Microphone.list_microphone_names()
        indice = None
        
        for i, nombre in enumerate(micros):
            if "Realtek" in nombre:
                indice = i
                break
        
        self.mic = sr.Microphone(device_index=indice)
        
    def escuchar(self):
        try:
            with self.mic as source:
                self.r.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.r.listen(source)
            
            texto = self.r.recognize_google(audio, language="es-ES")
            print(f"Dijiste: {texto}")
            return texto.lower()
            
        except:
            return None

class VozAsistente:
    def hablar(self, texto):
        voz = pyttsx3.init()
        voz.say(texto)
        voz.runAndWait()
        voz.stop()

class Hablador(VozAsistente):
    def saludar(self, nombre):
        frases = [
            f"\nHola, soy tu asistente robótico. Me llamo {nombre}, listo para ayudarte.",
            f"\n¡Te saluda {nombre}! Siempre es un buen día para ser útil.",
            f"\nSistema activado. {nombre} esta listo y preparado para trabajar contigo."
        ]

        frase_s = rd.choice(frases)
        print(frase_s)
        self.hablar(frase_s)

    def despedirse(self):
        frases = [
            "Hasta luego, ¡que tengas un excelente día!",
            "Fue un placer asistirte. ¡Hasta pronto!",
            "Modo reposo activado. ¡Nos vemos!"
        ]

        frase_s = rd.choice(frases)
        print("\n" + frase_s)
        self.hablar(frase_s)

    def emitir_mensaje(self, mensaje, tipo="AVISO"):
        sld_mensaje = f"{tipo}: {mensaje}"
        print(f"\n{sld_mensaje}")
        self.hablar(sld_mensaje)

class ReproductorAudio(Hablador):
    def __init__(self):
        super().__init__()
        self.volumen = 50 # capacidad por defecto en %
        self.musica_actual = None

    def reproducir_musica(self):
        print(f"\n=> Reproduciendo audio:")
        self.hablar("¿Qué música o audio deseas reproducir?")
        musica = self.escuchar()
        
        if musica:
            print("Iniciando reproducción...")
            t.sleep(0.8)
            self.musica_actual = musica
            self.emitir_mensaje(f"Reproduciendo {musica}.", "EXITO")
        else:
            self.emitir_mensaje("No se pudo reconocer el audio a reproducir", "ERROR")

    def detener_musica(self):
        print(f"\n=> Detener audio:")
        t.sleep(0.8)
        self.emitir_mensaje(f"La música se detuvo", "EXITO")
        self.musica_actual = None

    def subir_volumen(self):
        if not self.musica_actual:
            self.emitir_mensaje(f"No hay música en reproducción", "ERROR")
            return
        if self.volumen >= 100: 
            self.emitir_mensaje(f"Volumen en su maxima capacidad: {self.volumen}%.", "INFO")
            return
        self.volumen += 1
        self.emitir_mensaje(f"Volumen: {self.volumen}%.", "INFO")

    def bajar_volumen(self):
        if not self.musica_actual:
            self.emitir_mensaje(f"No hay música en reproducción", "ERROR")
            return
        if self.volumen <= 0: 
            self.emitir_mensaje(f"El audio esta silenciado.", "INFO")
            return
        self.volumen -= 1
        self.emitir_mensaje(f"Volumen: {self.volumen}%.", "INFO")

class ControlHogar(Hablador):
    def __init__(self):
        super().__init__()
        self.temperatura = 21 #aplicado en grados centigrados
        self.habitacion = None

    def encender_luz(self):
        print("\n=> NUEVA TAREA: Encender las luces")

        habitaciones = ["dormitorio", "baño", "cocina", "sala", "cochera", "comedor", "pasillo"]
        
        mensaje = "¿En qué habitación deseas encender la luz? Opciones: dormitorio, baño, cocina, sala, cochera, comedor o pasillo"
        print(mensaje)
        self.hablar(mensaje)
        
        lugar = self.escuchar()
        
        if lugar and any(hab in lugar for hab in habitaciones):
            for hab in habitaciones:
                if hab in lugar:
                    self.habitacion = hab.capitalize()
                    break
            
            print(f"\nEncendiendo las luces en {self.habitacion}...")
            t.sleep(1)
            self.emitir_mensaje(f"Las luces en {self.habitacion} están encendidas.")
        else:
            error = "No se reconoció la habitación. Inténtelo nuevamente."
            print(f"\n{error}")
            self.emitir_mensaje(error, "ERROR")

    def apagar_luz(self):
        print("\n=> NUEVA TAREA: Apagar las luces")

        habitaciones = ["dormitorio", "baño", "cocina", "sala", "cochera", "comedor", "pasillo"]
        
        mensaje = "¿En qué habitación deseas apagar la luz? Opciones: dormitorio, baño, cocina, sala, cochera, comedor o pasillo"
        print(mensaje)
        self.hablar(mensaje)
        
        lugar = self.escuchar()
        
        if lugar and any(hab in lugar for hab in habitaciones):
            for hab in habitaciones:
                if hab in lugar:
                    sel_habitacion = hab.capitalize()
                    break
            
            print(f"\nApagando las luces en {sel_habitacion}...")
            t.sleep(1)
            self.emitir_mensaje(f"Las luces en {sel_habitacion} están apagadas.")
        else:
            error = "No se reconoció la habitación. Inténtelo nuevamente."
            print(f"\n{error}")
            self.emitir_mensaje(error, "ERROR")

    def temp_actual(self):
        rango = {
            "Frío": self.temperatura < 18,
            "Confortable": 18 <= self.temperatura <= 24,
            "Cálido": self.temperatura > 24
        }
        estado = next(k for k, v in rango.items() if v)
        return f"Temperatura actual: {self.temperatura}°C — Estado: {estado}"

    def regular_temperatura(self):
        print("\n=> NUEVA TAREA: Regular la temperatura de la casa")
        self.emitir_mensaje(self.temp_actual(), "INFO")

        penticion = "¿A qué temperatura deseas ajustar la casa? Di solo el número en grados centígrados"
        print(penticion)
        self.hablar(penticion)
        temp_voz = self.escuchar()
        
        if temp_voz:
            try:
                # Extraer números del texto reconocido
                import re
                numeros = re.findall(r'\d+', temp_voz)
                
                if numeros:
                    temp = float(numeros[0])
                    print(f"\nAjustando la temperatura de toda la casa a {temp}°C...")
                    t.sleep(1.5)
                    self.temperatura = temp 
                    self.emitir_mensaje(self.temp_actual(), "INFO")
                else:
                    self.emitir_mensaje("No se reconoció un número válido para la temperatura", "ERROR")
            except ValueError:
                self.emitir_mensaje("No se pudo procesar la temperatura indicada", "ERROR")
        else:
            self.emitir_mensaje("No se pudo reconocer la temperatura", "ERROR")

class AsistenteVirtual(ControlHogar, ReproductorAudio, ComandoVoz):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.saludar(self.nombre)

    def mostrar_menu(self):
        print("\n" + "="*40)
        print("> MENÚ DE OPCIONES")
        print("="*40)
        
        opciones = [
            "Reproducir música",
            "Detener música",
            "Subir volumen",
            "Bajar volumen",
            "Encender luz",
            "Apagar luz",
            "Regular temperatura",
            "Info de sistema",
            "Salir"
        ]

        for i, opcion in enumerate(opciones, start=1):
            print(f"{i}. {opcion}")
        print("="*40)

    def info_robot(self):
        fecha_hora_actual = dt.datetime.now()
        formato_datetime = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

        mensaje = (
            f"\n=> ESTADO DEL SISTEMA:"
            f"\nAudio/Musica: {self.musica_actual}"
            f"\nVolumen: {self.volumen}%"
            f"\n{self.temp_actual()}"
            f"\nFecha/Hora actual: {formato_datetime}"
        )
        print(mensaje)
        self.hablar(mensaje)

    def ejecutar(self):
        acciones = {
            "reproducir música": self.reproducir_musica,
            "detener musica": self.detener_musica,
            "subir volumen": self.subir_volumen,
            "bajar volumen": self.bajar_volumen,
            "encender luz": self.encender_luz,
            "apagar luz": self.apagar_luz,
            "regular temperatura": self.regular_temperatura,
            "info de sistema": self.info_robot,
            "salir": self.despedirse
        }

        while True:
            self.mostrar_menu()
            mensaje = f"¿Qué deseas que haga {self.nombre}? Menciona la elección:"
            print(mensaje)

            opcion = self.escuchar()
            
            if not opcion:
                print("No se pudo escuchar. Intenta de nuevo...")
                continue
            
            opcion = opcion.lower().strip()

            if "salir" in opcion:
                self.despedirse()
                break

            accion_encontrada = None
            for clave in acciones.keys():
                if clave in opcion or opcion in clave:
                    accion_encontrada = clave
                    break
            
            if accion_encontrada:
                acciones[accion_encontrada]()
            else:
                self.emitir_mensaje("Opción no válida", "ERROR")

if __name__ == "__main__":
    robot = AsistenteVirtual("HomeBot_XV2")
    robot.ejecutar()