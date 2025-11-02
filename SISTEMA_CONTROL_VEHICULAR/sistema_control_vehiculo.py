from abc import ABC, abstractmethod
import time as t

class VehiculoAutonomo:
    @abstractmethod
    def iniciar_sistema(self): pass
    
    @abstractmethod
    def mover(self, destino, distancia): pass
    
    @abstractmethod
    def reportar_estado(self): pass

class AutoInteligente(VehiculoAutonomo):
    def __init__(self, matricula):
        self.matricula = matricula
        self.energia = 100.0
        self.modo = "ESTACIONADO"
        self.velocidad_max = 120 
        
    def iniciar_sistema(self) -> None:
        print(f"\nAuto {self.matricula}: Inicializando sistemas...")
        print("="*50)
        print(f"> Calibrando LIDAR y cámaras perimetrales")
        print(f"> Sincronizando con red de tráfico urbano")
        print(f"> Verificando integridad de baterías")
        self.modo = "LISTO"
        print(f"\nEnergía actual: {self.energia}%")
        
    def mover(self, destino, distancia):
        consumo_energia = distancia * 0.15
        
        if self.energia < consumo_energia:
            print(f"Energía insuficiente para el recorrido.")
            print(f"Redirigiendo a estación de carga más cercana...\n")
            return
            
        print("\n> OPERACIÓN EN MARCHA:")
        print(f"Auto {self.matricula} → Destino: {destino}")
        t.sleep(0.5)
        print(f"Calculando ruta óptima ({distancia} km)...")
        t.sleep(0.5)
        print(f"Iniciando trayecto...")
        
        self.energia -= consumo_energia
        self.modo = "EN_RUTA"
        
        t.sleep(1.5)
        print(f"\nDestino alcanzado. Energía restante: {self.energia:.1f}%")
        
    def reportar_estado(self):
        estado = {
            "tipo": "Auto Inteligente",
            "id": self.matricula,
            "energia": f"{self.energia:.1f}%",
            "modo": self.modo,
            "capacidad": "4 pasajeros",
            "autonomia_restante": f"{self.energia / 0.15:.1f} km"
        }
        
        print("\nREPORTE DE ESTADO - Auto Inteligente")
        print("="*50)
        for clave, valor in estado.items():
            print(f"> {clave.capitalize()}: {valor}")
        
class DronAereo(VehiculoAutonomo):
    def __init__(self, id):
        self.id = id
        self.energia = 100.0
        self.posicion = (0.0, 0.0, 0.0)
        self.modo = "EN_TIERRA"
        self.altitud_crucero = 120
        
    def iniciar_sistema(self) -> None:
        print(f"Dron {self.id}: Iniciando secuencia de despegue...")
        print("="*50)
        print(f"> Testeando rotores y estabilizadores")
        print(f"> Conectando con control de tráfico aéreo")
        print(f"> Validando permisos de espacio aéreo")
        self.modo = "PREPARADO"
        print(f"\nEnergía actual: {self.energia}%")
        
    def mover(self, destino, distancia):
        consumo_energia = distancia * 0.25
        
        if self.energia < consumo_energia:
            print(f"Batería crítica. Abortando vuelo.")
            print(f"Iniciando protocolo de aterrizaje de emergencia...\n")
            return
            
        print(f"Dron {self.id} → Destino: {destino}")
        print(f"Elevándose a {self.altitud_crucero}m de altitud...")
        print(f"Volando en línea recta ({distancia} km)...")
        
        self.energia -= consumo_energia
        self.posicion = (self.posicion[0] + distancia*0.7,
                        self.posicion[1] + distancia*0.4,
                        self.altitud_crucero)
        self.modo = "EN_VUELO"

        t.sleep(1.5)
        print(f"Aterrizaje completado. Batería: {self.energia:.1f}%\n")
        
    def reportar_estado(self) -> dict:
        estado = {
            "tipo": "Dron Aéreo",
            "id": self.id,
            "energia": f"{self.energia:.1f}%",
            "posicion": f"X:{self.posicion[0]:.1f}, Y:{self.posicion[1]:.1f}, ALT:{self.posicion[2]:.0f}m",
            "modo": self.modo,
            "carga_max": "5 kg",
            "tiempo_vuelo_restante": f"{self.energia / 0.25 * 6:.0f} minutos"
        }
        
        print("\nREPORTE DE ESTADO - Dron Aéreo")
        print("="*50)
        for clave, valor in estado.items():
            print(f"> {clave.capitalize()}: {valor}")

