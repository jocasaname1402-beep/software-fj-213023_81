# -*- coding: utf-8 -*-
"""
Modulo con el gestor principal del sistema Software FJ.

Guarda clientes, servicios y reservas en listas internas (sin base de datos)
y atrapa los errores para que la aplicacion nunca se detenga.
"""

from cliente import Cliente
from excepciones import ClienteInvalidoError, SoftwareFJError
from registro import registrar_error, registrar_evento
from reserva import Reserva


class SistemaSoftwareFJ:
    """Administra todas las operaciones de la empresa Software FJ."""

    def __init__(self):
        # Listas internas que reemplazan a la base de datos
        self.clientes = []
        self.servicios = []
        self.reservas = []
        registrar_evento("Sistema Software FJ iniciado")

    def registrar_cliente(self, nombre, documento, correo, telefono):
        """Crea y guarda un cliente; si los datos fallan, devuelve None."""
        try:
            # No se permiten dos clientes con el mismo documento
            if any(c.documento == str(documento) for c in self.clientes):
                raise ClienteInvalidoError(f"Ya existe un cliente con documento {documento}.")
            # Al crear el cliente se ejecutan todas sus validaciones
            cliente = Cliente(nombre, documento, correo, telefono)
        except SoftwareFJError as error:
            # Si algo falla se registra el error y el sistema continua
            registrar_error(error, "registrar_cliente")
            print(f"   [X] Cliente rechazado: {error}")
            return None
        else:
            # Solo si no hubo errores se guarda el cliente en la lista
            self.clientes.append(cliente)
            registrar_evento(f"Cliente registrado: {cliente.describir()}")
            print(f"   [OK] Cliente registrado: {cliente}")
            return cliente

    def agregar_servicio(self, clase_servicio, *args, **kwargs):
        """Crea un servicio de cualquier tipo; si falla, devuelve None."""
        try:
            # Se crea el servicio del tipo recibido (polimorfismo)
            servicio = clase_servicio(*args, **kwargs)
        except SoftwareFJError as error:
            registrar_error(error, f"agregar_servicio({clase_servicio.__name__})")
            print(f"   [X] Servicio rechazado: {error}")
            return None
        else:
            self.servicios.append(servicio)
            registrar_evento(f"Servicio creado: {servicio.describir()}")
            print(f"   [OK] Servicio creado: {servicio}")
            return servicio

    def crear_reserva(self, cliente, servicio, duracion, descuento=None):
        """Crea y confirma una reserva; los errores se registran y no detienen el sistema."""
        try:
            # Se crea la reserva y se intenta confirmar (calcula el costo)
            reserva = Reserva(cliente, servicio, duracion, descuento)
            reserva.confirmar()
        except SoftwareFJError as error:
            registrar_error(error, "crear_reserva")
            print(f"   [X] Reserva fallida: {error}")
            # Si el error fue encadenado se muestra tambien su causa
            if error.__cause__:
                print(f"     causa: {error.__cause__}")
            return None
        else:
            self.reservas.append(reserva)
            print(f"   [OK] Reserva confirmada: {reserva}")
            return reserva

    def procesar_reserva(self, reserva):
        """Procesa una reserva; si no se puede, informa sin detener el sistema."""
        try:
            reserva.procesar()
        except SoftwareFJError as error:
            print(f"   [X] No se pudo procesar: {error}")
        else:
            print(f"   [OK] Reserva procesada: {reserva}")

    def cancelar_reserva(self, reserva):
        """Cancela una reserva; si no se puede, informa sin detener el sistema."""
        try:
            reserva.cancelar()
        except SoftwareFJError as error:
            registrar_error(error, "cancelar_reserva")
            print(f"   [X] No se pudo cancelar: {error}")
        else:
            print(f"   [OK] Reserva cancelada: {reserva}")

    def resumen(self):
        """Muestra un resumen final de lo que quedo guardado."""
        print("\n" + "=" * 70)
        print(" RESUMEN FINAL DEL SISTEMA")
        print("=" * 70)
        print(f" Clientes registrados: {len(self.clientes)}")
        print(f" Servicios activos:    {len(self.servicios)}")
        print(f" Reservas creadas:     {len(self.reservas)}")
        for r in self.reservas:
            print(f"   - {r}")
