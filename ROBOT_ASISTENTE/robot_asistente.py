import time as t
import datetime as dt
import random as rd

# Creamos una clase adiciopnal que solicite las tareas y peticiones al usuario
class PedirDecision:
    def pedir_destino(self, tipo="ubicación"):
        while True:
            destino = input(f"Ingrese la {tipo}: ").strip()
            if destino: return destino
            print("Por favor, ingrese un valor válido.")

    def elegir_cafe(self):
        sabores = ["americano", "capuchino", "espresso", "moka"]
        print("\n> Sabores disponibles:")
        print("=" * 20)
        for i, s in enumerate(sabores, 1):
            print(f"{i}. {s.capitalize()}")
        print("=" * 20)

        eleccion = input("> Elige un tipo de café (número o nombre): ").strip().lower()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(sabores):
            return sabores[int(eleccion) - 1]
        elif eleccion in sabores:
            return eleccion
        else:
            print("Elección no válida, se seleccionará uno al azar.")
            return rd.choice(sabores)
        
    def confirmar_accion(self, mensaje):
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()
        return respuesta in ["s", "si", "yes"]

class Hablador:
    def saludar(self, nombre):
        frases = [
            f"\nHola {nombre}, soy tu asistente robótico, listo para ayudarte.",
            f"\n¡Saludos {nombre}! Siempre es un buen día para ser útil.",
            f"\nSistema activado, {nombre}. Preparado para trabajar contigo."
        ]
        print(rd.choice(frases))

    def despedirse(self):
        frases = [
            "Hasta luego, ¡que tengas un excelente día!",
            "Fue un placer asistirte. ¡Hasta pronto!",
            "Modo reposo activado. ¡Nos vemos!"
        ]
        print("\n" + rd.choice(frases))

    def emitir_mensaje(self, mensaje, tipo="AVISO"):
        print(f"\n{tipo}: {mensaje}")

    def info_fecha_hora(self):
        print("\n=> Fecha y hora actual:")
        fecha_hora_actual = dt.datetime.now()
        print(fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"))

class Caminante:
    def mover(self, destino):
        print(f"\n=> Destino: {destino}")
        print("Iniciando desplazamiento...")
        t.sleep(0.8)
        recorrido = rd.randint(5, 15)
        print(f"Robot en movimiento... recorriendo {recorrido} metros.")
        for i in range(3):
            print(f"\r.", end="", flush=True)
        print("\n> Destino alcanzado con éxito.")
        return recorrido
    
    def detener(self):
        print("> El robot se ha detenido.")

class RobotAsistente(Hablador, Caminante):
    def __init__(self, nombre):
        self.nombre = nombre
        self.tareas_realizadas = 0
        self.bateria = 100
        self.motores_activos = False
        self.decision = PedirDecision()
        self.historial_tareas = []
        self.ubicacion_actual = "Base"

        self.saludar(self.nombre)

    def usar_bateria(self, consumo):
        self.bateria -= consumo
        if self.bateria < 0:
            self.bateria = 0
        print(f"Batería restante: {self.bateria}%")

        if self.bateria <= 20:
            self.emitir_mensaje(f"Bateria baja: {self.bateria}%", "ADVERTENCIA")
        if self.bateria == 0:
            self.emitir_mensaje(f"Bateria agotada: {self.bateria}%", "ERROR")
            return False
        return True

    def registrar_tarea(self, descripcion):
        self.tareas_realizadas += 1
        self.historial_tareas.append((descripcion, dt.datetime.now()))

    def recargar_bateria(self):
        print("\n> RECARGA DE BATERÍA ===")
        if self.bateria == 100:
            self.emitir_mensaje("La batería ya está al máximo.")
            return

        print("Conectando a estación de carga...")
        t.sleep(1)

        while self.bateria < 100:
            self.bateria = min(self.bateria + 1, 100)
            print(f"\rCargando: {self.bateria}%", end=" ", flush=True)
            t.sleep(0.5)

        print("\n> Tiempo de acraga completado.")
        self.registrar_tarea(f"Recarga de batería")

    def verificar_bateria(self, consumo):
        if self.bateria < consumo:
            self.emitir_mensaje(f"Bateria insuficiente: {self.bateria}%.\nSe requiere por lo menos {consumo}%", "ADVERTENCIA")
            if self.decision.confirmar_accion("¿Deseas recargar ahora?"):
                self.recargar_bateria()
                return True
            return False

    def desplazarse(self):
        print("\n=> NUEVA TAREA: Desplazarse")
        destino = self.decision.pedir_destino("ubicación del destino")

        if self.verificar_bateria(8): return

        recorrido = self.mover(destino)

        print(f"\nDestino designado: {destino}")
        self.ubicacion_actual = destino
        self.usar_bateria(recorrido // 2)
        self.registrar_tarea(f"Desplazamiento a {destino}")

    # Simular la tarea de entregar un documento en un respectivo lugar:
    def trabajar(self):
        print("\n=> NUEVA TAREA: Entregar un documento.")

        if self.verificar_bateria(8): return

        ubicacion = self.decision.pedir_destino("ubicación del documento: ")
        doc = input("Ingrese el nombre del documento: ")

        if not doc: 
            self.emitir_mensaje("Nombre de documento inválido.", "ERROR")
            return

        recorrido = self.mover(ubicacion)
        self.ubicacion_actual = ubicacion
        self.usar_bateria(recorrido // 2)
        t.sleep(0.5)
        self.emitir_mensaje(f"Documento {doc} recogido.", "EXITO")

        destino = self.decision.pedir_destino("ubicación de entrega")
        recorrido_entrega = self.mover(destino)
        self.ubicacion_actual = destino
        self.usar_bateria(recorrido_entrega // 2)
        
        self.emitir_mensaje(f"Documento '{doc}' entregado exitosamente.", "EXITO")
        self.registrar_tarea(f"Entrega de documento: {doc}")
        self.usar_bateria(5)
        
    def servir_cafe(self):
        print("\n=> NUEVA TAREA: Preparar café")

        if self.verificar_bateria(5): return

        tipo = self.decision.elegir_cafe()
        print(f"Preparando café tipo {tipo}...")
        t.sleep(2)
        self.emitir_mensaje(f"Café {tipo} listo. ¡Disfrútalo!", "EXITO")
        self.registrar_tarea(f"Preparación de café {tipo}")
        self.usar_bateria(3)

    def encender_luz(self):
        print("\n=> NUEVA TAREA: Encender las luces")

        if self.verificar_bateria(3):return

        lugar = self.decision.pedir_destino("ubicación (sala/cocina/habitación/etc)")
        print(f"\nEncendiendo las luces en {lugar}...")
        t.sleep(1)
        self.emitir_mensaje(f"Las luces en {lugar} están encendidas.")
        self.registrar_tarea(f"Encender las luces en {lugar}")
        self.usar_bateria(2)

    def estado(self):
        print("\n=> ESTADO DEL SISTEMA:")
        estado_motor = "Activos" if self.motores_activos else "En reposo"
        print(f"Ubicación actual: {self.ubicacion_actual}")
        print(f"Batería: {self.bateria}%")
        print(f"Motores: {estado_motor}")
        print(f"Tareas completadas: {self.tareas_realizadas}")
        self.info_fecha_hora()

    def mostrar_menu(self):
        print("\n" + "="*40)
        print(" "*5 + "MENÚ DE OPCIONES")
        print("="*40)
        
        opciones = [
            "Desplazarse a una ubicación",
            "Entregar un documento",
            "Preparar café",
            "Encender luces",
            "Ver estado del robot",
            "Recargar batería",
            "Salir"
        ]

        for i, opcion in enumerate(opciones, start=1):
            print(f"{i}. {opcion}")
        print("="*40)

    def ejecutar(self):
        acciones = [
            self.desplazarse,
            self.trabajar,
            self.servir_cafe,
            self.encender_luz,
            self.estado,
            self.recargar_bateria,
            self.despedirse
        ]

        while True:
            self.mostrar_menu()
            opcion = input(f"\n¿Qué deseas que haga {self.nombre}? (1-7): ").strip()

            if opcion.isdigit() and 1 <= int(opcion) <= len(acciones):
                acciones[int(opcion) - 1]()
                if opcion == "7": break
            else: self.emitir_mensaje("Opción no válida", "ERROR")

            if self.bateria == 0:
                self.emitir_mensaje("El robot se ha apagado por falta de batería", "ERROR")
                break

if __name__ == "__main__":
    robot = RobotAsistente("Cobot-VX1")
    robot.ejecutar()