class RobotRepartidor(VehiculoAutonomo):
    def __init__(self, codigo):
        self.codigo = codigo
        self.energia = 100.0
        self.posicion = (0.0, 0.0)
        self.modo = "ESPERANDO_CARGA"
        self.compartimento_ocupado = False
        self.velocidad_max = 15 #capacidad maxima en km
        
    def iniciar_sistema(self) -> None:
        print(f"Robot {self.codigo}: Activando sistemas de reparto...")
        print("="*50)
        print(f"> Calibrando sensores de obstáculos peatonales")
        print(f"> Verificando mecanismo de compartimento seguro")
        print(f"> Sincronizando con plataforma de pedidos")
        self.modo = "DISPONIBLE"
        print(f"\nRobot preparado. Energía actual: {self.energia}%")

    def mover(self, destino, distancia):
        consumo_energia = distancia * 0.08
        
        if self.energia < consumo_energia:
            print(f"Energía insuficiente. Cancelando entrega a {destino}")
            print(f"Solicitando robot de reemplazo...\n")
            return
            
        print(f"Robot {self.codigo} → Destino: {destino}")
        print(f"Navegando por aceras y ciclovías ({distancia} km)...")
        
        self.energia -= consumo_energia
        self.posicion = (self.posicion[0] + distancia*0.4, 
                        self.posicion[1] + distancia*0.6)
        self.modo = "EN_ENTREGA"
        
        t.sleep(1.5)
        print(f"> Entrega realizada. Energía: {self.energia:.1f}%\n")
        
    def reportar_estado(self):
        estado = {
            "tipo": "Robot Repartidor",
            "codigo": self.codigo,
            "energia": f"{self.energia:.1f}%",
            "posicion": f"GPS {self.posicion[0]:.2f}, {self.posicion[1]:.2f}",
            "modo": self.modo,
            "compartimento": "OCUPADO" if self.compartimento_ocupado else "VACÍO",
            "entregas_pendientes": "1" if self.compartimento_ocupado else "0",
            "rango_operativo (energía)": f"{self.energia / 0.08:.1f} km"
        }
        
        print("\nREPORTE DE ESTADO - Robot Repartidor")
        print("="*50)
        for clave, valor in estado.items():
            print(f"> {clave.capitalize()}: {valor}")
        
class CentroControl:
    def __init__(self):
        #especificamos eltipo de valores en la lista
        self.vehiculos: list[VehiculoAutonomo] = []
        
    def registrar_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)
        tipo = vehiculo.__class__.__name__
        t.sleep(0.5)
        print(f"> {tipo} registrado en el sistema de control")
        
    def activar_vehiculos(self) -> None:
        print("\n" + "═" * 60)
        print("CENTRO DE CONTROL - Iniciando operaciones")
        print("═" * 60 + "\n")
        
        for vehiculo in self.vehiculos:
            vehiculo.iniciar_sistema()
            
    def despachar_mision(self, vehiculo, destino, distancia):
        vehiculo.mover(destino, distancia)
        
    def monitorear_vehiculos(self) -> None:
        print("\n" + "═" * 60)
        print("CENTRO DE CONTROL - Monitoreo de operaciones")
        print("═" * 60 + "\n")
        
        for vehiculo in self.vehiculos:
            vehiculo.reportar_estado()

ctr_control = CentroControl()

vh_1 = AutoInteligente("ADC-2024")
vh_2 = DronAereo("DRN-X789")
vh_3 = RobotRepartidor("RBT-4521")

for vh in [vh_1, vh_2, vh_3]: ctr_control.registrar_vehiculo(vh)
ctr_control.activar_vehiculos()

print("═" * 60)
print("CENTRO DE CONTROL - Despiege de operaciones")
print("═" * 60 + "\n")

ctr_control.despachar_mision(vh_1, "Mall Plaza Comas", 15.5)
ctr_control.despachar_mision(vh_2, "Hospital de Urgencias", 8.2)
ctr_control.despachar_mision(vh_3, "Oficina central", 3.7)

ctr_control.monitorear_vehiculos()