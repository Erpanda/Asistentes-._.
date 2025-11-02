from abc import ABC, abstractmethod

class MetodoPago(ABC):
    @abstractmethod
    def validar_monto(self, monto): pass

    @abstractmethod
    def procesar_pago(self, monto): pass

class TarjetaCredito(MetodoPago):
    __limite = 5000

    def __init__(self, titular, nro_tarjeta, saldo):
        self.titular = titular
        self.nro_tarjeta = nro_tarjeta
        self.saldo = saldo

    def validar_monto(self, monto):
        print(f"Verificando saldo de la tarjeta de {self.titular}...")
        return 0 <= monto <= self.__limite and monto <= self.saldo
    
    def procesar_pago(self, monto):
        if not self.validar_monto(monto):
            return f"ERROR: El monto S/{monto:.2f} excede el límite de S/{self.__limite} o el saldo es insuficiente."
        self.saldo -= monto
        return f"PAGO EXITOSO: Pago de S/ {monto:.2f} realizado con tarjeta de {self.titular}..."

class BilleteraVirtual(MetodoPago):
    __limite = 1000

    def __init__(self, email, saldo):
        self.email = email
        self.saldo = saldo

    def validar_monto(self, monto):
        print(f"Verificando saldo de la billetera digital...")
        return 0 <= monto <= self.__limite and monto <= self.saldo
    
    def procesar_pago(self, monto):
        if not self.validar_monto(monto):
            return f"ERROR: El monto S/{monto:.2f} excede el límite de S/{self.__limite} o el saldo es insuficiente."
        self.saldo -= monto
        return f"PAGO EXITOSO: Pago de S/ {monto:.2f} realizado con la billetera digital (user: #{self.email})..."

class PayPal(MetodoPago):
    __limite = 3000

    def __init__(self, correo, saldo):
        self.correo = correo
        self.saldo = saldo

    def validar_monto(self, monto):
        print(f"Verificando cuenta PayPal {self.correo}...")
        return 0 < monto <= self.__limite and monto <= self.saldo
    
    def procesar_pago(self, monto):
        if not self.validar_monto(monto):
            return f"ERROR: El monto S/{monto:.2f} excede el límite de S/{self.__limite} o el saldo es insuficiente."
        self.saldo -= monto
        return f"PAGO EXITOSO: Pago de S/{monto:.2f} procesado mediante PayPal ({self.correo}). Saldo restante: S/{self.saldo:.2f}"


class CriptoMoneda(MetodoPago):
    __tasa_conversion = 250000

    def __init__(self, billetera, saldo_btc):
        self.billetera = billetera
        self.saldo_btc = saldo_btc
    
    def validar_monto(self, monto):
        print(f"Verificando saldo en billetera ({self.billetera})...")
        monto_btc = monto / self.__tasa_conversion
        return monto > 0 and self.saldo_btc >= monto_btc
    
    def procesar_pago(self, monto):
        monto_btc = monto / self.__tasa_conversion
        if not self.validar_monto(monto):
            return f"ERROR: El monto S/{monto:.2f} ({monto_btc:.6f} BTC) excede el saldo disponible en la billetera ({self.billetera})."
        self.saldo_btc -= monto_btc
        return f"PAGO EXITOSO: Pago de S/{monto:.2f} realizado desde {self.billetera} ({monto_btc:.6f} BTC). Saldo restante: {self.saldo_btc:.6f} BTC"

class SistemaPagos:
    def __init__(self):
        self.historial = []
    
    def realizar_pago(self, metodo_pago, monto, descripcion=""):
        print(f"\n{'='*70}")
        print(f"PROCESANDO PAGO: {descripcion}")
        print(f"{'='*70}")
        
        resultado = metodo_pago.procesar_pago(monto)
        print(resultado)
        
        self.historial.append({
            'metodo': metodo_pago.__class__.__name__,
            'monto': monto,
            'descripcion': descripcion,
            'exitoso': 'EXITOSO' in resultado # True si "EXITOSO" esta en la respuesta ._.
        })
    
    def mostrar_historial(self):
        print(f"\n{'='*70}")
        print("HISTORIAL DE OPERACIONES:")
        print(f"{'='*70}")
        
        if not self.historial:
            print("ERROR: No hay operaciones registradas.")
            return
        
        exitosas = sum(1 for t in self.historial if t['exitoso'])
        rechazadas = len(self.historial) - exitosas
        
        for i, ope in enumerate(self.historial, 1):
            estado = "APROBADO" if ope['exitoso'] else "RECHAZADO"
            print(f"{i}. [{estado}] {ope['metodo']} - S/{ope['monto']:.2f} - {ope['descripcion']}")
        
        print(f"\nRESUMEN DE OPERACIONES: {exitosas} exitosas | {rechazadas} rechazadas")


op_tarjeta = TarjetaCredito("Juan Pérez", "4532876543210987", 4000)
op_billetera = BilleteraVirtual("maria@email.com", 800)
op_paypal = PayPal("carlos@email.com", 2500)
op_cripto = CriptoMoneda("1A1zP1eP5QGe", 0.05)

sistema_pago = SistemaPagos()

sistema_pago.realizar_pago(op_tarjeta, 3000, "Compra de computadora")
sistema_pago.realizar_pago(op_billetera, 500, "Pago de internet")
sistema_pago.realizar_pago(op_paypal, 1500, "Suscripción anual")
sistema_pago.realizar_pago(op_cripto, 10000, "Inversión en acciones") 

sistema_pago.mostrar_historial()